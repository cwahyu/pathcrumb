# tests/test_cli.py

from typer.testing import CliRunner

from pathcrumb.cli import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Keep Python file headers" in result.output


def test_check_no_files(tmp_path):
    result = runner.invoke(app, ["check"], catch_exceptions=False)

    assert result.exit_code in (0, 1)
