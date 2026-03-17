# src/pathcrumb/cli.py

import typer
from pathlib import Path

from .checker import find_missing_headers
from .fixer import fix_headers

app = typer.Typer(help="Keep Python file headers aligned with file paths")


@app.command()
def check(
    paths: list[Path] = typer.Argument(None),
    fail_on_missing: bool = typer.Option(
        False,
        "--fail-on-missing",
        help="Exit with code 1 if headers are missing (useful for CI).",
    ),
):
    """
    Check for missing header paths.
    """

    roots = paths or [Path.cwd()]

    missing = find_missing_headers(roots)

    if not missing:
        print("✔ All Python files contain header paths.")
        raise typer.Exit(code=0)

    print("\n⚠ Files missing header paths:\n")

    for file in missing:
        print(f"  {file}")

    print(f"\nTotal missing headers: {len(missing)}")

    if fail_on_missing:
        raise typer.Exit(code=1)

    raise typer.Exit(code=0)


@app.command()
def fix(
    paths: list[Path] = typer.Argument(None),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview changes"),
):
    """
    Fix or add header paths.
    """

    roots = paths or [Path.cwd()]

    stats = fix_headers(roots, dry_run)

    print()

    print(f"Scanned {stats['scanned']} files")

    if stats["added"] == 0 and stats["updated"] == 0:
        print("No header changes needed")
        return

    print(f"Added headers: {stats['added']}")
    print(f"Updated headers: {stats['updated']}")
