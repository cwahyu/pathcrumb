# src/pathcrumb/cli.py

import importlib.metadata
from pathlib import Path

import tomli_w
import tomllib
import typer

from .checker import find_missing_headers
from .config import load_config
from .fixer import fix_headers


def get_version() -> str:
    """
    Get version from installed package metadata,
    fallback to pyproject.toml for local development.
    """

    try:
        return importlib.metadata.version("pathcrumb")
    except importlib.metadata.PackageNotFoundError:
        pyproject = Path.cwd() / "pyproject.toml"
        if pyproject.exists():
            data = tomllib.loads(pyproject.read_text())
            return data["project"]["version"]

    return "0.0.0"


def version_callback(value: bool):
    if value:
        print(f"pathcrumb {get_version()}")
        raise typer.Exit()


app = typer.Typer(
    help="Keep Python file headers aligned with file paths",
    add_completion=False,
)


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
):
    pass


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

    config = load_config()

    if paths:
        roots = paths
    elif config["target"]:
        roots = [Path(p) for p in config["target"]]
    else:
        roots = [Path.cwd()]

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
    check: bool = typer.Option(
        False,
        "--check",
        help="Do not modify files, exit with code 1 if changes would occur.",
    ),
):
    """
    Fix or add header paths.
    """

    roots = paths or [Path.cwd()]

    if check:
        dry_run = True

    stats = fix_headers(roots, dry_run)

    print()

    print(f"Scanned {stats['scanned']} files")

    if stats["added"] == 0 and stats["updated"] == 0:
        print("No header changes needed")
        raise typer.Exit(code=0)

    print(f"Added headers: {stats['added']}")
    print(f"Updated headers: {stats['updated']}")

    if check:
        raise typer.Exit(code=1)


@app.command()
def init():
    """
    Initialize pathcrumb configuration in pyproject.toml.
    """

    pyproject = Path.cwd() / "pyproject.toml"

    if not pyproject.exists():
        print("pyproject.toml not found.")
        raise typer.Exit(code=1)

    data = tomllib.loads(pyproject.read_text())

    tool = data.setdefault("tool", {})

    if "pathcrumb" in tool:
        print("[tool.pathcrumb] already exists in pyproject.toml")
        raise typer.Exit(code=0)

    tool["pathcrumb"] = {
        "target": ["src"],
        "ignore": ["tests"],
    }

    pyproject.write_text(tomli_w.dumps(data))

    print("Added configuration:")
    print()
    print("[tool.pathcrumb]")
    print('target = ["src"]')
    print('ignore = ["tests"]')
