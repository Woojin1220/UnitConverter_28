"""CLI boundary — stdin/stdout formatting (control only)."""

from control.converter import run_conversion
from control.exceptions import ParseError, ValidationError

PROMPT = "Insert value for converting (ex: meter:2.5): "


def _user_message(exc: Exception) -> str:
    if isinstance(exc, ParseError):
        message = str(exc)
        if "Invalid format" in message:
            return "Invalid format. Use unit:value (ex: meter:2.5)"
        return message
    if isinstance(exc, ValidationError):
        return str(exc)
    raise exc


def process(raw: str) -> list[str]:
    try:
        value, unit, conversions = run_conversion(raw)
    except (ParseError, ValidationError) as exc:
        return [_user_message(exc)]
    return [f"{value} {unit} = {converted} {target}" for target, converted in conversions.items()]


def run(raw: str) -> str:
    lines = process(raw)
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


def main() -> None:
    raw = input(PROMPT)
    for line in process(raw):
        print(line)
