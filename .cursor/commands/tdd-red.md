# TDD RED — 실패 테스트 먼저

Dual-Track TDD의 RED 단계만 수행한다. `.cursorrules`와 `reference.md`의 D-* ID를 따른다.

## 필수 선언

응답 **첫 줄**에 반드시 선언한다:

```
Phase: RED | Layer: entity | control | boundary | Track: Logic (D-*) | UI (U-*)
```

이어서 이번에 다룰 **테스트 ID 한 개**를 명시한다 (예: `D-CONV-01`).

## 절차

1. **ID 확인** — `reference.md` 또는 사용자 지정 ID와 Layer·Track이 일치하는지 확인한다.
2. **선행 게이트**
   - `control` RED → `pytest tests/entity -q` 통과 상태 확인
   - `boundary` UI RED → 해당 Logic Layer GREEN 확인 후 진행
3. **파일 배치** — Logic: `tests/entity/test_d_*.py` 또는 `tests/control/test_d_*.py` / UI: `tests/boundary/test_u_*.py`
4. **AAA 테스트 작성**
   - **Arrange** — 입력·픽스처 준비 (Logic Track: mock 없이 실제 import)
   - **Act** — 아직 없거나 미구현인 `src/` API 호출
   - **Assert** — 구체적 기대값·예외·출력 문자열 명시
   - 테스트 함수 docstring 또는 주석에 ID 기록
5. **pytest FAIL** — Layer 디렉터리에서 실행, exit ≠ 0 및 **의도한 실패**인지 확인한다.
6. **범위 고정** — RED 완료까지 `src/` 및 `UnitConverter.py`는 수정하지 않는다.

## pytest 예시

```bash
# entity Logic RED
pytest tests/entity -q

# control Logic RED (entity 통과 후)
pytest tests/control -q

# boundary UI RED (Logic GREEN 후)
pytest tests/boundary -q

# 실패 1건만 빠르게 확인
pytest tests/entity/test_d_conversion.py::test_d_conv_01 -q
```

기대: `FAILED` 또는 `ERROR`, exit code ≠ 0. `passed`이면 assert가 약하거나 구현이 이미 있는 것 — RED 실패로 재검토한다.

## 보고

RED 완료 시 아래만 간결히 보고한다:

| 항목 | 내용 |
|------|------|
| 테스트 ID | `D-*` 또는 `U-*` |
| FAIL 요약 | 실패 테스트명·assert 메시지 한 줄 |
| 변경 파일 | `tests/` 하위 경로만 (예: `tests/entity/test_d_conversion.py`) |
| pytest | 실행 명령 + exit code |
| 다음 | GREEN 대기 (src/ 수정은 GREEN에서) |

## 금지

- `src/`, `UnitConverter.py` **수정**
- Logic Track에서 **Domain Mock** (`unittest.mock`, `pytest` mock, `monkeypatch`로 entity·control 패치)
- UI Track에서 **entity 직접 mock**
- **assert 완화** (느슨한 조건, `pytest.approx` 임의 완화, 조건 삭제)
- `@pytest.mark.skip`, `xfail`, `pass`로 실패 우회
- 테스트 없이 구현 선행
- 한 RED에서 여러 Layer·여러 ID 동시 진행
