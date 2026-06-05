"""U-CLI-04 — FR-4: 미등록 단위 Golden Master."""

from boundary.cli import run

from tests.boundary.conftest import load_golden_master


def test_u_cli_04_unknown_unit(cubit_input):
    # Given: "cubit:2" (등록 전)
    # When: CLI 처리
    # Then: Golden Master 거부 메시지
    assert run(cubit_input) == load_golden_master("u_cli_04_unknown_unit")
