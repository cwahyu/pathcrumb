from pathlib import Path
from .config import IGNORED_FOLDERS


def should_skip(file_path: Path) -> bool:
    return any(part in IGNORED_FOLDERS for part in file_path.parts)


def iter_python_files(root: Path):
    for py_file in root.rglob("*.py"):
        if should_skip(py_file):
            continue
        yield py_file
