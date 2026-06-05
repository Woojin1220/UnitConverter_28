"""U-CLI-02~05 — FR-4: 거부 케이스 Golden Master."""

import pytest

from boundary.cli import run

from tests.boundary.conftest import load_golden_master
from tests.conftest import CUBIT_INPUT, INVALID_INPUT_NO_COLON, INVALID_NUMBER_INPUT


@pytest.mark.parametrize(
    ("golden_name", "raw_input"),
    [
        ("u_cli_02_invalid_format", INVALID_INPUT_NO_COLON),
        ("u_cli_03_invalid_number", INVALID_NUMBER_INPUT),
        ("u_cli_04_unknown_unit", CUBIT_INPUT),
        ("u_cli_05_negative_value", "meter:-1"),
    ],
    ids=["U-CLI-02", "U-CLI-03", "U-CLI-04", "U-CLI-05"],
)
def test_u_cli_rejection_golden_master(golden_name, raw_input):
    # Given: 거부 대상 입력 (manifest input과 동일)
    # When: CLI 처리
    # Then: Golden Master 거부 메시지
    assert run(raw_input) == load_golden_master(golden_name)
