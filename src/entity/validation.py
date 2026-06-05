from entity.exceptions import ValidationError
from entity.registry import get_registered_units


def validate_value(value: float) -> None:
    if value < 0:
        raise ValidationError(f"Negative value not allowed: {value}")


def validate_numeric(value_str: str) -> None:
    try:
        float(value_str)
    except ValueError as exc:
        raise ValidationError(f"Invalid number: {value_str}") from exc


def validate_unit(unit: str) -> None:
    if unit not in get_registered_units():
        raise ValidationError(f"Unknown unit: {unit}")
