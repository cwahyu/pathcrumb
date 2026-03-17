# tests/test_headers.py

from pathcrumb.checker import find_missing_headers


def test_detect_missing_header(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("print('hello')\n")

    missing = find_missing_headers([tmp_path])

    assert len(missing) == 1
    assert missing[0].name == "example.py"
