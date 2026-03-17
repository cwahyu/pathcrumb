# src/pathcrumb/fixer.py

from pathlib import Path
from .patterns import HEADER_PATTERN
from .scanner import iter_python_files


def update_header(file_path: Path, dry_run: bool):
    project_root = Path.cwd().resolve()
    rel_path = file_path.resolve().relative_to(project_root)

    header_line = f"# {rel_path}"

    lines = file_path.read_text().splitlines()

    if not lines:
        return "skipped"

    idx = 0

    # detect shebang
    if lines[0].startswith("#!"):
        idx = 1

    # detect existing header
    if idx < len(lines) and HEADER_PATTERN.match(lines[idx]):
        # header exists but incorrect
        if lines[idx].strip() != header_line:
            print(f"Update: {rel_path}")

            if not dry_run:
                lines[idx] = header_line
                _normalize_spacing(lines)
                file_path.write_text("\n".join(lines) + "\n")

            return "updated"

        # header correct → normalize spacing only
        if not dry_run:
            original = list(lines)
            _normalize_spacing(lines)

            if lines != original:
                file_path.write_text("\n".join(lines) + "\n")

        return "ok"

    # header missing
    print(f"Add: {rel_path}")

    if not dry_run:
        new_lines = []

        # preserve shebang
        if idx == 1:
            new_lines.append(lines[0])

        # insert header
        new_lines.append(header_line)

        # detect comment block after shebang/header
        comment_start = idx
        comment_block_end = comment_start

        while comment_block_end < len(lines) and lines[comment_block_end].startswith(
            "#"
        ):
            comment_block_end += 1

        # preserve comment block
        if comment_block_end > comment_start:
            new_lines.extend(lines[comment_start:comment_block_end])

        # enforce blank line
        new_lines.append("")

        new_lines.extend(lines[comment_block_end:])

        _normalize_spacing(new_lines)

        file_path.write_text("\n".join(new_lines) + "\n")

    return "added"


def _normalize_spacing(lines: list[str]) -> None:
    """
    Ensure exactly one blank line after the header/comment block.
    """

    i = 0

    # skip shebang
    if lines and lines[0].startswith("#!"):
        i = 1

    # skip header + comment block
    while i < len(lines) and lines[i].startswith("#"):
        i += 1

    # remove extra blank lines
    while i < len(lines) and lines[i] == "":
        lines.pop(i)

    # insert exactly one blank line
    lines.insert(i, "")


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
