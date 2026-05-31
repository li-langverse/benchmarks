#!/usr/bin/env python3
"""Copy benchmark workloads and harness files from LIC_ROOT into this repo.

Idempotent: only adds missing paths; does not overwrite newer benchmarks files.
Preserves benchmarks-only harness modules (paths.py, run_suite.py).
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

BENCH_REPO = Path(__file__).resolve().parents[1]
WORKLOADS = BENCH_REPO / "benchmarks" / "workloads"
HARNESS = BENCH_REPO / "harness"
SKIP_HARNESS = frozenset({"paths.py", "run_suite.py"})

WORKLOAD_TIERS = (
    "tier1_stdlib",
    "tier3_ecosystem",
    "tier5_http",
    "competitive",
    "toolchain",
    "runtime_refs",
)


def lic_root() -> Path:
    raw = os.environ.get("LIC_ROOT") or os.environ.get("LI_REPO_ROOT")
    if raw:
        return Path(raw).resolve()
    sibling = BENCH_REPO.parent / "lic"
    if sibling.is_dir():
        return sibling.resolve()
    raise SystemExit("Set LIC_ROOT to li-langverse/lic checkout")


def copy_tree(src: Path, dst: Path) -> tuple[int, int]:
    added = skipped = 0
    if not src.is_dir():
        return added, skipped
    for root, _dirs, files in os.walk(src):
        rel = Path(root).relative_to(src)
        out_dir = dst / rel
        out_dir.mkdir(parents=True, exist_ok=True)
        for name in files:
            s = Path(root) / name
            d = out_dir / name
            if d.exists():
                skipped += 1
                continue
            shutil.copy2(s, d)
            added += 1
    return added, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lic-root", type=Path, default=None)
    args = parser.parse_args()
    lic = args.lic_root.resolve() if args.lic_root else lic_root()
    lic_bench = lic / "benchmarks"
    if not lic_bench.is_dir():
        raise SystemExit(f"missing {lic_bench}")

    WORKLOADS.mkdir(parents=True, exist_ok=True)
    total_add = total_skip = 0
    for tier in WORKLOAD_TIERS:
        src = lic_bench / tier
        dst = WORKLOADS / tier
        a, s = copy_tree(src, dst)
        print(f"{tier}: +{a} files (skipped existing {s})")
        total_add += a
        total_skip += s

    lic_h = lic_bench / "harness"
    h_add = h_skip = 0
    if lic_h.is_dir():
        for item in lic_h.iterdir():
            if item.name in SKIP_HARNESS:
                continue
            dst = HARNESS / item.name
            if item.is_dir():
                a, s = copy_tree(item, dst)
                h_add += a
                h_skip += s
            elif not dst.exists():
                shutil.copy2(item, dst)
                h_add += 1
            else:
                h_skip += 1
    print(f"harness: +{h_add} files (skipped existing {h_skip})")
    print(f"done: workloads +{total_add}, harness +{h_add}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
