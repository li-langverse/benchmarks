#!/usr/bin/env python3
"""PH-5b catalog honesty: repo field, vertical stub paths, planned deferrals (#266).

- Set repo=benchmarks when path exists under this repo (ADR benchmarks-only workloads).
- Fix bogus competitive-vertical remaps (id != path tail) when tier2 workload dir exists.
- Mark rows with no on-disk harness as catalog_lifecycle=planned, path=unknown.
- Fix lis tier-5 paths (vendor layout: benchmarks/tier5_http/..., not workloads/).

Usage:
  python3 scripts/catalog/fix-catalog-honesty-ph5b.py --dry-run
  python3 scripts/catalog/fix-catalog-honesty-ph5b.py --write
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
WORKLOADS = ROOT / "benchmarks" / "workloads"
VENDOR_LIS = ROOT / "vendor" / "lis-tier5"

BENCHMARK_KEYS = (
    "id",
    "base_id",
    "category",
    "pillar",
    "package",
    "tier",
    "repo",
    "path",
    "metric",
    "threshold_ratio_cpp",
    "compare_oracle",
    "variant",
    "problem_size",
    "size_label",
    "validity_required",
    "catalog_lifecycle",
)

VERTICAL_PREFIXES = ("bio_", "drug_", "am_")

# Rows that stay on lic repo (tier-0 proofs in li-tests).
LIC_ONLY_PATH_PREFIXES = ("li-tests/", "packages/")


def workload_path_for_id(bid: str) -> str | None:
    for tier in ("tier2_physics", "tier1_micro", "tier1_stdlib", "tier3_ecosystem"):
        if (WORKLOADS / tier / bid).is_dir():
            return f"benchmarks/workloads/{tier}/{bid}"
    return None


def path_exists_in_repo(repo: str, rel: str) -> bool:
    if not rel or rel == "unknown":
        return False
    if rel.startswith(LIC_ONLY_PATH_PREFIXES):
        return False
    if repo in ("benchmarks", "lic", "li-math", "lig"):
        return (ROOT / rel).is_dir() or (ROOT / rel).is_file()
    if repo == "lis":
        root = VENDOR_LIS if VENDOR_LIS.is_dir() else ROOT
        return (root / rel).is_dir() or (root / rel).is_file()
    return False


def is_bogus_vertical_remap(row: dict) -> bool:
    bid = str(row.get("id", ""))
    rel = str(row.get("path", "")).strip()
    if not bid.startswith(VERTICAL_PREFIXES):
        return False
    tail = rel.split("/")[-1] if rel else ""
    return bool(tail and tail != bid)


def format_benchmark(b: dict) -> str:
    lines = ["[[benchmark]]", f'id = "{b["id"]}"']
    for key in BENCHMARK_KEYS:
        if key == "id" or key not in b or b[key] is None:
            continue
        val = b[key]
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


def parse_catalog(text: str) -> tuple[str, list[dict]]:
    import tomllib

    header_end = text.find("[[benchmark]]")
    header = text[:header_end].rstrip() + "\n\n" if header_end != -1 else ""
    data = tomllib.loads(text)
    return header, list(data.get("benchmark", []))


def apply_fixes(rows: list[dict]) -> tuple[list[dict], dict[str, int]]:
    stats = {
        "repo_benchmarks": 0,
        "path_vertical_fix": 0,
        "planned_defer": 0,
        "tier5_path_fix": 0,
    }
    out: list[dict] = []
    for row in rows:
        b = dict(row)
        rel = str(b.get("path", "")).strip()
        repo = str(b.get("repo", "lic"))
        bid = str(b.get("id", ""))

        if rel.startswith("benchmarks/workloads/tier5_http/") and repo == "lis":
            fixed = rel.replace("/workloads/tier5_http/", "/tier5_http/", 1)
            if fixed != rel:
                b["path"] = fixed
                stats["tier5_path_fix"] += 1
                rel = fixed

        if is_bogus_vertical_remap(b):
            honest = workload_path_for_id(bid)
            if honest:
                b["path"] = honest
                b["repo"] = "benchmarks"
                if b.get("variant") == "algo_registry":
                    b["variant"] = "competitive_vertical"
                stats["path_vertical_fix"] += 1
                rel = honest
                repo = "benchmarks"

        if rel and rel != "unknown" and not rel.startswith(LIC_ONLY_PATH_PREFIXES):
            if path_exists_in_repo("benchmarks", rel) and repo != "benchmarks":
                if repo == "lic" or (repo in ("lig", "li-math") and rel.startswith("benchmarks/")):
                    b["repo"] = "benchmarks"
                    stats["repo_benchmarks"] += 1
                    repo = "benchmarks"

        if (
            rel
            and rel != "unknown"
            and b.get("catalog_lifecycle") != "planned"
            and not path_exists_in_repo(repo, rel)
            and not rel.startswith(LIC_ONLY_PATH_PREFIXES)
        ):
            b["catalog_lifecycle"] = "planned"
            b["path"] = "unknown"
            if not b.get("variant"):
                b["variant"] = "vertical_stub"
            ph = list(b.get("ph_ids") or [])
            if "PH-5b" not in ph:
                ph.append("PH-5b")
            b["ph_ids"] = ph
            stats["planned_defer"] += 1

        out.append(b)
    return out, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write catalog.toml")
    parser.add_argument("--dry-run", action="store_true", help="Print stats only")
    args = parser.parse_args()
    if not CATALOG.is_file():
        raise SystemExit(f"missing {CATALOG}")

    text = CATALOG.read_text(encoding="utf-8")
    header, rows = parse_catalog(text)
    fixed_rows, stats = apply_fixes(rows)

    print("fix-catalog-honesty-ph5b:", stats)
    if args.dry_run or not args.write:
        if not args.write:
            print("(dry-run; pass --write to apply)")
        return 0

    body = header + "\n".join(format_benchmark(b) for b in fixed_rows) + "\n"
    CATALOG.write_text(body, encoding="utf-8")
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
