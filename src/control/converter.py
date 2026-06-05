from entity.conversion import convert_length
from entity.exceptions import ValidationError as EntityValidationError
from entity.registry import get_registered_units
from entity.validation import validate_unit, validate_value

from control.exceptions import ValidationError
from control.parser import parse_input


def _convert_units(
    unit: str, value: float, *, exclude_input: bool = False
) -> dict[str, float]:
    validate_value(value)
    validate_unit(unit)
    return {
        target: convert_length(value, unit, target)
        for target in get_registered_units()
        if not exclude_input or target != unit
    }


def convert_all(raw: str) -> dict[str, float]:
    unit, value = parse_input(raw)
    return _convert_units(unit, value)


def convert_excluding_input(raw: str) -> dict[str, float]:
    unit, value = parse_input(raw)
    return _convert_units(unit, value, exclude_input=True)


def run_conversion(raw: str) -> tuple[float, str, dict[str, float]]:
    try:
        unit, value = parse_input(raw)
        conversions = _convert_units(unit, value, exclude_input=True)
    except EntityValidationError as exc:
        raise ValidationError(str(exc)) from exc
    return value, unit, conversions


def supported_units() -> list[str]:
    return sorted(get_registered_units().keys())
