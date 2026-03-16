import typer
from pathlib import Path

from .checker import find_missing_headers
from .fixer import fix_headers

app = typer.Typer(help="Keep Python file headers aligned with file paths")


@app.command()
def check():
    """Check for missing header paths."""
    root = Path.cwd()
    find_missing_headers(root)


@app.command()
def fix(dry_run: bool = typer.Option(False, "--dry-run", help="Preview changes")):
    """Fix incorrect headers."""
    root = Path.cwd()
    fix_headers(root, dry_run)


if __name__ == "__main__":
    app()
