# src/pathcrumb/scanner.py

from pathlib import Path
from .config import IGNORED_DIR_NAMES


def should_skip(file_path: Path) -> bool:
    """
    Skip files located inside ignored directories.
    """
    return any(part in IGNORED_DIR_NAMES for part in file_path.parts)


def iter_python_files(roots: list[Path]):
    """
    Iterate over Python files inside one or more root directories.
    """

    for root in roots:
        if root.is_file():
            if root.suffix == ".py" and not should_skip(root):
                yield root
            continue

        for py_file in root.rglob("*.py"):
            if should_skip(py_file):
                continue

            yield py_file
