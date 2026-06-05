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

상세: [`docs/PRD.md`](./docs/PRD.md) · [`2. ProblemDefinition_Report.md`](./docs/Report/2.%20ProblemDefinition_Report.md) · [**Report 10 — 최신 SSOT**](./docs/Report/10.%20UnitConverter_REFACTOR_Complete_Report.md) · [Report 8 — GREEN 시점 SSOT](./docs/Report/8.%20UnitConverter_Progress_Summary_Report.md)

---

## 아키텍처 (ECB)

의존 방향: **boundary → control → entity**

| 계층 | 책임 | 구현 (GREEN) |
|------|------|----------------|
| **Entity** | 변환 비율·순수 변환·검증 | `convert_length()`, `constants.py`, `registry.py` |
| **Control** | 파싱·유스케이스 조율 | `parse_input()`, `_convert_units()`, `convert_all()`, `convert_excluding_input()` |
| **Boundary** | CLI·입출력·포맷 | `process()` → `ProcessResult`, `format_number()`, `run()` · `UnitConverter.py` thin wrapper |
| **Boundary (GUI)** | PyQt 화면 | `qt_app.py` · `process(..., format_numbers=True)` · `UnitConverterGUI.py` |

- **Dual-Track TDD:** Logic `D-*` (`tests/entity`, `tests/control`) + UI `U-*` (`tests/boundary`)
- **RED 우선:** pytest FAIL → GREEN → REFACTOR
- 규칙 SSOT: [`.cursorrules`](./.cursorrules) · Skill: [`.cursor/skills/unit-conversion-tdd/`](./.cursor/skills/unit-conversion-tdd/)

---

> **최신 진행:** [Report/10. UnitConverter_REFACTOR_Complete_Report.md](./docs/Report/10.%20UnitConverter_REFACTOR_Complete_Report.md) · [Report/9 — Post-GREEN GUI](./docs/Report/9.%20UnitConverter_PostGREEN_GUI_Report.md)

## TDD 진행 목록

> 규칙: **RED → GREEN → REFACTOR** · 테스트 ID SSOT: [reference.md](./.cursor/skills/unit-conversion-tdd/reference.md)  
> **현재 Phase:** **REFACTOR 완료** (Dual-Track TDD Must Have) · **다음:** (선택) U-GUI-* · `validate_numeric` 연결

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

Golden Master는 **UI Track(boundary)만** 사용합니다. Logic Track(`D-*`)은 `tests/entity/`·`tests/control/`에서 도메인 값·예외를 직접 검증합니다. 상세: [`golden/README.md`](./golden/README.md).

| Test ID | 작업 | 상태 |
|---------|------|------|
| U-CLI-01 | G1 변환 Golden Master + `main()` capsys | ✅ GREEN |
| U-CLI-02~05 | 검증 Golden Master (`test_u_cli_rejections.py`) | ✅ GREEN · REFACTOR |

### GREEN · REFACTOR 완료 게이트

- [x] Logic: `pytest tests/entity tests/control -q` — **12 passed**
- [x] UI: `pytest tests/boundary -q` — **6 passed**
- [x] 전체: `pytest -q` — **18 passed**
- [x] Golden Master: `golden/u_cli_01~05/` (output.txt + approval.yaml)
- [x] REFACTOR — control/boundary 구조 개선 · GUI 숫자 포맷 · 문서 동기화

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
├── UnitConverter.py              # CLI — boundary thin wrapper → src/boundary/cli
├── UnitConverterGUI.py           # GUI — PyQt6 → src/boundary/qt_app
├── README.md
├── .cursorrules                  # ECB · Dual-Track · TDD 정책
├── pyproject.toml                # pytest testpaths · pythonpath=src
├── docs/
│   ├── PRD.md
│   ├── Report/
│   │   ├── 1. mom-test-report.md
│   │   ├── 2. ProblemDefinition_Report.md
│   │   ├── 3. AI-Layer-Setup_Report.md
│   │   ├── 4. UnitConverter_RED_Design_Report.md
│   │   ├── 5. UnitConverter_RED_Skeleton_Report.md
│   │   ├── 6. UnitConverter_Logic_RED_Complete_Report.md
│   │   ├── 7. UnitConverter_GREEN_Complete_Report.md
│   │   ├── 8. UnitConverter_Progress_Summary_Report.md   # GREEN 시점 SSOT
│   │   ├── 9. UnitConverter_PostGREEN_GUI_Report.md    # Post-GREEN · GUI
│   │   └── 10. UnitConverter_REFACTOR_Complete_Report.md  # REFACTOR · 최신 SSOT
│   └── Prompt/
│       ├── 1. mom-test-transcript.md
│       ├── 2. ProblemDefinition-transcript.md
│       ├── 3. AI-Layer-Setup-transcript.md
│       ├── 4. UnitConverter_RED_Design-Transcript.md
│       ├── 5. UnitConverter_RED_Skeleton-Transcript.md
│       ├── 6. UnitConverter_Logic_RED_Complete-Transcript.md
│       ├── 7. UnitConverter_GREEN_Complete-Transcript.md
│       ├── 8. UnitConverter_Progress_Export-Transcript.md
│       ├── 9. UnitConverter_PostGREEN_GUI-Transcript.md
│       └── 10. UnitConverter_REFACTOR_Complete-Transcript.md
├── src/
│   ├── entity/                   # 변환·비율 (순수 로직)
│   ├── control/                  # 파싱·유스케이스
│   └── boundary/                 # cli.py · qt_app.py (GUI)
├── tests/
│   ├── conftest.py               # G1·검증·확장 픽스처 (데이터만)
│   ├── entity/                   # test_d_conv_*.py, test_d_val_*.py, test_d_ext_*.py
│   ├── control/
│   └── boundary/                 # test_u_cli_01.py · test_u_cli_rejections.py · golden_loader.py
├── golden/                       # UI Golden Master SSOT · approval.yaml
│   ├── manifest.yaml
│   └── u_cli_*/output.txt
└── .cursor/
    ├── commands/                 # tdd-red.md, review-ecb.md
    ├── hooks/                    # pytest 자동 실행·스냅샷 차단
    └── skills/unit-conversion-tdd/
        ├── SKILL.md
        └── reference.md          # D-* ID SSOT
```

---

## Setup & Run

### 1. 가상환경(venv) 만들기 (최초 1회)

```bash
# 프로젝트 루트에서
cd UnitConverter_28

python -m venv venv
```

### 2. 가상환경 활성화

```bash
# Windows (PowerShell / CMD)
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

프롬프트 앞에 `(venv)`가 보이면 활성화된 상태입니다.

### 3. 패키지 설치 (최초 1회 · venv 활성화 후)

```bash
pip install -r requirements.txt
```

회사망 등에서 SSL 오류가 나면:

```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

또는 개별 설치:

```bash
pip install pytest PyQt6
```

### 4. 실행

```bash
# CLI (터미널)
python UnitConverter.py
# 예: meter:2.5 입력 → feet, yard 변환 결과 출력

# GUI (PyQt6)
python UnitConverterGUI.py
```

### 5. 테스트

```bash
pytest tests/entity -q
pytest tests/control -q
pytest tests/boundary -q
pytest -q          # 전체 (GREEN: 18 passed)
```

### 6. 가상환경 종료

```bash
deactivate
```

### GUI 사용법

1. **값** 입력란에 숫자 입력 (예: `2.5`)
2. **단위** 드롭다운에서 `meter` / `feet` / `yard` 선택
3. **변환** 클릭 (또는 Enter) → 입력 단위를 제외한 변환 결과 표시
4. 잘못된 값(음수, 숫자 아님 등)은 CLI와 동일한 검증 메시지로 표시

> GUI는 `boundary/cli.process(..., format_numbers=True)`를 재사용하므로 변환·검증 로직은 CLI와 동일합니다.  
> **표시 포맷:** GUI만 최대 소수 5자리·끝 0 제거 (예: `0.762 meter`). CLI Golden Master 출력은 변경 없음.

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
- **KPT 회고** (Keep · Problem · Try)

#### Keep

- **프롬프트를 AI가 이해하기 쉽게 작성** — Phase/Layer/Track 선언, 슬래시 커맨드(`/red-test-plan`, `/green-minimal`, `/refactor-smell`), 제약 조건(`코드 수정 금지`, `tests/`만 변경, Golden Master 불변)을 명시했다.
- **구성·조건으로 범위를 좁힘** — 세션 10 P0 리팩토링처럼 `대상` / `방법` / `Budget`(파일·클래스·메서드 상한)을 주면 public API 유지와 회귀 테스트 통과가 안정적이었다.
- **명확한 지시사항 확립립** — 세션 3의 `.cursorrules`, Skill, Hook, `reference.md` 덕분에 이후 짧은 지시(`/green-minimal`, RED test 파일 생성 등)도 일관된 결과를 냈다.
- **Ask 모드 + “수정 없음” 검토** — `/refactor-smell`, Green phase 점검처럼 구현 전·후 점검을 분리한 패턴이 효과적이었다.
- **Report/Prompt Export** — 10개 세션 Transcript로 PR·회고·다음 프롬프트 작성 시 맥락을 유지했다.
- **All pytest 패스 조건 + Golden Master 불변** — REFACTOR·GUI 변경 시에도 회귀 기준이 명확해 자신감 있게 구조를 개선할 수 있었다.

#### Problem

- **간단한 프롬프트만으로도 AI가 답을 내주니, 더 구체적인 프롬프트 작성 연습이 어렵다** — 다만 짧은 지시가 통한 것은 Rule·Skill·SSOT 인프라가 이미 깔려 있었기 때문이다. 인프라 없이 같은 수준의 지시를 쓰면 결과가 달라질 수 있다.
- **TDD·ECB·Dual-Track·Golden Master 이해가 깊을수록 더 좋은 프롬프트를 쓸 수 있다** — `D-LOC-*` → `D-CONV-*` naming drift, `convert_all` vs `convert_excluding_input` 혼동, Golden Master는 boundary만 해당 등 개념을 모르면 계약·레이어를 어기기 쉽다.
- **AI 작성 문서 완성도가 높아 헛점을 찾으려면 꼼꼼한 교차 검증이 필요하다** — `validate_numeric` dead code, 예외 이원화, FR-3↔D-CONV-04 C2C 모호함, README 반올림(8.2) vs 테스트 SSOT(8.2021) 불일치, PRD/Prompt drift 등은 Ask 검토에서야 드러났다.
- **프로젝트 고유 규칙은 AI가 스스로 추론하지 못하는 경우가 있다** — PR base `green` 지정, `Prompting/` → `Prompt/` 폴더 정정처럼 팀 Ground Rule을 프롬프트에 넣지 않으면 후속 수정이 반복된다.
- **문서 양이 많아질수록(Report 1~10) 교차 검증 피로가 커진다.**

#### Try

- **나만의 direction이 담긴 프롬프트 표준화** — 실습 프롬프트 발췌·“만들어줘” 수준에서, 세션 10처럼 `대상` / `방법` / `Budget` / `게이트` 템플릿을 모든 Agent 작업에 기본 적용한다. (예: GUI 숫자 포맷 — “끝 0 제거, 최대 5자리” + “CLI Golden Master 불변”)
- **팀 Ground Rule을 알려주고 PR 생성** — phase별 base 브랜치(`red` → `green` → `refactoring`), PR 본문(Summary / Test plan / `pytest -q` 결과 / Report 링크), Golden Master·assert 완화·skip 금지(`.cursorrules` 인용), 변경 범위·Budget 명시.
- **Phase 종료마다 “Ask 검토 → Agent 수정” 2단계 루틴 고정** — GREEN·REFACTOR 직후 “수정 없이 전체 점검” 프롬프트를 템플릿화한다.
- **프롬프트에 SSOT 참조를 항상 포함** — `reference.md`, `PRD.md`, `golden/manifest.yaml` 확인 후 작업을 시작한다.
- **설계 의견을 프롬프트에 명시** — “왜 이 레이어에 둘지”, “어떤 계약을 유지할지”, “무엇은 건드리지 않을지”를 한 줄이라도 적는 연습.

> **한 줄 요약:** Rule·Skill·Hook으로 범위를 좁히고 짧은 프롬프트도 통하게 만들었지만, 문서·계약·SSOT 검증은 여전히 내가 깊이 이해하고 꼼꼼히 봐야 했다. 다음에는 **대상/방법/Budget/게이트** 프롬프트와 **팀 PR Ground Rule**을 표준으로 쓴다.

---

## 다음 단계

1. **(선택)** `validate_numeric` ↔ `parse_input` 역할 정리·연결
2. **(선택)** U-GUI-* Golden Master · GUI Track 테스트 ID
3. **(선택)** feet/yard 입력 Golden Master · cubit CLI/GUI (FR-9)

---

## References

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](./docs/PRD.md) | **SSOT** — FR/SC/Loop/TDD |
| [.cursorrules](./.cursorrules) | ECB · Dual-Track · TDD 게이트 |
| [reference.md](./.cursor/skills/unit-conversion-tdd/reference.md) | **D-* / U-* 테스트 ID** |
| [Report/10. UnitConverter_REFACTOR_Complete_Report.md](./docs/Report/10.%20UnitConverter_REFACTOR_Complete_Report.md) | **REFACTOR 완료 · 최신 SSOT** |
| [Report/3. AI-Layer-Setup_Report.md](./docs/Report/3.%20AI-Layer-Setup_Report.md) | Harness · Hook · 8계층 |
| [Report/4. UnitConverter_RED_Design_Report.md](./docs/Report/4.%20UnitConverter_RED_Design_Report.md) | RED 설계 · C2C · G1 격자 |
| [Report/5. UnitConverter_RED_Skeleton_Report.md](./docs/Report/5.%20UnitConverter_RED_Skeleton_Report.md) | RED 스켈레톤 · D-CONV-01 FAIL |
| [Report/6. UnitConverter_Logic_RED_Complete_Report.md](./docs/Report/6.%20UnitConverter_Logic_RED_Complete_Report.md) | Logic RED 12건 완료 |
| [Report/7. UnitConverter_GREEN_Complete_Report.md](./docs/Report/7.%20UnitConverter_GREEN_Complete_Report.md) | GREEN · Golden Master · convert_all 정리 |
| [Report/8. UnitConverter_Progress_Summary_Report.md](./docs/Report/8.%20UnitConverter_Progress_Summary_Report.md) | GREEN 시점 누적 SSOT |
| [Report/9. UnitConverter_PostGREEN_GUI_Report.md](./docs/Report/9.%20UnitConverter_PostGREEN_GUI_Report.md) | Post-GREEN · GUI · venv · docs/golden 정리 |
| [Prompt/10. UnitConverter_REFACTOR_Complete-Transcript.md](./docs/Prompt/10.%20UnitConverter_REFACTOR_Complete-Transcript.md) | 세션 10 REFACTOR Transcript |
| [Prompt/4. UnitConverter_RED_Design-Transcript.md](./docs/Prompt/4.%20UnitConverter_RED_Design-Transcript.md) | 세션 4 Transcript |
| [Prompt/5. UnitConverter_RED_Skeleton-Transcript.md](./docs/Prompt/5.%20UnitConverter_RED_Skeleton-Transcript.md) | 세션 5 Transcript |
| [Prompt/6. UnitConverter_Logic_RED_Complete-Transcript.md](./docs/Prompt/6.%20UnitConverter_Logic_RED_Complete-Transcript.md) | 세션 6 Transcript |
| [Prompt/7. UnitConverter_GREEN_Complete-Transcript.md](./docs/Prompt/7.%20UnitConverter_GREEN_Complete-Transcript.md) | 세션 7 GREEN Transcript |
| [Prompt/8. UnitConverter_Progress_Export-Transcript.md](./docs/Prompt/8.%20UnitConverter_Progress_Export-Transcript.md) | 세션 8 Export Transcript |
| [Prompt/9. UnitConverter_PostGREEN_GUI-Transcript.md](./docs/Prompt/9.%20UnitConverter_PostGREEN_GUI-Transcript.md) | 세션 9 GUI · venv Transcript |
| [Mom Test Report](./docs/Report/1.%20mom-test-report.md) | 인터뷰 증거 |
| [Problem Definition Report](./docs/Report/2.%20ProblemDefinition_Report.md) | R-G-I-O · SC1~3 |