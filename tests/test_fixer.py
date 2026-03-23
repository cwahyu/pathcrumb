# tests/test_fixer.py

from pathcrumb.fixer import fix_headers


def test_add_header(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("print('hello')\n")

    result = fix_headers([tmp_path], dry_run=False)

    content = file.read_text()

    assert "# example.py" in content
    assert result["stats"]["added"] == 1


def test_update_header(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("# wrong.py\n\nprint('hello')\n")

    result = fix_headers([tmp_path], dry_run=False)

    content = file.read_text()

    assert "# example.py" in content
    assert result["stats"]["updated"] == 1


def test_dry_run_does_not_modify(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("print('hello')\n")

    fix_headers([tmp_path], dry_run=True)

    content = file.read_text()

    assert content == "print('hello')\n"


def test_shebang_preserved(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("#!/usr/bin/env python3\nprint('hello')\n")

    fix_headers([tmp_path], dry_run=False)

    content = file.read_text().splitlines()

    assert content[0].startswith("#!")
    assert "# example.py" in content[1]


def test_spacing_normalized(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("# example.py\nprint('hello')\n")

    fix_headers([tmp_path], dry_run=False)

    lines = file.read_text().splitlines()

    assert lines[1] == ""
