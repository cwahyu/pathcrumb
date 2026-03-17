# src/pathcrumb/fixer.py

from pathlib import Path
from .patterns import HEADER_PATTERN
from .scanner import iter_python_files


def update_header(file_path: Path, dry_run: bool):
    project_root = Path.cwd()
    rel_path = file_path.resolve().relative_to(project_root)

    new_header = f"# {rel_path}"

    lines = file_path.read_text().splitlines()

    if not lines:
        return "skipped"

    first_line = lines[0]

    # Case 1: header exists but incorrect
    if HEADER_PATTERN.match(first_line):
        if first_line.strip() != new_header:
            print(f"Update: {rel_path}")

            if not dry_run:
                lines[0] = new_header
                file_path.write_text("\n".join(lines) + "\n")

            return "updated"

        return "ok"

    # Case 2: header missing
    print(f"Add: {rel_path}")

    if not dry_run:
        lines.insert(0, new_header)
        file_path.write_text("\n".join(lines) + "\n")

    return "added"


def fix_headers(roots: list[Path], dry_run: bool):
    stats = {
        "scanned": 0,
        "added": 0,
        "updated": 0,
    }

    for py_file in iter_python_files(roots):
        stats["scanned"] += 1

        result = update_header(py_file, dry_run)

        if result == "added":
            stats["added"] += 1

        if result == "updated":
            stats["updated"] += 1

    return stats
