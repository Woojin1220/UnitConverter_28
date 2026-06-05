"""D-VAL-04 — FR-4: 콜론 없는 형식 거부."""

import pytest


def test_d_val_04_rejects_missing_colon(invalid_input_no_colon):
    # Given: "meter2.5" (콜론 없음)
    # When: parse_input(invalid_input_no_colon) 호출
    # Then: 거부 (예외 또는 ParseError)
    pytest.fail("RED: D-VAL-04 — 구현 없음, 의도적 실패")
