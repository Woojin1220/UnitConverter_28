"""CLI boundary — stdin/stdout formatting (control only)."""

from dataclasses import dataclass

from control.converter import run_conversion
from control.exceptions import ParseError, ValidationError

PROMPT = "Insert value for converting (ex: meter:2.5): "
MAX_DISPLAY_DECIMALS = 5


@dataclass(frozen=True)
class ProcessResult:
    ok: bool
    lines: list[str]


def format_number(value: float, max_decimals: int = MAX_DISPLAY_DECIMALS) -> str:
    text = f"{value:.{max_decimals}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _conversion_line(
    value: float,
    unit: str,
    converted: float,
    target: str,
    *,
    format_numbers: bool,
) -> str:
    if format_numbers:
        value_text = format_number(value)
        converted_text = format_number(converted)
    else:
        value_text = value
        converted_text = converted
    return f"{value_text} {unit} = {converted_text} {target}"


def _user_message(exc: Exception) -> str:
    if isinstance(exc, ParseError):
        message = str(exc)
        if "Invalid format" in message:
            return "Invalid format. Use unit:value (ex: meter:2.5)"
        return message
    if isinstance(exc, ValidationError):
        return str(exc)
    raise exc


def process(raw: str, *, format_numbers: bool = False) -> ProcessResult:
    try:
        value, unit, conversions = run_conversion(raw)
    except (ParseError, ValidationError) as exc:
        return ProcessResult(ok=False, lines=[_user_message(exc)])
    return ProcessResult(
        ok=True,
        lines=[
            _conversion_line(value, unit, converted, target, format_numbers=format_numbers)
            for target, converted in conversions.items()
        ],
    )


def run(raw: str) -> str:
    result = process(raw)
    if not result.lines:
        return ""
    return "\n".join(result.lines) + "\n"


def main() -> None:
    raw = input(PROMPT)
    for line in process(raw).lines:
        print(line)
