from typer.testing import CliRunner
from pathcrumb.cli import app

runner = CliRunner()


def test_cli_runs():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
