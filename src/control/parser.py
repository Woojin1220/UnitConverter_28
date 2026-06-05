from control.exceptions import ParseError


def parse_input(raw: str) -> tuple[str, float]:
    if ":" not in raw:
        raise ParseError(f"Invalid format. Use unit:value (ex: meter:2.5): {raw}")
    unit, value_str = raw.split(":", 1)
    try:
        value = float(value_str)
    except ValueError as exc:
        raise ParseError(f"Invalid number: {value_str}") from exc
    return unit, value
