# tests/test_headers.py

from pathlib import Path

from pathcrumb.checker import find_missing_headers


def test_detect_missing_header(tmp_path):

    file = tmp_path / "example.py"
    file.write_text("print('hello')\n")

    missing = find_missing_headers([tmp_path])

    assert len(missing) == 1
    assert missing[0] == Path("example.py")


def test_shebang_header(tmp_path):

    file = tmp_path / "example.py"

    file.write_text("#!/usr/bin/env python3\n# example.py\n\nprint('hello')\n")

    missing = find_missing_headers([tmp_path])

    assert missing == []


def test_empty_file_ignored(tmp_path):
    file = tmp_path / "empty.py"
    file.write_text("")

    missing = find_missing_headers([tmp_path])

    assert missing == []
