"""D-CONV-04 — FR-3: 단일 입력 → 전 단위 변환 결과."""

from control.converter import convert_all


def test_d_conv_04_single_input_all_units(valid_input, g1_all_conversions):
    # Given: "meter:2.5"
    # When: convert_all(valid_input) 호출
    # Then: {"meter": 2.5, "feet": 8.2021, "yard": 2.734025} (등록 전 단위)
    assert convert_all(valid_input) == g1_all_conversions
