---
name: unit-conversion-tdd
description: 프로젝트 Dual-Track TDD·ECB 개발 시 Agent가 따를 절차
---

# Unit Conversion — Dual-Track TDD Skill

`.cursorrules`의 정책을 따르며, 본 Skill은 **실행 절차**만 정의한다.

## 언제 이 Skill을 켜는가

다음 중 하나에 해당하면 본 Skill을 적용한다:

- `src/entity`, `src/control`, `src/boundary` 또는 `tests/**` 파일을 **새로 만들거나 수정**할 때
- 사용자가 TDD, RED/GREEN/REFACTOR, ECB, Dual-Track, `D-*`/`U-*` 테스트를 언급할 때
- PRD Loop 1~3(변환·검증·확장) 또는 SC1~3 구현·검증을 요청할 때
- `pytest` 결과를 보고 다음 Phase를 결정해야 할 때

**켜지 않는 경우:** README·Report·PRD 문서만 수정, Harness 골격 외 인프라만 다룰 때.

시작 시 응답 상단에 선언한다:

```
Phase: RED | GREEN | REFACTOR
Layer: entity | control | boundary
Track: Logic (D-*) | UI (U-*)
```

---

## Logic Track vs UI Track

| 항목 | Logic Track | UI Track |
|------|-------------|----------|
| 대상 Layer | `entity`, `control` | `boundary` |
| 테스트 ID | `D-*` | `U-*` |
| 파일명 | `test_d_*.py` | `test_u_*.py` |
| 위치 | `tests/entity/`, `tests/control/` | `tests/boundary/` |
| Mock | **금지** (실제 객체·함수만) | control·stdin/stdout mock **허용** |
| 검증 방식 | 예외·Result·도메인 값 assert | capsys/capfd·출력 문자열·Golden Master |
| 시작 시점 | Loop·Layer 순서의 **먼저** | 해당 Logic Layer **GREEN 후** |

---

## RED (5~7단계)

1. **범위 확인** — 이번 Layer·Track·Loop(SC/FR)와 `reference.md`의 D-* ID를 확정한다.
2. **선행 게이트** — entity 작업은 생략; control은 `pytest tests/entity -q` 통과; boundary(U-*)는 해당 Logic GREEN 확인.
3. **테스트 파일 생성** — `test_d_*.py` 또는 `test_u_*.py`에 테스트 ID를 docstring/주석으로 명시한다.
4. **실패 테스트 작성** — 아직 없는 구현을 호출하는 assert만 추가한다. Mock·skip·xfail 사용 금지.
5. **의도적 실패 확인** — `pytest tests/<layer> -q` 실행, exit ≠ 0 및 실패 메시지가 기대와 일치하는지 확인한다.
6. **범위 고정** — RED 단계에서는 `src/` 프로덕션 코드를 수정하지 않는다.
7. **전환** — 실패가 확인되면 GREEN으로 넘어간다고 보고한다.

---

## GREEN (5~7단계)

1. **최소 구현** — RED를 통과시키는 **가장 작은** 코드만 해당 Layer `src/`에 추가한다.
2. **ECB 준수** — import 방향(boundary→control→entity)과 Layer 책임을 어기지 않는다.
3. **Mock 금지 유지** — Logic Track 테스트·구현에 mock 패치를 넣지 않는다.
4. **Layer pytest** — `pytest tests/<layer> -q` 실행, 해당 Layer 전체 통과를 확인한다.
5. **범위 수호** — 요청·RED 범위 밖 기능(설정 파일·포맷 선택 등)을 추가하지 않는다.
6. **UI Track** — boundary GREEN 시 control을 mock해도 되나 entity 직접 mock은 금지한다.
7. **전환** — Layer pytest 통과 후 REFACTOR 또는 다음 Layer RED 후보를 보고한다.

---

## REFACTOR (5~7단계)

1. **동작 고정** — 테스트 assert·기대값을 변경하지 않는다 (완화·approx·삭제 금지).
2. **구조 개선** — OCP/SRP에 맞게 클래스·함수 분리, 중복 제거, 네이밍 정리한다.
3. **단위 확장 점검** — Loop 3 시 "기존 클래스 수정" 대신 "등록·설정 추가" 패턴을 우선한다.
4. **Layer pytest** — `pytest tests/<layer> -q`로 해당 Layer 회귀 없음을 확인한다.
5. **전체 Review** — `pytest -q` 전체 통과를 확인한다.
6. **Mom Test 대조** — SC1~3(즉시 출력·최소 변경·재확인 불필요)에 기여하는지 한 줄로 평가한다.
7. **다음 작업 제안** — 같은 Layer UI Track RED, 또는 다음 Layer Logic RED 중 하나만 제안한다.

---

## Test / Review Loop — pytest 실행 시점

| 시점 | 명령 | 기대 결과 |
|------|------|-----------|
| RED 직후 | `pytest tests/<layer> -q` | exit ≠ 0, 의도한 실패 1건 이상 |
| GREEN 직후 | `pytest tests/<layer> -q` | 해당 Layer 전체 통과 |
| REFACTOR 중·후 | `pytest tests/<layer> -q` | Layer 회귀 없음 |
| Phase 종료·릴리스 전 | `pytest -q` | 전체 통과 (exit 0) |
| control 시작 전 | `pytest tests/entity -q` | entity 전체 통과 |
| boundary U-* RED 전 | `pytest tests/entity tests/control -q` | Logic 전체 통과 |

**Loop 순서 (PRD §6.4):**

```
Loop 1 변환:  tests/entity D-* → tests/control D-* → (선택) tests/boundary U-*
Loop 2 검증:  tests/entity|control D-* → tests/boundary U-*
Loop 3 확장:  tests/entity D-* → tests/control D-* → tests/boundary U-*
```

Layer 작업 중에는 `-q`로 빠르게, REFACTOR·Loop 완료 시에는 반드시 `pytest -q` 전체를 돌린다.

---

## 완료 보고 항목

Phase·Layer·Track 작업을 마칠 때 아래를 포함해 보고한다:

| 항목 | 내용 |
|------|------|
| Phase / Layer / Track | 현재 완료한 상태 |
| 테스트 ID | 추가·통과한 `D-*` 또는 `U-*` 목록 |
| pytest 결과 | 실행 명령과 pass/fail 요약 |
| 변경 파일 | `src/`, `tests/` 경로 목록 |
| ECB 점검 | import 방향 위반 여부 |
| SC 대조 | SC1 / SC2 / SC3 중 이번 변경이 기여한 항목 |
| 다음 단계 | 한 가지 — RED / GREEN / REFACTOR + Layer + Track |

Golden Master·스냅샷을 변경했다면 **사용자 승인 여부**를 반드시 명시한다. SSOT: `golden/<case>/output.txt` + `approval.yaml` (인덱스: `golden/manifest.yaml`).

---

## 참고

- D-* 테스트 ID 목록: [reference.md](reference.md)
- 정책·금지 사항: 프로젝트 루트 `.cursorrules`
