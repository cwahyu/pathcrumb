# tests/test_headers.py

from pathcrumb.checker import find_missing_headers


def test_detect_missing_header(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("print('hello')\n")

    find_missing_headers(tmp_path)
