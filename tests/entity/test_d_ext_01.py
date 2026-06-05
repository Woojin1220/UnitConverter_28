"""D-EXT-01 — FR-5/FR-9: 새 단위 등록 후 변환 (entity)."""

from entity.constants import METER_TO_FEET, METER_TO_YARD
from entity.conversion import convert_length
from entity.registry import register_unit


def test_d_ext_01_register_and_convert_all(cubit_registration, cubit_input):
    # Given: cubit 등록 (1 cubit = 0.4572 meter), 값 2.0
    # When: register_unit("cubit", 0.4572) 후 convert_length(2, "cubit", "meter") 등
    # Then: meter·feet·yard 변환 가능 (cubit 기준)
    name, ratio = cubit_registration
    value = float(cubit_input.split(":", 1)[1])
    register_unit(name, ratio)
    in_meters = value * ratio
    assert convert_length(value, name, "meter") == in_meters
    assert convert_length(value, name, "feet") == in_meters * METER_TO_FEET
    assert convert_length(value, name, "yard") == in_meters * METER_TO_YARD
