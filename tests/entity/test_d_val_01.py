"""D-VAL-01 — FR-4: 음수 값 거부."""

import pytest


def test_d_val_01_rejects_negative_value(negative_value):
    # Given: 음수 값 -1.0
    # When: validate_value(negative_value) 호출
    # Then: 거부 (예외 또는 ValidationError)
    pytest.fail("RED: D-VAL-01 — 구현 없음, 의도적 실패")
