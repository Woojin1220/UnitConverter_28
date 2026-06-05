"""D-VAL-03 — FR-4: 미등록 단위 거부."""

import pytest


def test_d_val_03_rejects_unknown_unit(unknown_unit):
    # Given: 미등록 단위 "cubit" (등록 전)
    # When: validate_unit(unknown_unit) 호출
    # Then: 거부 (예외 또는 ValidationError)
    pytest.fail("RED: D-VAL-03 — 구현 없음, 의도적 실패")
