#!/usr/bin/env python3
"""Apply PH-5b catalog honesty fixes (repo/path/defer) from catalog-gap-triage logic.

Usage:
  LIC_ROOT=../lic python3 scripts/catalog/apply-catalog-honesty-ph5b.py --dry-run
  LIC_ROOT=../lic python3 scripts/catalog/apply-catalog-honesty-ph5b.py --write
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from catalog.catalog_honesty import classify_row  # noqa: E402

CATALOG = ROOT / "catalog.toml"


def load_format_benchmark():
    path = Path(__file__).parent / "sync-paths-from-lic-tree.py"
    spec = importlib.util.spec_from_file_location("sync_paths", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.format_benchmark, mod.load_header


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.write and not args.dry_run:
        ap.error("pass --write or --dry-run")

    text = CATALOG.read_text(encoding="utf-8")
    rows = tomllib.loads(text).get("benchmark", [])
    format_benchmark, load_header = load_format_benchmark()

    changes: list[str] = []
    for row in rows:
        item = classify_row(row)
        action = item["action"]
        if action == "ok" or action == "skip":
            continue
        if action == "defer_planned":
            if row.get("catalog_lifecycle") != "planned":
                row["catalog_lifecycle"] = "planned"
                changes.append(f"{row['id']}: defer -> planned")
            continue
        if action in ("fix_repo", "fix_path"):
            row["repo"] = item["repo"]
            row["path"] = item["path"]
            changes.append(
                f"{row['id']}: {item.get('was_repo')}:{item.get('was_path')} "
                f"-> {item['repo']}:{item['path']} ({item.get('reason')})"
            )

    print(f"changes: {len(changes)}")
    for line in changes[:40]:
        print(f"  {line}")
    if len(changes) > 40:
        print(f"  ... and {len(changes) - 40} more")

    if args.write:
        body = load_header(text) + "\n".join(format_benchmark(b) for b in rows) + "\n"
        CATALOG.write_text(body, encoding="utf-8")
        print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
