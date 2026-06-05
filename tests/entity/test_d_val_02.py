"""D-VAL-02 — FR-4: 잘못된 숫자 거부 (entity — 값 부분)."""

import pytest


def test_d_val_02_rejects_invalid_number(invalid_value_str):
    # Given: 값 부분 "abc" (숫자로 변환 불가)
    # When: validate_numeric(invalid_value_str) 호출
    # Then: 거부 (예외 또는 ValidationError)
    pytest.fail("RED: D-VAL-02 — 구현 없음, 의도적 실패")
