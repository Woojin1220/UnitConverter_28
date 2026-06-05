"""Shared pytest fixtures — conversion grid data only (no domain logic)."""

import pytest

# G1 SSOT (GREEN 시 entity.constants.py로 이전 예정)
G1_METER_VALUE = 2.5
METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361
G1_METER_TO_FEET_EXPECTED = G1_METER_VALUE * METER_TO_FEET  # 8.2021


@pytest.fixture
def g1_meter_value():
    """G1 anchor — 2.5 meter."""
    return G1_METER_VALUE


@pytest.fixture
def g1_meter_to_feet():
    """G1 — D-LOC-01: (value, from_unit, to_unit, expected)."""
    return (G1_METER_VALUE, "meter", "feet", G1_METER_TO_FEET_EXPECTED)
