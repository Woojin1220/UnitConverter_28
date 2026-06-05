"""D-VAL-05 — FR-1: `단위:값` 파싱 성공."""

from control.parser import parse_input


def test_d_val_05_parses_unit_value(valid_input, parsed_meter):
    # Given: "meter:2.5"
    # When: parse_input(valid_input) 호출
    # Then: ("meter", 2.5) 반환
    assert parse_input(valid_input) == parsed_meter
