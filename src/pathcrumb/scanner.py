# src/pathcrumb/scanner.py

from pathlib import Path
from .config import load_config


def should_skip(file_path: Path) -> bool:
    config = load_config()
    ignored = config["ignore"]

    return any(part in ignored for part in file_path.parts)


def iter_python_files(roots: list[Path]):
    for root in roots:
        if root.is_file():
            if root.suffix == ".py" and not should_skip(root):
                yield root
            continue

        for py_file in root.rglob("*.py"):
            if should_skip(py_file):
                continue

            yield py_file
