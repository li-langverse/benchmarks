#!/usr/bin/env python3
"""Set catalog.toml repo=benchmarks when the workload path exists under this repo.

Fixes false plan-completion-audit gaps from ADR single-repo layout (workloads live
under benchmarks/ but rows still say repo=lic or repo=lis).

Usage:
  python3 scripts/catalog/fix-catalog-repo-field.py --dry-run
  python3 scripts/catalog/fix-catalog-repo-field.py --write
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"

REPO_WHEN_PATH_UNDER_BENCHMARKS = frozenset({"lic", "lis"})


def load_header(text: str) -> str:
    idx = text.find("[[benchmark]]")
    return text[:idx].rstrip() + "\n\n" if idx != -1 else ""


def format_benchmark(b: dict) -> str:
    lines = ["[[benchmark]]", f'id = "{b["id"]}"']
    skip = {"id", "ph_ids"}
    for key, val in b.items():
        if key in skip:
            continue
        if val is None:
            continue
        if isinstance(val, bool):
            lines.append(f"{key} = {'true' if val else 'false'}")
        elif isinstance(val, (int, float)):
            lines.append(f"{key} = {val}")
        else:
            lines.append(f'{key} = "{val}"')
    ph = b.get("ph_ids") or []
    if ph:
        lines.append("ph_ids = [" + ", ".join(f'"{p}"' for p in ph) + "]")
    return "\n".join(lines)


def main() -> int:
    import tomllib

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.write:
        parser.error("pass --dry-run or --write")

    text = CATALOG.read_text(encoding="utf-8")
    benches = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    fixes: list[tuple[str, str, str]] = []
    for b in benches:
        rel = str(b.get("path") or "").strip()
        if not rel or rel == "unknown":
            continue
        repo = str(b.get("repo") or "lic")
        if repo not in REPO_WHEN_PATH_UNDER_BENCHMARKS:
            continue
        if not (ROOT / rel).exists():
            continue
        fixes.append((b["id"], repo, "benchmarks"))
        if args.write:
            b["repo"] = "benchmarks"

    print(f"repo field fixes: {len(fixes)}")
    for bench_id, old, new in fixes[:25]:
        print(f"  {bench_id}: {old} -> {new}")
    if len(fixes) > 25:
        print(f"  ... and {len(fixes) - 25} more")

    if not args.write:
        return 0

    header = load_header(text)
    CATALOG.write_text(header + "\n\n".join(format_benchmark(b) for b in benches) + "\n")
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
