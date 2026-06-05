"""U-CLI-03 — FR-4: 잘못된 숫자 Golden Master."""

from boundary.cli import run

from tests.boundary.conftest import load_golden_master


def test_u_cli_03_invalid_number(invalid_number_input):
    # Given: "meter:abc"
    # When: CLI 처리
    # Then: Golden Master 거부 메시지
    assert run(invalid_number_input) == load_golden_master("u_cli_03_invalid_number")
