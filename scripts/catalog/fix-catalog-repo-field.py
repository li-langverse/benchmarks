#!/usr/bin/env python3
"""Align catalog.toml repo/path fields with benchmarks-only workload ADR (PH-5b / #266).

Sub-phases:
  A — set repo=benchmarks when benchmarks/<path> exists on disk
  B — competitive vertical stub remaps → planned + path=unknown + variant=vertical_stub
  C — fix lis tier-5 paths (vendor/lis-tier5 uses benchmarks/tier5_http, not workloads/)

Usage:
  python3 scripts/catalog/fix-catalog-repo-field.py --dry-run
  python3 scripts/catalog/fix-catalog-repo-field.py --write
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
VENDOR_LIS = ROOT / "vendor/lis-tier5"

# Competitive-vertical ids that incorrectly alias tier1/tier2 micro kernels.
VERTICAL_STUB_PREFIXES = ("bio_", "drug_", "am_")

LIS_WORKLOADS_PREFIX = "benchmarks/workloads/tier5_http/"
LIS_LEGACY_PREFIX = "benchmarks/tier5_http/"


def load_format_benchmark():
    path = Path(__file__).parent / "sync-paths-from-lic-tree.py"
    spec = importlib.util.spec_from_file_location("sync_paths", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.format_benchmark, mod.load_header


def is_vertical_stub_remap(bench_id: str, path: str) -> bool:
    if not bench_id.startswith(VERTICAL_STUB_PREFIXES):
        return False
    if not path or path == "unknown":
        return False
    tail = path.rsplit("/", 1)[-1]
    return tail != bench_id


def resolve_lis_path(path: str) -> str | None:
    """Return corrected lis-relative path when vendor tree has the scenario."""
    if not path.startswith(LIS_WORKLOADS_PREFIX):
        return None
    legacy = LIS_LEGACY_PREFIX + path[len(LIS_WORKLOADS_PREFIX) :]
    if (VENDOR_LIS / legacy).is_dir():
        return legacy
    return None


def apply_fixes(benchmarks: list[dict]) -> list[tuple[str, str, str]]:
    changes: list[tuple[str, str, str]] = []

    for b in benchmarks:
        bid = b["id"]
        repo = str(b.get("repo") or "lic")
        path = str(b.get("path") or "")

        if is_vertical_stub_remap(bid, path):
            old = f"repo={repo} path={path}"
            b["path"] = "unknown"
            b["catalog_lifecycle"] = "planned"
            b["variant"] = "vertical_stub"
            changes.append((bid, old, "planned vertical_stub path=unknown"))
            continue

        if repo == "lic" and path.startswith("benchmarks/") and (ROOT / path).is_dir():
            old = f"repo=lic path={path}"
            b["repo"] = "benchmarks"
            changes.append((bid, old, f"repo=benchmarks path={path}"))
            repo = "benchmarks"

        if repo == "lis" and path.startswith("benchmarks/") and (ROOT / path).is_dir():
            old = f"repo=lis path={path}"
            b["repo"] = "benchmarks"
            changes.append((bid, old, f"repo=benchmarks path={path}"))
            repo = "benchmarks"

        if repo == "lis":
            fixed = resolve_lis_path(path)
            if fixed and fixed != path:
                old = f"repo=lis path={path}"
                b["path"] = fixed
                changes.append((bid, old, f"repo=lis path={fixed}"))

        if bid == "proxy_loopback" and path == "packages/li-net-httpd":
            legacy = f"{LIS_LEGACY_PREFIX}scenarios/proxy_loopback"
            if (VENDOR_LIS / legacy).is_dir():
                old = f"repo={repo} path={path}"
                b["repo"] = "lis"
                b["path"] = legacy
                changes.append((bid, old, f"repo=lis path={legacy}"))

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    import tomllib

    format_benchmark, load_header = load_format_benchmark()
    text = CATALOG.read_text(encoding="utf-8")
    benchmarks = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]

    changes = apply_fixes(benchmarks)
    print(f"catalog fixes: {len(changes)}")
    for bid, old, new in changes[:25]:
        print(f"  {bid}: {old} -> {new}")
    if len(changes) > 25:
        print(f"  ... and {len(changes) - 25} more")

    if args.dry_run and not args.write:
        return 0
    if not args.write:
        print("pass --write to update catalog.toml", file=sys.stderr)
        return 1

    header = load_header(text)
    CATALOG.write_text(
        header + "\n\n".join(format_benchmark(b) for b in benchmarks) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
