# tests/test_scanner.py

from pathcrumb.scanner import iter_python_files


def test_iter_python_files(tmp_path):
    (tmp_path / "a.py").write_text("")
    (tmp_path / "b.txt").write_text("")

    files = list(iter_python_files([tmp_path]))

    assert len(files) == 1
    assert files[0].name == "a.py"


def test_ignore_directory(tmp_path):
    ignored = tmp_path / "__pycache__"
    ignored.mkdir()

    file = ignored / "a.py"
    file.write_text("")

    files = list(iter_python_files([tmp_path]))

    assert files == []
