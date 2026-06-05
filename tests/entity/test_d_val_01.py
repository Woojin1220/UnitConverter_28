"""D-VAL-01 — FR-4: 음수 값 거부."""

import pytest

from entity.exceptions import ValidationError
from entity.validation import validate_value


def test_d_val_01_rejects_negative_value(negative_value):
    # Given: 음수 값 -1.0
    # When: validate_value(negative_value) 호출
    # Then: 거부 (예외 또는 ValidationError)
    with pytest.raises(ValidationError):
        validate_value(negative_value)
