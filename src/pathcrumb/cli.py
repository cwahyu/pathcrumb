# src/pathcrumb/cli.py

import typer
from pathlib import Path

from .checker import find_missing_headers
from .fixer import fix_headers

app = typer.Typer(help="Keep Python file headers aligned with file paths")


@app.command()
def check(paths: list[Path] = typer.Argument(None)):
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

    raise typer.Exit(code=1)


@app.command()
def fix(
    paths: list[Path] = typer.Argument(None),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview changes"),
):
    """
    Fix or add header paths.
    """

    roots = paths or [Path.cwd()]

    fix_headers(roots, dry_run)


if __name__ == "__main__":
    app()
