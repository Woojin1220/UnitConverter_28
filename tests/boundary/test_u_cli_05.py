"""U-CLI-05 — FR-4: 음수 값 Golden Master."""

from boundary.cli import run

from tests.boundary.conftest import load_golden_master


def test_u_cli_05_negative_value():
    # Given: "meter:-1"
    # When: CLI 처리
    # Then: Golden Master 거부 메시지
    assert run("meter:-1") == load_golden_master("u_cli_05_negative_value")
