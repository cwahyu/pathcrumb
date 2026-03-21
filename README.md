# pathcrumb

Keep Python file headers aligned with their relative file paths.

## What it does

pathcrumb ensures every Python file starts with a header like:

```python
# src/pathcrumb/checker.py
```

It can:

- add missing headers
- fix incorrect headers
- normalize spacing
- preserve shebang and comment blocks

## Installation

### Using pipx (recommended)

```bash
pipx install pathcrumb
```

### From source

```bash
git clone https://github.com/cwahyu/pathcrumb
cd pathcrumb

uv sync
uv pip install -e .
```

## Quick Start

Initialize configuration:

```bash
pathcrumb init
```

Fix headers:

```bash
pathcrumb fix
```

Check for issues:

```bash
pathcrumb check
```

## Commands

### pathcrumb fix

Add or update headers.

```bash
pathcrumb fix
pathcrumb fix src
pathcrumb fix src --dry-run
pathcrumb fix --check
```

Options:

- `--dry-run` → preview changes
- `--check` → do not modify files, exit with code 1 if changes are needed

### pathcrumb check

Check for missing headers.

```bash
pathcrumb check
pathcrumb check src
pathcrumb check --fail-on-missing
```

Options:

- `--fail-on-missing` → exit with code 1 if issues are found (CI-friendly)

### pathcrumb init

Add default configuration to pyproject.toml.

```toml
[tool.pathcrumb]
target = ["src"]
ignore = ["tests"]
```

## Configuration

Configure via pyproject.toml:

```toml
[tool.pathcrumb]
target = ["src"]
ignore = ["tests", "docs"]
```

- `target` → directories to scan by default
- `ignore` → directories to exclude

If not configured, pathcrumb scans the current directory.

## Behavior

pathcrumb enforces this structure:

```text
shebang (optional)
path header
comment block (optional)

code
```

### Example

Before:

```python
#!/usr/bin/env python3
# MIT License
print("hello")
```

After:

```python
#!/usr/bin/env python3
# src/example.py
# MIT License

print("hello")
```

## Typical Workflow

### Local development

```bash
pathcrumb fix
```

### CI

```bash
pathcrumb check --fail-on-missing
```

### Pre-commit

```yaml
- repo: local
  hooks:
    - id: pathcrumb
      name: pathcrumb
      entry: pathcrumb fix
      language: system
      types: [python]
```

## Philosophy

- minimal defaults
- explicit configuration
- predictable behavior

## Requirements

- Python 3.10+

## Development

Run tests:

```bash
uv run pytest
```

## License

MIT License
