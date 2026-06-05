"""D-VAL-02 — FR-4: 잘못된 숫자 거부 (entity — 값 부분)."""

import pytest

from entity.exceptions import ValidationError
from entity.validation import validate_numeric


def test_d_val_02_rejects_invalid_number(invalid_value_str):
    # Given: 값 부분 "abc" (숫자로 변환 불가)
    # When: validate_numeric(invalid_value_str) 호출
    # Then: 거부 (예외 또는 ValidationError)
    with pytest.raises(ValidationError):
        validate_numeric(invalid_value_str)
