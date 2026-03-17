# src/pathcrumb/checker.py

from pathlib import Path
from .patterns import HEADER_PATTERN
from .scanner import iter_python_files


def find_missing_headers(roots: list[Path]) -> list[Path]:
    """
    Return a list of Python files missing header paths.
    """

    missing: list[Path] = []

    for py_file in iter_python_files(roots):
        lines = py_file.read_text().splitlines()

        if not lines:
            continue

        if not HEADER_PATTERN.match(lines[0]):
            missing.append(py_file)

    return missing
