# src/pathcrumb/cli.py

import importlib.metadata
from pathlib import Path

import tomli_w
import tomllib
import typer

from .checker import find_missing_headers
from .config import load_config
from .fixer import fix_headers

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


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


def resolve_roots(paths: list[Path] | None) -> list[Path]:
    """
    Resolve scan roots from CLI arguments or configuration.
    """
    config = load_config()

    if paths:
        return paths

    if config["target"]:
        return [Path(p) for p in config["target"]]

    return [Path.cwd()]


# -----------------------------------------------------------------------------
# App
# -----------------------------------------------------------------------------


app = typer.Typer(
    help=(
        "Keep Python file headers aligned with their relative file paths.\n\n"
        "Examples:\n"
        "  pathcrumb init\n"
        "  pathcrumb fix\n"
        "  pathcrumb fix src --dry-run\n"
        "  pathcrumb check --fail-on-missing\n"
    ),
    add_completion=False,
    no_args_is_help=True,
)


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
):
    """
    Pathcrumb CLI.
    """
    pass


# -----------------------------------------------------------------------------
# Commands
# -----------------------------------------------------------------------------


@app.command()
def check(
    paths: list[Path] = typer.Argument(
        None,
        help=(
            "Files or directories to scan (default: configured target or project root)."
        ),
    ),
    fail_on_missing: bool = typer.Option(
        False,
        "--fail-on-missing",
        help="Exit with code 1 if missing headers are found (CI-friendly).",
    ),
):
    """
    Check Python files for missing header paths.

    Examples:
      pathcrumb check
      pathcrumb check src
      pathcrumb check src tests
      pathcrumb check --fail-on-missing
    """

    roots = resolve_roots(paths)
    missing = find_missing_headers(roots)

    if not missing:
        print("All Python files contain header paths.")
        raise typer.Exit(code=0)

    print("\nFiles missing header paths:\n")

    for file in missing:
        print(f"  {file}")

    print(f"\nTotal missing headers: {len(missing)}")

    if fail_on_missing:
        raise typer.Exit(code=1)

    raise typer.Exit(code=0)


@app.command()
def fix(
    paths: list[Path] = typer.Argument(
        None,
        help=(
            "Files or directories to scan (default: configured target or project root)."
        ),
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview changes without modifying files.",
    ),
    check: bool = typer.Option(
        False,
        "--check",
        help="Exit with code 1 if changes would be made.",
    ),
):
    """
    Add or update header paths in Python files.

    Examples:
      pathcrumb fix
      pathcrumb fix src
      pathcrumb fix src --dry-run
      pathcrumb fix --check
    """

    roots = resolve_roots(paths)

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

    This adds a [tool.pathcrumb] section with default settings.

    Example:
      pathcrumb init
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

    print("Added configuration:\n")
    print("[tool.pathcrumb]")
    print('target = ["src"]')
    print('ignore = ["tests"]')
