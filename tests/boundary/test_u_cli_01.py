"""U-CLI-01 — FR-3/SC1: G1 변환 Golden Master (meter:2.5)."""

from boundary.cli import PROMPT, main, run

from tests.boundary.conftest import load_golden_master


def test_u_cli_01_meter_conversion(valid_input):
    # Given: "meter:2.5"
    # When: CLI 변환 출력 (run)
    # Then: Golden Master와 일치 (입력 단위 meter 제외)
    assert run(valid_input) == load_golden_master("u_cli_01_meter_conversion")


def test_u_cli_01_main_stdout(valid_input, monkeypatch, capsys):
    # Given: "meter:2.5" stdin mock (prompt는 input()가 stdout에 기록)
    # When: main() — prompt + print
    # Then: capsys stdout = PROMPT + Golden Master 본문
    def fake_input(prompt=""):
        import sys

        sys.stdout.write(prompt)
        return valid_input

    monkeypatch.setattr("builtins.input", fake_input)
    main()
    captured = capsys.readouterr()
    assert captured.out == PROMPT + load_golden_master("u_cli_01_meter_conversion")
