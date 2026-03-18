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

        idx = 0

        # skip shebang
        if lines[0].startswith("#!"):
            idx = 1

        if idx >= len(lines) or not HEADER_PATTERN.match(lines[idx]):
            # compute path relative to the closest root
            for root in roots:
                try:
                    rel = py_file.resolve().relative_to(root.resolve())
                    break
                except ValueError:
                    continue
            else:
                rel = py_file

            missing.append(rel)

    return missing
