# src/pathcrumb/fixer.py

from pathlib import Path
from .patterns import HEADER_PATTERN
from .scanner import iter_python_files


def update_header(file_path: Path, root: Path, dry_run: bool):
    rel_path = file_path.relative_to(root)
    new_header = f"# {rel_path}"

    lines = file_path.read_text().splitlines()

    if not lines:
        return

    first_line = lines[0]

    # header exists but incorrect
    if HEADER_PATTERN.match(first_line):
        if first_line.strip() != new_header:
            print(f"Update: {rel_path}")

            if not dry_run:
                lines[0] = new_header
                file_path.write_text("\n".join(lines) + "\n")

        return

    # header missing
    print(f"Add: {rel_path}")

    if not dry_run:
        lines.insert(0, new_header)
        file_path.write_text("\n".join(lines) + "\n")


def fix_headers(roots: list[Path], dry_run: bool):
    for root in roots:
        for py_file in iter_python_files([root]):
            update_header(py_file, root, dry_run)
