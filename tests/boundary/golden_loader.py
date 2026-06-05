"""Golden Master loader — reads approved CLI output from golden/ SSOT.

UI Track (boundary) only. Logic Track tests do not use this module.
"""

from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parents[2] / "golden"


def golden_case_dir(name: str) -> Path:
    return GOLDEN_DIR / name


def load_golden_master(name: str) -> str:
    output_path = golden_case_dir(name) / "output.txt"
    if not output_path.is_file():
        raise FileNotFoundError(f"Golden Master not found: {output_path}")
    return output_path.read_text(encoding="utf-8")
