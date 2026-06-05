"""Boundary test helpers — Golden Master loader."""

from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def load_golden_master(name: str) -> str:
    return (FIXTURES_DIR / f"{name}.stdout").read_text(encoding="utf-8")
