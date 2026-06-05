"""Shared pytest fixtures — test data only (no domain logic)."""

import pytest

# --- G1 변환 격자 (Loop 1 entity) ---
G1_METER_VALUE = 2.5
METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361
G1_METER_TO_FEET_EXPECTED = G1_METER_VALUE * METER_TO_FEET  # 8.2021
G1_METER_TO_YARD_EXPECTED = G1_METER_VALUE * METER_TO_YARD  # 2.734025
G1_FEET_TO_YARD_VALUE = G1_METER_TO_FEET_EXPECTED
G1_FEET_TO_YARD_EXPECTED = G1_METER_TO_YARD_EXPECTED

# --- 입력 검증 (Loop 2) ---
VALID_INPUT = "meter:2.5"
INVALID_INPUT_NO_COLON = "meter2.5"
INVALID_NUMBER_INPUT = "meter:abc"  # control 파싱 실패 (D-VAL-04/05와 구분)
INVALID_VALUE_STR = "abc"  # entity 값 부분 검증 (D-VAL-02)
NEGATIVE_VALUE = -1.0
UNKNOWN_UNIT = "cubit"
PARSED_METER = ("meter", 2.5)

# --- 확장성 (Loop 3) ---
CUBIT_TO_METER = 0.4572
CUBIT_VALUE = 2.0
CUBIT_INPUT = f"cubit:{CUBIT_VALUE}"
CUBIT_IN_METERS = CUBIT_VALUE * CUBIT_TO_METER  # 0.9144

# --- control 변환 기대 (meter:2.5 입력) ---
G1_ALL_CONVERSIONS = {
    "feet": G1_METER_TO_FEET_EXPECTED,
    "yard": G1_METER_TO_YARD_EXPECTED,
}
# D-CONV-05: meter 키 없음 (feet·yard만)
G1_EXCLUDED_INPUT_CONVERSIONS = dict(G1_ALL_CONVERSIONS)


@pytest.fixture
def g1_meter_value():
    """G1 anchor — 2.5 meter."""
    return G1_METER_VALUE


@pytest.fixture
def g1_meter_to_feet():
    """G1 — D-CONV-01: (value, from_unit, to_unit, expected)."""
    return (G1_METER_VALUE, "meter", "feet", G1_METER_TO_FEET_EXPECTED)


@pytest.fixture
def g1_meter_to_yard():
    """G1 — D-CONV-02: (value, from_unit, to_unit, expected)."""
    return (G1_METER_VALUE, "meter", "yard", G1_METER_TO_YARD_EXPECTED)


@pytest.fixture
def g1_feet_to_yard():
    """G1 — D-CONV-03: (value, from_unit, to_unit, expected)."""
    return (G1_FEET_TO_YARD_VALUE, "feet", "yard", G1_FEET_TO_YARD_EXPECTED)


@pytest.fixture
def valid_input():
    """D-CONV-04/05, D-VAL-05 — 유효 `단위:값` 문자열."""
    return VALID_INPUT


@pytest.fixture
def invalid_input_no_colon():
    """D-VAL-04 — 콜론 없는 형식."""
    return INVALID_INPUT_NO_COLON


@pytest.fixture
def invalid_number_input():
    """control — `meter:abc` 전체 입력 (파싱 단계)."""
    return INVALID_NUMBER_INPUT


@pytest.fixture
def invalid_value_str():
    """D-VAL-02 — 값 부분 `"abc"` (entity 숫자 검증)."""
    return INVALID_VALUE_STR


@pytest.fixture
def negative_value():
    """D-VAL-01 — 음수 값."""
    return NEGATIVE_VALUE


@pytest.fixture
def unknown_unit():
    """D-VAL-03 — 미등록 단위."""
    return UNKNOWN_UNIT


@pytest.fixture
def parsed_meter():
    """D-VAL-05 — 파싱 기대 (unit, value)."""
    return PARSED_METER


@pytest.fixture
def g1_all_conversions():
    """D-CONV-04 — meter:2.5 → 전 단위 변환 결과."""
    return G1_ALL_CONVERSIONS


@pytest.fixture
def g1_excluded_input_conversions():
    """D-CONV-05 — meter:2.5, 입력 단위 제외."""
    return G1_EXCLUDED_INPUT_CONVERSIONS


@pytest.fixture
def cubit_registration():
    """D-EXT-01~02 — cubit 등록 (1 cubit = 0.4572 meter)."""
    return ("cubit", CUBIT_TO_METER)


@pytest.fixture
def cubit_input():
    """D-EXT-01 — cubit:2 입력."""
    return CUBIT_INPUT
