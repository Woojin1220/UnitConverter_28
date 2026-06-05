"""U-CLI-02 — FR-4: 콜론 없는 형식 Golden Master."""

from boundary.cli import run

from tests.boundary.conftest import load_golden_master


def test_u_cli_02_invalid_format(invalid_input_no_colon):
    # Given: "meter2.5"
    # When: CLI 처리
    # Then: Golden Master 거부 메시지
    assert run(invalid_input_no_colon) == load_golden_master("u_cli_02_invalid_format")
