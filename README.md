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

| SC | GREEN 달성 |
|----|------------|
| SC1 | ✅ U-CLI-01 (G1 `meter:2.5`) |
| SC2 | ⚳ entity D-EXT ✅ · CLI FR-9 ❌ |
| SC3 | ✅ pytest 18 passed |

상세: [`docs/PRD.md`](./docs/PRD.md) · [`Report/2.ProblemDefinition_Report.md`](./Report/2.ProblemDefinition_Report.md) · [**Report 8 — 누적 SSOT**](./Report/8.%20UnitConverter_Progress_Summary_Report.md)

---

## 아키텍처 (ECB)

의존 방향: **boundary → control → entity**

| 계층 | 책임 | 구현 (GREEN) |
|------|------|----------------|
| **Entity** | 변환 비율·순수 변환·검증 | `convert_length()`, `constants.py`, `registry.py` |
| **Control** | 파싱·유스케이스 조율 | `parse_input()`, `convert_all()`, `convert_excluding_input()` |
| **Boundary** | CLI·입출력 | `src/boundary/cli.py` · `UnitConverter.py` thin wrapper |

- **Dual-Track TDD:** Logic `D-*` (`tests/entity`, `tests/control`) + UI `U-*` (`tests/boundary`)
- **RED 우선:** pytest FAIL → GREEN → REFACTOR
- 규칙 SSOT: [`.cursorrules`](./.cursorrules) · Skill: [`.cursor/skills/unit-conversion-tdd/`](./.cursor/skills/unit-conversion-tdd/)

---

> **누적 진행 SSOT:** [Report/8. UnitConverter_Progress_Summary_Report.md](./Report/8.%20UnitConverter_Progress_Summary_Report.md)

## TDD 진행 목록

> 규칙: **RED → GREEN → REFACTOR** · 테스트 ID SSOT: [reference.md](./.cursor/skills/unit-conversion-tdd/reference.md)  
> **현재 Phase:** GREEN 완료 · **다음:** REFACTOR

### 공통 Harness

- [x] `tests/conftest.py` — G1 격자·검증·확장 픽스처 (비율 SSOT: `entity.constants`)
- [x] `src/entity/constants.py` — `METER_TO_FEET`, `METER_TO_YARD`

**G1 변환 격자** — anchor `2.5 meter`:

```
D-CONV-01: 2.5 meter → 8.2021 feet    (× 3.28084)
D-CONV-02: 2.5 meter → 2.734025 yard  (× 1.09361)
D-CONV-03: 8.2021 feet → 2.734025 yard (meter 경유)
```

### Track B — Logic (`tests/entity/`, `tests/control/`)

| Test ID | 작업 | 상태 |
|---------|------|------|
| D-CONV-01~03 | `convert_length()` · G1 격자 | ✅ GREEN |
| D-CONV-04 | `convert_all()` — **등록 전 단위** (입력 포함) | ✅ GREEN |
| D-CONV-05 | `convert_excluding_input()` — 입력 단위 제외 | ✅ GREEN |
| D-VAL-01~03 | entity 입력 검증 | ✅ GREEN |
| D-VAL-04~05 | control 파싱 | ✅ GREEN |
| D-EXT-01~02 | `register_unit()` OCP | ✅ GREEN |

### Track A — UI (`tests/boundary/`)

| Test ID | 작업 | 상태 |
|---------|------|------|
| U-CLI-01 | G1 변환 Golden Master + `main()` capsys | ✅ GREEN |
| U-CLI-02~05 | 검증 Golden Master | ✅ GREEN |

### GREEN 완료 게이트

- [x] Logic: `pytest tests/entity tests/control -q` — **12 passed**
- [x] UI: `pytest tests/boundary -q` — **6 passed**
- [x] 전체: `pytest -q` — **18 passed**
- [x] Golden Master: `tests/boundary/fixtures/u_cli_01~05.stdout`
- [ ] REFACTOR — 구조 개선·문서 동기화

---

## RED 단계 (완료 · 참고)

<details>
<summary>RED 12건 스켈레톤 · 의도적 FAIL 이력</summary>

**권장 순서 (PRD §6.4):** Loop 1 `D-CONV-*` → Loop 2 `D-VAL-*` → Loop 3 `D-EXT-*` → UI `U-*`

| Test ID | RED 작업 | 상태 |
|---------|----------|------|
| D-CONV-01~03 | `test_d_conv_01.py` | ✅ RED → GREEN |
| D-CONV-04~05 | `test_d_conv_04~05.py` | ✅ RED → GREEN |
| D-VAL-01~05 | entity/control 검증 | ✅ RED → GREEN |
| D-EXT-01~02 | OCP 확장 | ✅ RED → GREEN |

Logic RED 게이트: 12 failed (의도) → GREEN 12 passed.

</details>

---

## C2C 요약

| Test ID | PRD | Layer | 요약 |
|---------|-----|-------|------|
| D-CONV-01 | FR-2 | entity | meter → feet (**RED 우선 묶음**) |
| D-CONV-02 | FR-2 | entity | meter → yard |
| D-CONV-03 | FR-2 | entity | feet → yard (meter 경유) |
| D-CONV-04 | FR-2 | control | `convert_all()` — 등록 전 단위 (입력 포함, 내부 격자) |
| D-CONV-05 | FR-3 | control | `convert_excluding_input()` — CLI/boundary 출력 계약 |
| D-VAL-01~03 | FR-4 | entity | 음수·잘못된 숫자·미등록 단위 거부 |
| D-VAL-04~05 | FR-1, FR-4 | control | 파싱·형식 검증 |
| D-EXT-01~02 | FR-5, SC2 | entity | OCP 단위 확장 |
| U-CLI-01~05 | FR-3, FR-4, SC1 | boundary | Golden Master CLI |

**판단 (entity API):** `convert_length(value, from_unit, to_unit) -> float` 단일 순수 함수로 확정. 입력 검증은 Loop 2(`D-VAL-*`)로 분리.

---

## Project Structure

```
UnitConverter_28/
├── UnitConverter.py              # boundary thin wrapper → src/boundary/cli
├── README.md
├── .cursorrules                  # ECB · Dual-Track · TDD 정책
├── pyproject.toml                # pytest testpaths · pythonpath=src
├── docs/
│   └── PRD.md
├── Report/
│   ├── 1. mom-test-report.md
│   ├── 2. ProblemDefinition_Report.md
│   ├── 3. AI-Layer-Setup_Report.md
│   ├── 4. UnitConverter_RED_Design_Report.md
│   ├── 5. UnitConverter_RED_Skeleton_Report.md
│   ├── 6. UnitConverter_Logic_RED_Complete_Report.md
│   ├── 7. UnitConverter_GREEN_Complete_Report.md
│   └── 8. UnitConverter_Progress_Summary_Report.md   # 누적 SSOT
├── Prompt/
│   ├── 1. mom-test-transcript.md
│   ├── 2. ProblemDefinition-transcript.md
│   ├── 3. AI-Layer-Setup-transcript.md
│   ├── 4. UnitConverter_RED_Design-Transcript.md
│   ├── 5. UnitConverter_RED_Skeleton-Transcript.md
│   ├── 6. UnitConverter_Logic_RED_Complete-Transcript.md
│   ├── 7. UnitConverter_GREEN_Complete-Transcript.md
│   └── 8. UnitConverter_Progress_Export-Transcript.md
├── src/
│   ├── entity/                   # 변환·비율 (순수 로직)
│   ├── control/                  # 파싱·유스케이스
│   └── boundary/                 # CLI·I/O
├── tests/
│   ├── conftest.py               # G1·검증·확장 픽스처 (데이터만)
│   ├── entity/                   # test_d_conv_*.py, test_d_val_*.py, test_d_ext_*.py
│   ├── control/
│   └── boundary/                 # test_u_cli_*.py · fixtures/*.stdout
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

# 테스트 — Layer별
pytest tests/entity -q
pytest tests/control -q
pytest tests/boundary -q

# 전체 (GREEN: 18 passed)
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

출력 예시 (CLI — **입력 단위 제외**, 테스트 정밀값):

```
2.5 meter = 8.2021 feet
2.5 meter = 2.734025 yard
```

> README 요약(8.2 feet)은 반올림 표현 · Golden Master·Logic 테스트는 **8.2021** SSOT.

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

1. **REFACTOR** — 예외 매핑·`validate_numeric` 연결·중복 제거
2. UI 확장 — feet/yard 입력 Golden Master (선택)
3. PRD SC1~3 체크리스트 갱신

---

## References

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](./docs/PRD.md) | **SSOT** — FR/SC/Loop/TDD |
| [.cursorrules](./.cursorrules) | ECB · Dual-Track · TDD 게이트 |
| [reference.md](./.cursor/skills/unit-conversion-tdd/reference.md) | **D-* 테스트 ID** |
| [Report/3. AI-Layer-Setup_Report.md](./Report/3.%20AI-Layer-Setup_Report.md) | Harness · Hook · 8계층 |
| [Report/4. UnitConverter_RED_Design_Report.md](./Report/4.%20UnitConverter_RED_Design_Report.md) | RED 설계 · C2C · G1 격자 |
| [Report/5. UnitConverter_RED_Skeleton_Report.md](./Report/5.%20UnitConverter_RED_Skeleton_Report.md) | RED 스켈레톤 · D-CONV-01 FAIL |
| [Report/6. UnitConverter_Logic_RED_Complete_Report.md](./Report/6.%20UnitConverter_Logic_RED_Complete_Report.md) | Logic RED 12건 완료 |
| [Report/7. UnitConverter_GREEN_Complete_Report.md](./Report/7.%20UnitConverter_GREEN_Complete_Report.md) | GREEN · Golden Master · convert_all 정리 |
| [Report/8. UnitConverter_Progress_Summary_Report.md](./Report/8.%20UnitConverter_Progress_Summary_Report.md) | **누적 진행 SSOT** · REFACTOR 백로그 |
| [Prompt/4. UnitConverter_RED_Design-Transcript.md](./Prompt/4.%20UnitConverter_RED_Design-Transcript.md) | 세션 4 Transcript |
| [Prompt/5. UnitConverter_RED_Skeleton-Transcript.md](./Prompt/5.%20UnitConverter_RED_Skeleton-Transcript.md) | 세션 5 Transcript |
| [Prompt/6. UnitConverter_Logic_RED_Complete-Transcript.md](./Prompt/6.%20UnitConverter_Logic_RED_Complete-Transcript.md) | 세션 6 Transcript |
| [Prompt/7. UnitConverter_GREEN_Complete-Transcript.md](./Prompt/7.%20UnitConverter_GREEN_Complete-Transcript.md) | 세션 7 GREEN Transcript |
| [Prompt/8. UnitConverter_Progress_Export-Transcript.md](./Prompt/8.%20UnitConverter_Progress_Export-Transcript.md) | 세션 8 Export Transcript |
| [Mom Test Report](./Report/1.%20mom-test-report.md) | 인터뷰 증거 |
| [Problem Definition Report](./Report/2.ProblemDefinition_Report.md) | R-G-I-O · SC1~3 |
