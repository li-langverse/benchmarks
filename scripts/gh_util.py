"""Shared GitHub CLI helpers for benchmarks preflight scripts."""
from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any


def gh_available() -> bool:
    return shutil.which("gh") is not None


def gh_json(args: list[str], *, default: Any = None) -> Any:
    """Run ``gh`` and parse JSON stdout; tolerate Windows UTF-8 and empty output."""
    proc = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    stdout = proc.stdout or ""
    if proc.returncode != 0 or not stdout.strip():
        return default
    return json.loads(stdout)
