# Unit Converter (Python)

![unit-converter](./unit-converter.jpg)

## Overview

사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 **다른 모든 단위**로 변환해 출력하는 프로그램.

- 새로운 단위 추가 시 기존 코드 변경을 최소화하도록 설계 (OCP)
- 입력 검증 / 변환 / 출력 책임 분리 (SRP)
- 단위 변환 로직은 테스트 코드로 검증 (TDD)

### Problem (Mom Test)

> **진짜 문제:** 외울 수 없는 다양한 단위 조합 앞에서, 매번 찾아보느라 바로 답하지 못하고 과제가 지연된다.

| 성공 기준 | 설명 |
|-----------|------|
| **SC1** | 한 번 입력 → 전 단위 변환 결과 즉시 출력 |
| **SC2** | 새 단위 추가 시 기존 코드 최소 변경 |
| **SC3** | 테스트 통과 → 제출 전 재확인 불필요 |

상세: [`docs/PRD.md`](./docs/PRD.md) · [`Report/2.ProblemDefinition_Report.md`](./Report/2.ProblemDefinition_Report.md)

---

## 아키텍처 (ECB)

의존 방향: **boundary → control → entity**

| 계층 | 책임 | 후보 |
|------|------|------|
| **Entity** | 변환 비율·순수 변환 로직 | `convert_length()`, `constants.py` |
| **Control** | 파싱·유스케이스 조율 | `UnitConverter`, `InputParser` |
| **Boundary** | CLI·입출력 | `UnitConverter.py` thin wrapper |

- **Dual-Track TDD:** Logic `D-*` (`tests/entity`, `tests/control`) + UI `U-*` (`tests/boundary`)
- **RED 우선:** pytest FAIL → GREEN → REFACTOR
- 규칙 SSOT: [`.cursorrules`](./.cursorrules) · Skill: [`.cursor/skills/unit-conversion-tdd/`](./.cursor/skills/unit-conversion-tdd/)

---

## RED 단계 진행 목록

> 규칙: **RED 1턴 = 테스트 ID 1묶음** · 변경은 `tests/`만 · `skip`/`xfail` 금지 · Logic Track Domain Mock 금지  
> 테스트 ID SSOT: [`.cursor/skills/unit-conversion-tdd/reference.md`](./.cursor/skills/unit-conversion-tdd/reference.md)

**권장 순서 (PRD §6.4):** Loop 1 `D-CONV-*` → Loop 2 `D-VAL-*` → Loop 3 `D-EXT-*` → UI `U-*` (Logic GREEN 후)

### 공통 Harness (RED 선행)

- [ ] `tests/conftest.py` — G1 변환 격자 픽스처 (데이터만, 도메인 로직 없음)
- [ ] `src/entity/constants.py` — `METER_TO_FEET`, `METER_TO_YARD` SSOT (GREEN 시)

**G1 변환 격자 (RED SSOT)** — anchor `2.5 meter`:

```
D-CONV-01: 2.5 meter → 8.2021 feet    (× 3.28084)
D-CONV-02: 2.5 meter → 2.734025 yard  (× 1.09361)
D-CONV-03: 8.2021 feet → 2.734025 yard (meter 경유, D-CONV-02와 일치)
```

### Track B — Logic (`tests/entity/`, `tests/control/`)

| Test ID | RED 작업 | pytest (예시) | 상태 |
|---------|----------|---------------|------|
| D-CONV-01 | `test_d_conv_01.py` — `convert_length()` · G1 meter→feet | `pytest tests/entity/test_d_conv_01.py::test_d_conv_01_meter_to_feet -v` | ⏳ |
| D-CONV-02 | `test_d_conv_01.py` — `convert_length()` · G1 meter→yard | `pytest tests/entity/test_d_conv_01.py::test_d_conv_02_meter_to_yard -v` | ⏳ |
| D-CONV-03 | `test_d_conv_01.py` — `convert_length()` · G1 feet→yard | `pytest tests/entity/test_d_conv_01.py::test_d_conv_03_feet_to_yard -v` | ⏳ |
| D-CONV-04 | `test_d_conv_04.py` — 단일 입력 → 전 단위 변환 결과 | `pytest tests/control/test_d_conv_04.py -v` | ⏳ |
| D-CONV-05 | `test_d_conv_05.py` — 입력 단위 제외 출력 목록 | `pytest tests/control/test_d_conv_05.py -v` | ⏳ |
| D-VAL-01 | `test_d_val_01.py` — 음수 값 거부 | `pytest tests/entity/test_d_val_01.py -v` | ⏳ |
| D-VAL-02 | `test_d_val_02.py` — 잘못된 숫자 거부 | `pytest tests/entity/test_d_val_02.py -v` | ⏳ |
| D-VAL-03 | `test_d_val_03.py` — 미등록 단위 거부 | `pytest tests/entity/test_d_val_03.py -v` | ⏳ |
| D-VAL-04 | `test_d_val_04.py` — 콜론 없는 형식 거부 | `pytest tests/control/test_d_val_04.py -v` | ⏳ |
| D-VAL-05 | `test_d_val_05.py` — `단위:값` 파싱 성공 | `pytest tests/control/test_d_val_05.py -v` | ⏳ |
| D-EXT-01 | `test_d_ext_01.py` — 새 단위 등록 후 전체 변환 | `pytest tests/entity/test_d_ext_01.py -v` | ⏳ |
| D-EXT-02 | `test_d_ext_02.py` — 등록만으로 확장 (OCP) | `pytest tests/entity/test_d_ext_02.py -v` | ⏳ |

**Logic RED 게이트:** 각 ID마다 터미널 **FAILED** (`ModuleNotFoundError` / `pytest.fail("RED: D-xxx …")`) 확인 후 GREEN.

### Track A — UI (`tests/boundary/`)

> Logic Layer GREEN 후 시작 · control·stdin/stdout mock 허용 · entity 직접 mock 금지

| Test ID | RED 작업 | 상태 |
|---------|----------|------|
| U-CLI-01~ | CLI 입출력·Golden Master | ⏳ (ID 확정 후 `reference.md` 보강) |

### RED 완료 게이트

- [ ] Loop 1 entity: `pytest tests/entity/test_d_conv_01.py -v` — D-CONV-01~03 RED FAIL 확보
- [ ] Loop 1 control: `pytest tests/control/ -v` — D-CONV-04~05 RED FAIL 확보
- [ ] 이후 GREEN → REFACTOR (`.cursor/commands/tdd-red.md` 참고)

---

## C2C 요약

| Test ID | PRD | Layer | 요약 |
|---------|-----|-------|------|
| D-CONV-01 | FR-2 | entity | meter → feet (**RED 우선 묶음**) |
| D-CONV-02 | FR-2 | entity | meter → yard |
| D-CONV-03 | FR-2 | entity | feet → yard (meter 경유) |
| D-CONV-04 | FR-3 | control | 단일 입력 → 전 단위 결과 |
| D-CONV-05 | FR-3 | control | 입력 단위 제외 목록 |
| D-VAL-01~03 | FR-4 | entity | 음수·형식·미등록 단위 거부 |
| D-VAL-04~05 | FR-1, FR-4 | control | 파싱·형식 검증 |
| D-EXT-01~02 | FR-5, SC2 | entity | OCP 단위 확장 |

**판단 (entity API):** `convert_length(value, from_unit, to_unit) -> float` 단일 순수 함수로 확정. 입력 검증은 Loop 2(`D-VAL-*`)로 분리.

---

## Project Structure

```
UnitConverter_28/
├── UnitConverter.py              # boundary 진입점 (스타터, 향후 thin wrapper)
├── README.md
├── .cursorrules                  # ECB · Dual-Track · TDD 정책
├── pyproject.toml                # pytest testpaths · pythonpath=src
├── docs/
│   └── PRD.md
├── Report/
│   ├── 1. mom-test-report.md
│   ├── 2. ProblemDefinition_Report.md
│   ├── 3. AI-Layer-Setup_Report.md
│   └── 4. UnitConverter_RED_Design_Report.md
├── Prompt/
│   ├── 1. mom-test-transcript.md
│   ├── 2. ProblemDefinition-transcript.md
│   ├── 3. AI-Layer-Setup-transcript.md
│   └── 4. UnitConverter_RED_Design-Transcript.md
├── src/
│   ├── entity/                   # 변환·비율 (순수 로직)
│   ├── control/                  # 파싱·유스케이스
│   └── boundary/                 # CLI·I/O
├── tests/
│   ├── conftest.py               # G1 픽스처 (RED 예정)
│   ├── entity/                   # test_d_conv_*.py, test_d_val_*.py
│   ├── control/
│   └── boundary/                 # test_u_*.py
└── .cursor/
    ├── commands/                 # tdd-red.md, review-ecb.md
    ├── hooks/                    # pytest 자동 실행·스냅샷 차단
    └── skills/unit-conversion-tdd/
        ├── SKILL.md
        └── reference.md          # D-* ID SSOT
```

---

## Setup & Run

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 실행
python UnitConverter.py

# 테스트 — Layer 작업 중
pytest tests/entity -q

# RED — 현재 묶음 (D-CONV-01~03)
pytest tests/entity/test_d_conv_01.py -v

# 전체 (Phase 종료·REFACTOR 후)
pytest -q

# 가상환경 비활성화
deactivate
```

---

## Requirements

### Input / Output

입력 예시:

```
meter:2.5
```

출력 예시:

```
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
...
```

### Supported Units

- meter
- feet
- yard

### Business Logic

- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간 비율은 meter 기준으로 계산

### Quality

- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)
- 단위 변환 및 입력 검증 테스트 코드

### Additional (Should Have)

- **설정 외부화** — 변환 비율을 JSON/YAML 설정 파일에서 로드
- **동적 단위 등록** — 예: `1 cubit = 0.4572 meter`
- **출력 포맷 선택** — JSON / CSV / 표 형태

---

## Activities (생성형 AI 활용, 6시간)

| # | 활동 | 시간 |
|---|------|------|
| 1 | 문제 코드 및 기본 요구사항 분석 | 0.5h |
| 2 | 기본·품질 요구사항 구현 (OCP/SRP/입력 검증) | 2h |
| 3 | TC 구현 (단위 변환·입력 검증) | 0.5h |
| 4 | 추가 요구사항 구현 및 TC | 2h |
| 5 | 회고 및 발표 | 1h |

**회고 항목**

- 실습 목표와 달성도
- AI 활용 — 도움이 된 순간과 한계
- TC 추가가 개선에 미친 영향, TC 작성 팁
- 클린코드·리팩토링에서 느낀 장점과 어려운 점

---

## 다음 단계

1. `/red-skeleton` — `tests/conftest.py` G1 픽스처 + `tests/entity/test_d_conv_01.py` RED 스켈레톤 (D-CONV-01~03)
2. `pytest` **FAILED** 로그 확보 → GREEN은 ID 1묶음씩
3. entity GREEN 후 control `D-CONV-04`~`05` RED
4. Logic Track 완료 후 boundary `U-*` RED

---

## References

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](./docs/PRD.md) | **SSOT** — FR/SC/Loop/TDD |
| [.cursorrules](./.cursorrules) | ECB · Dual-Track · TDD 게이트 |
| [reference.md](./.cursor/skills/unit-conversion-tdd/reference.md) | **D-* 테스트 ID** |
| [Report/3. AI-Layer-Setup_Report.md](./Report/3.%20AI-Layer-Setup_Report.md) | Harness · Hook · 8계층 |
| [Report/4. UnitConverter_RED_Design_Report.md](./Report/4.%20UnitConverter_RED_Design_Report.md) | RED 설계 · C2C · G1 격자 |
| [Prompt/4. UnitConverter_RED_Design-Transcript.md](./Prompt/4.%20UnitConverter_RED_Design-Transcript.md) | 세션 4 Transcript |
| [Mom Test Report](./Report/1.%20mom-test-report.md) | 인터뷰 증거 |
| [Problem Definition Report](./Report/2.ProblemDefinition_Report.md) | R-G-I-O · SC1~3 |
