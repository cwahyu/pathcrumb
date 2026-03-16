from pathlib import Path
from .patterns import HEADER_PATTERN
from .scanner import iter_python_files


def find_missing_headers(root: Path):
    missing = []

    for py_file in iter_python_files(root):
        lines = py_file.read_text().splitlines()

        if not lines:
            continue

        if not HEADER_PATTERN.match(lines[0]):
            missing.append(py_file.relative_to(root))

    if not missing:
        print("✔ All Python files contain header paths.")
        return

    print("\n⚠ Files missing header paths:\n")

    for file in missing:
        print(f"  {file}")

    print(f"\nTotal missing headers: {len(missing)}")
