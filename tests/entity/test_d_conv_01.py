"""D-CONV-01~03 — FR-2: convert_length (G1 변환 격자)."""

from entity.conversion import convert_length


def test_d_conv_01_meter_to_feet(g1_meter_to_feet):
    # Given: G1 — 2.5 meter (g1_meter_to_feet 픽스처)
    # When: convert_length(2.5, "meter", "feet") 호출
    # Then: 8.2021 feet 반환 (2.5 × 3.28084)
    value, from_unit, to_unit, expected = g1_meter_to_feet
    assert convert_length(value, from_unit, to_unit) == expected


def test_d_conv_02_meter_to_yard(g1_meter_to_yard):
    # Given: G1 — 2.5 meter (g1_meter_to_yard 픽스처)
    # When: convert_length(2.5, "meter", "yard") 호출
    # Then: 2.734025 yard 반환 (2.5 × 1.09361)
    value, from_unit, to_unit, expected = g1_meter_to_yard
    assert convert_length(value, from_unit, to_unit) == expected


def test_d_conv_03_feet_to_yard(g1_feet_to_yard):
    # Given: G1 — 8.2021 feet (g1_feet_to_yard 픽스처, D-CONV-01 결과 재사용)
    # When: convert_length(8.2021, "feet", "yard") 호출
    # Then: 2.734025 yard 반환 (meter 경유, D-CONV-02와 일치)
    value, from_unit, to_unit, expected = g1_feet_to_yard
    assert convert_length(value, from_unit, to_unit) == expected
