# pathcrumb

Keep Python file headers aligned with their relative file paths.

## Installation

```bash
pipx install pathcrumb
```

## Usage

```bash
pathcrumb fix
pathcrumb check
```

## Examples

Add or update headers:

```bash
pathcrumb fix
pathcrumb fix src
```

Check for missing headers:

```bash
pathcrumb check
pathcrumb check --fail-on-missing
```

Preview changes:

```bash
pathcrumb fix --dry-run
```

CI mode:

```bash
pathcrumb fix --check
```

## Configuration

Configure via `pyproject.toml`:

```toml
[tool.pathcrumb]
target = ["src"]
ignore = ["tests"]
```

## Behavior

Each Python file should begin with:

```python
# path/to/file.py
```

Structure:

```text
shebang (optional)
path header
comment block (optional)

code
```

## Pre-commit

```yaml
repos:
  - repo: https://github.com/cwahyu/pathcrumb
    rev: v0.2.0
    hooks:
      - id: pathcrumb-fix
      - id: pathcrumb-check
```

## Development

```bash
uv run pytest
```

## License

MIT
