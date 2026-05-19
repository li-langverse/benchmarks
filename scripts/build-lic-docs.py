#!/usr/bin/env python3
"""Build lic MkDocs site when LIC_ROOT is set (for real UX docs audit)."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def lic_root() -> Path:
    return Path(os.environ.get("LIC_ROOT", Path(__file__).resolve().parents[2] / "lic")).resolve()


def site_index() -> Path:
    return lic_root() / "site" / "index.html"


def build(force: bool = False) -> int:
    root = lic_root()
    index = site_index()
    if index.is_file() and not force:
        print(json_ok(root, built=False, reason="site already built"))
        return 0

    mkdocs_yml = root / "mkdocs.yml"
    req = root / "docs" / "requirements.txt"
    if not mkdocs_yml.is_file():
        print(f"lic mkdocs.yml missing: {mkdocs_yml}", file=sys.stderr)
        return 1

    if not shutil.which("mkdocs") and req.is_file():
        proc = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-r", str(req)],
            check=False,
        )
        if proc.returncode != 0:
            return proc.returncode

    mkdocs_bin = shutil.which("mkdocs") or "mkdocs"
    proc = subprocess.run(
        [mkdocs_bin, "build", "-f", str(mkdocs_yml)],
        cwd=str(root),
        check=False,
    )
    if proc.returncode != 0:
        return proc.returncode
    if not index.is_file():
        print(f"mkdocs build finished but missing {index}", file=sys.stderr)
        return 1
    print(json_ok(root, built=True))
    return 0


def json_ok(root: Path, built: bool, reason: str | None = None) -> str:
    import json

    return json.dumps(
        {
            "ok": True,
            "lic_root": str(root),
            "site_index": str(site_index()),
            "built": built,
            "reason": reason,
        }
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    raise SystemExit(build(force=args.force))
