"""D-CONV-05 — FR-3: 입력 단위 제외 출력 목록."""

from control.converter import convert_excluding_input


def test_d_conv_05_excludes_input_unit(valid_input, g1_excluded_input_conversions):
    # Given: "meter:2.5"
    # When: convert_excluding_input(valid_input) 호출
    # Then: feet·yard만 포함, meter 제외
    assert convert_excluding_input(valid_input) == g1_excluded_input_conversions
