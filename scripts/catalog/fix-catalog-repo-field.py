#!/usr/bin/env python3
"""Set catalog.toml repo = \"benchmarks\" when the workload path exists under this repo.

Part of PH-5b / benchmarks#266 sub-phase A (benchmarks-only workload ADR).

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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    import tomllib

    text = CATALOG.read_text(encoding="utf-8")
    benchmarks = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    fixes: list[tuple[str, str, str]] = []

    for b in benchmarks:
        rel = str(b.get("path") or "").strip()
        if not rel or rel == "unknown":
            continue
        repo = str(b.get("repo", "lic"))
        if repo == "benchmarks":
            continue
        if not rel.startswith("benchmarks/"):
            continue
        if not (ROOT / rel).exists():
            continue
        fixes.append((b["id"], repo, "benchmarks"))
        b["repo"] = "benchmarks"

    print(f"repo field fixes: {len(fixes)}")
    for bench_id, old, new in fixes[:15]:
        print(f"  {bench_id}: {old} -> {new}")
    if len(fixes) > 15:
        print(f"  ... and {len(fixes) - 15} more")

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
