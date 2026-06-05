"""D-VAL-03 — FR-4: 미등록 단위 거부."""

import pytest

from entity.exceptions import ValidationError
from entity.validation import validate_unit


def test_d_val_03_rejects_unknown_unit(unknown_unit):
    # Given: 미등록 단위 "cubit" (등록 전)
    # When: validate_unit(unknown_unit) 호출
    # Then: 거부 (예외 또는 ValidationError)
    with pytest.raises(ValidationError):
        validate_unit(unknown_unit)
