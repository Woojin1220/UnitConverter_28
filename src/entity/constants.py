METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361

DEFAULT_UNITS: dict[str, float] = {
    "meter": 1.0,
    "feet": 1.0 / METER_TO_FEET,
    "yard": 1.0 / METER_TO_YARD,
}
