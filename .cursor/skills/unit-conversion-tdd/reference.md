# D-* 테스트 ID (Logic Track)

> PRD C2C: [`docs/PRD.md`](../../../docs/PRD.md) · 테스트 파일: `tests/entity/test_d_*.py`, `tests/control/test_d_*.py`

## Loop 1 — 변환 정확성 (SC1, SC3)

| ID | Layer | 파일 | 함수 (RED) | 대상 API | 요약 |
|----|-------|------|------------|----------|------|
| D-CONV-01 | entity | `test_d_conv_01.py` | `test_d_conv_01_meter_to_feet` | `convert_length()` | meter → feet |
| D-CONV-02 | entity | `test_d_conv_01.py` | `test_d_conv_02_meter_to_yard` | `convert_length()` | meter → yard |
| D-CONV-03 | entity | `test_d_conv_01.py` | `test_d_conv_03_feet_to_yard` | `convert_length()` | feet → yard (meter 경유) |
| D-CONV-04 | control | `test_d_conv_04.py` | `test_d_conv_04_single_input_all_units` | `convert_all()` | 단일 입력 → 전 단위 변환 결과 |
| D-CONV-05 | control | `test_d_conv_05.py` | `test_d_conv_05_excludes_input_unit` | `convert_excluding_input()` | 입력 단위 제외 목록 |

## Loop 2 — 입력 검증 (SC3)

| ID | Layer | 파일 | 함수 (RED) | 대상 API | 요약 |
|----|-------|------|------------|----------|------|
| D-VAL-01 | entity | `test_d_val_01.py` | `test_d_val_01_rejects_negative_value` | `validate_value()` | 음수 값 거부 |
| D-VAL-02 | entity | `test_d_val_02.py` | `test_d_val_02_rejects_invalid_number` | `validate_numeric()` | 값 부분 숫자 아님 거부 (`"abc"`) |
| D-VAL-03 | entity | `test_d_val_03.py` | `test_d_val_03_rejects_unknown_unit` | `validate_unit()` | 미등록 단위 거부 |
| D-VAL-04 | control | `test_d_val_04.py` | `test_d_val_04_rejects_missing_colon` | `parse_input()` | 콜론 없는 형식 거부 |
| D-VAL-05 | control | `test_d_val_05.py` | `test_d_val_05_parses_unit_value` | `parse_input()` | `단위:값` 파싱 성공 |

## Loop 3 — 확장성 (SC2)

| ID | Layer | 파일 | 함수 (RED) | 대상 API | 요약 |
|----|-------|------|------------|----------|------|
| D-EXT-01 | entity | `test_d_ext_01.py` | `test_d_ext_01_register_and_convert_all` | `register_unit()` + `convert_length()` | cubit 등록 후 변환 |
| D-EXT-02 | entity | `test_d_ext_02.py` | `test_d_ext_02_register_without_core_change` | `register_unit()` | 등록만으로 확장 (OCP) |

## GREEN API (판단 SSOT)

| Layer | 함수 | 책임 |
|-------|------|------|
| entity | `convert_length(value, from_unit, to_unit) -> float` | 순수 변환 |
| entity | `validate_value(value) -> None` | 음수 등 값 검증 |
| entity | `validate_numeric(value_str) -> None` | 숫자 형식 검증 |
| entity | `validate_unit(unit) -> None` | 등록 단위 검증 |
| entity | `register_unit(name, to_meter_ratio) -> None` | 단위 등록 (OCP) |
| control | `parse_input(raw: str) -> tuple[str, float]` | `단위:값` 파싱 |
| control | `convert_all(raw: str) -> dict[str, float]` | 등록된 **전** 단위 변환 (입력 단위 포함) |
| control | `convert_excluding_input(raw: str) -> dict[str, float]` | 입력 단위 **제외** (boundary/CLI용) |
| control | `run_conversion(raw: str) -> tuple[float, str, dict]` | boundary용 — `convert_excluding_input`와 동일 결과 |

## UI Track — Golden Master (`tests/boundary/`)

> Logic GREEN 후 · SSOT: `golden/<case>/output.txt` + `approval.yaml`

| ID | 파일 | 함수 | 입력 | 요약 |
|----|------|------|------|------|
| U-CLI-01 | `test_u_cli_01.py` | `test_u_cli_01_meter_conversion` · `test_u_cli_01_main_stdout` | `meter:2.5` | G1 변환 출력 (SC1) · capsys |
| U-CLI-02 | `test_u_cli_02.py` | `test_u_cli_02_invalid_format` | `meter2.5` | 콜론 없음 |
| U-CLI-03 | `test_u_cli_03.py` | `test_u_cli_03_invalid_number` | `meter:abc` | 숫자 아님 |
| U-CLI-04 | `test_u_cli_04.py` | `test_u_cli_04_unknown_unit` | `cubit:2` | 미등록 단위 |
| U-CLI-05 | `test_u_cli_05.py` | `test_u_cli_05_negative_value` | `meter:-1` | 음수 거부 |
