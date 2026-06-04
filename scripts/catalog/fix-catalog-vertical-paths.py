#!/usr/bin/env python3
"""Correct competitive-vertical catalog rows that alias unrelated harness paths.

When benchmarks/workloads/tier2_physics/<id> exists but catalog points at a shared
tier1_micro or md_* kernel, rewrite path and repo=benchmarks (catalog honesty PH-5b).

Usage:
  python3 scripts/catalog/fix-catalog-vertical-paths.py --dry-run
  python3 scripts/catalog/fix-catalog-vertical-paths.py --write
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"

VERTICAL_PREFIXES = ("bio_", "drug_", "am_")


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


def dedicated_path(bench_id: str) -> Path | None:
    p = ROOT / "benchmarks" / "workloads" / "tier2_physics" / bench_id
    return p if p.is_dir() else None


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
        bid = str(b.get("id") or "")
        if not bid.startswith(VERTICAL_PREFIXES):
            continue
        dedicated = dedicated_path(bid)
        if dedicated is None:
            continue
        rel = f"benchmarks/workloads/tier2_physics/{bid}"
        cur = str(b.get("path") or "")
        if cur == rel and str(b.get("repo")) == "benchmarks":
            continue
        fixes.append((bid, cur, rel))
        if args.write:
            b["path"] = rel
            b["repo"] = "benchmarks"
            if b.get("variant") == "algo_registry":
                b["variant"] = "shared_c_kernel"

    print(f"vertical path fixes: {len(fixes)}")
    for bench_id, old, new in fixes:
        print(f"  {bench_id}: {old} -> {new}")

    if not args.write:
        return 0

    header = load_header(text)
    CATALOG.write_text(header + "\n\n".join(format_benchmark(b) for b in benches) + "\n")
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
