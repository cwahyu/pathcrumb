# src/pathcrumb/config.py

from pathlib import Path

import tomllib

DEFAULT_IGNORE_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "build",
    "dist",
}


def load_config():
    project_root = Path.cwd()
    pyproject = project_root / "pyproject.toml"

    config = {
        "target": None,
        "ignore": set(DEFAULT_IGNORE_DIRS),
    }

    if not pyproject.exists():
        return config

    data = tomllib.loads(pyproject.read_text())

    tool_cfg = data.get("tool", {}).get("pathcrumb")

    if not tool_cfg:
        return config

    if "ignore" in tool_cfg:
        config["ignore"] |= set(tool_cfg["ignore"])

    if "target" in tool_cfg:
        config["target"] = tool_cfg["target"]

    return config
