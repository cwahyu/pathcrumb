# tests/test_cli.py

from typer.testing import CliRunner

from pathcrumb.cli import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Keep Python file headers" in result.output


def test_fix_adds_header(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("print('hello')\n")

    result = runner.invoke(app, ["fix", str(tmp_path)])

    assert result.exit_code == 0
    assert "Added headers: 1" in result.output


def test_fix_check_mode(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("print('hello')\n")

    result = runner.invoke(app, ["fix", str(tmp_path), "--check"])

    assert result.exit_code == 1


def test_check_missing(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("print('hello')\n")

    result = runner.invoke(app, ["check", str(tmp_path)])

    assert result.exit_code == 0
    assert "missing header" in result.output.lower()


def test_check_fail_on_missing(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("print('hello')\n")

    result = runner.invoke(
        app,
        ["check", str(tmp_path), "--fail-on-missing"],
    )

    assert result.exit_code == 1


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "pathcrumb" in result.output


def test_init_creates_config(tmp_path, monkeypatch):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[project]\nname='x'\nversion='0.1.0'\n")

    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    content = pyproject.read_text()

    assert "[tool.pathcrumb]" in content


def test_init_already_exists(tmp_path, monkeypatch):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[project]\nname='x'\nversion='0.1.0'\n\n[tool.pathcrumb]\n")

    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    assert "already exists" in result.output


def test_fix_no_changes(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("# example.py\n\nprint('hello')\n")

    result = runner.invoke(app, ["fix", str(tmp_path)])

    assert "No header changes needed" in result.output
