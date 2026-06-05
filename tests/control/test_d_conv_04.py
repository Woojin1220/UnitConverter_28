"""D-CONV-04 — FR-3: 단일 입력 → 전 단위 변환 결과."""

import pytest


def test_d_conv_04_single_input_all_units(valid_input, g1_all_conversions):
    # Given: "meter:2.5"
    # When: convert_all(valid_input) 호출
    # Then: {"feet": 8.2021, "yard": 2.734025} (전 지원 단위)
    pytest.fail("RED: D-CONV-04 — 구현 없음, 의도적 실패")
