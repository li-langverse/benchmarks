#!/usr/bin/env python3
"""Triage catalog.toml repo/path honesty for plan-completion-audit (PH-5b).

- Set ``repo = "benchmarks"`` when the path exists under the benchmarks checkout.
- Point tier-5 lis scenarios at ``vendor/lis-tier5/`` when workloads mirror is absent.
- Defer competitive vertical stub rows that wrongly alias numerics harness paths.

Usage:
  python3 scripts/catalog/triage-catalog-repo-honesty.py --dry-run
  python3 scripts/catalog/triage-catalog-repo-honesty.py --write
"""
from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
VENDOR_TIER5 = ROOT / "vendor/lis-tier5/benchmarks/tier5_http"

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

# Rows that intentionally target lic-only trees not vendored in benchmarks.
DEFER_LIC_ONLY = frozenset({"tier0_stability", "proxy_loopback"})

DEFER_PREFIXES = (
    "bio_",
    "drug_",
    "robo_",
    "viz_",
    "auto_",
    "am_",
    "fea_",
    "cfd_",
    "qm_",
    "gaming_",
    "rigid_",
)


def load_header(text: str) -> str:
    idx = text.find("[[benchmark]]")
    return text[:idx].rstrip() + "\n\n" if idx != -1 else ""


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


def path_on_disk(rel: str) -> Path | None:
    if not rel or rel == "unknown":
        return None
    p = ROOT / rel
    if p.is_dir() or p.is_file():
        return p
    if rel.startswith("benchmarks/workloads/tier5_http/"):
        alt = ROOT / rel.replace(
            "benchmarks/workloads/tier5_http/",
            "vendor/lis-tier5/benchmarks/tier5_http/",
        )
        if alt.is_dir() or alt.is_file():
            return alt
    return None


def resolve_honest_path(rel: str) -> str | None:
    """Return corrected relative path when a mirror exists, else None."""
    if not rel or rel == "unknown":
        return None
    if path_on_disk(rel):
        if rel.startswith("benchmarks/workloads/tier5_http/"):
            vendor_rel = rel.replace(
                "benchmarks/workloads/tier5_http/",
                "vendor/lis-tier5/benchmarks/tier5_http/",
            )
            workloads = ROOT / rel
            vendor = ROOT / vendor_rel
            if vendor.is_dir() and not workloads.is_dir():
                return vendor_rel
        return rel if (ROOT / rel).is_dir() or (ROOT / rel).is_file() else rel
    return None


def is_size_variant(bench_id: str, stem: str) -> bool:
    if bench_id == stem:
        return True
    return bool(re.match(rf"^{re.escape(stem)}_", bench_id))


def should_defer_stub(bench_id: str, path: str) -> bool:
    stem = Path(path).name
    if is_size_variant(bench_id, stem):
        return False
    if not any(bench_id.startswith(p) for p in DEFER_PREFIXES):
        return False
    if stem.startswith("num_") or stem.startswith("md_"):
        return True
    return False


def build_path_index(benchmarks: list[dict]) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for b in benchmarks:
        p = str(b.get("path") or "")
        if p and p != "unknown":
            index.setdefault(p, []).append(b["id"])
    return index


def triage(benchmarks: list[dict]) -> list[tuple[str, str, str, str]]:
    """Return list of (id, field, old, new) changes."""
    path_index = build_path_index(benchmarks)
    changes: list[tuple[str, str, str, str]] = []

    def record(bid: str, field: str, old: str, new: str) -> None:
        if old != new:
            changes.append((bid, field, old, new))

    workloads = ROOT / "benchmarks" / "workloads"

    for b in benchmarks:
        bid = b["id"]
        path = str(b.get("path") or "unknown")
        repo = str(b.get("repo") or "lic")
        lifecycle = str(b.get("catalog_lifecycle") or "")

        if lifecycle == "planned":
            continue

        if bid in DEFER_LIC_ONLY and not path_on_disk(path):
            record(bid, "path", path, "unknown")
            record(bid, "catalog_lifecycle", lifecycle, "planned")
            b["path"] = "unknown"
            b["catalog_lifecycle"] = "planned"
            continue

        for tier in ("tier1_micro", "tier2_physics", "tier1_stdlib"):
            wdir = workloads / tier / bid
            if wdir.is_dir():
                honest = f"benchmarks/workloads/{tier}/{bid}"
                if path != honest:
                    record(bid, "path", path, honest)
                    b["path"] = honest
                    path = honest
                if repo != "benchmarks":
                    record(bid, "repo", repo, "benchmarks")
                    b["repo"] = "benchmarks"
                break

        if path != "unknown":
            stem = Path(path).name
            ids_for_path = path_index.get(path, [])
            if len(ids_for_path) > 1 and should_defer_stub(bid, path):
                canonical = [i for i in ids_for_path if is_size_variant(i, stem)]
                if bid not in canonical:
                    record(bid, "path", path, "unknown")
                    record(bid, "catalog_lifecycle", lifecycle, "planned")
                    b["path"] = "unknown"
                    b["catalog_lifecycle"] = "planned"
                    continue

            resolved = resolve_honest_path(path)
            if resolved and resolved != path:
                record(bid, "path", path, resolved)
                b["path"] = resolved
                path = resolved

            if path_on_disk(path) and repo != "benchmarks":
                record(bid, "repo", repo, "benchmarks")
                b["repo"] = "benchmarks"

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.write:
        parser.error("pass --dry-run or --write")

    text = CATALOG.read_text(encoding="utf-8")
    benchmarks = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    changes = triage(benchmarks)
    print(f"catalog rows: {len(benchmarks)}")
    print(f"changes: {len(changes)}")
    for bid, field, old, new in changes[:25]:
        print(f"  {bid} {field}: {old!r} -> {new!r}")
    if len(changes) > 25:
        print(f"  ... and {len(changes) - 25} more")

    if args.dry_run or not args.write:
        return 0

    header = load_header(text)
    CATALOG.write_text(
        header + "\n\n".join(format_benchmark(b) for b in benchmarks) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
