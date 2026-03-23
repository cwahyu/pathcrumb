# src/pathcrumb/checker.py

from pathlib import Path

from .patterns import HEADER_PATTERN
from .scanner import iter_python_files


def find_missing_headers(roots: list[Path]) -> list[Path]:
    """
    Return a list of Python files missing header paths.
    """

    missing: list[Path] = []

    project_root = Path.cwd().resolve()

    for py_file in iter_python_files(roots):
        lines = py_file.read_text().splitlines()

        if not lines:
            continue

        idx = 0

        # skip shebang
        if lines[0].startswith("#!"):
            idx = 1

        if idx >= len(lines) or not HEADER_PATTERN.match(lines[idx]):
            file_resolved = py_file.resolve()

            try:
                # preferred: relative to project root
                rel = file_resolved.relative_to(project_root)
            except ValueError:
                # fallback: relative to scan roots
                for root in roots:
                    try:
                        rel = file_resolved.relative_to(root.resolve())
                        break
                    except ValueError:
                        continue
                else:
                    rel = Path(py_file.name)

            missing.append(rel)

    return missing
