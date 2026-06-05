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

## Project Structure

```
UnitConverter_28/
├── UnitConverter.py          # 메인 실행 파일 (스타터 코드)
├── README.md
├── docs/
│   └── PRD.md                # 제품 요구사항
├── Report/
│   ├── 1. mom-test-report.md
│   └── 2. ProblemDefinition_Report.md
└── Prompt/
    ├── 1. mom-test-transcript.md
    └── 2. ProblemDefinition-transcript.md
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

# 테스트 (구현 후)
pytest

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

## References

- [PRD](./docs/PRD.md)
- [Mom Test Report](./Report/1.%20mom-test-report.md)
- [Problem Definition Report](./Report/2.ProblemDefinition_Report.md)
