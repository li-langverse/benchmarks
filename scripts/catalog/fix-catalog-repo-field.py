#!/usr/bin/env python3
"""Set catalog.toml repo=benchmarks when the workload path exists under benchmarks root.

Rows with catalog_lifecycle=planned or path=unknown are skipped.

Usage:
  python3 scripts/catalog/fix-catalog-repo-field.py --dry-run
  python3 scripts/catalog/fix-catalog-repo-field.py --write
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import tomllib
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


def load_format_module():
    path = Path(__file__).parent / "sync-paths-from-lic-tree.py"
    spec = importlib.util.spec_from_file_location("sync_paths", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def path_exists_under(root: Path, rel: str) -> bool:
    if not rel or rel == "unknown":
        return False
    p = root / rel
    return p.is_dir() or p.is_file()


def repo_field_fixes(benchmarks: list[dict]) -> list[tuple[str, str, str]]:
    fixes: list[tuple[str, str, str]] = []
    for row in benchmarks:
        if row.get("catalog_lifecycle") == "planned":
            continue
        rel = str(row.get("path") or "").strip()
        if not rel or rel == "unknown":
            continue
        repo = str(row.get("repo") or "lic")
        if repo == "benchmarks":
            continue
        if path_exists_under(ROOT, rel):
            fixes.append((row["id"], repo, "benchmarks"))
            row["repo"] = "benchmarks"
    return fixes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    fmt = load_format_module()
    text = CATALOG.read_text(encoding="utf-8")
    benchmarks = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    fixes = repo_field_fixes(benchmarks)
    print(f"repo field fixes: {len(fixes)}")
    for bid, old, new in fixes[:25]:
        print(f"  {bid}: {old} -> {new}")
    if len(fixes) > 25:
        print(f"  ... and {len(fixes) - 25} more")

    if args.dry_run and not args.write:
        return 0
    if not args.write:
        print("pass --write to update catalog.toml", file=sys.stderr)
        return 1

    header = fmt.load_header(text)
    footer = fmt.load_footer(text)
    if not footer:
        footer = (
            "\n[reporting]\n"
            'platforms = ["linux", "macos", "windows"]\n'
            "validity_required = true\n"
            'sota_policy = "best_competitor_lang_excludes_li"\n'
        )
    CATALOG.write_text(
        header + "\n\n".join(fmt.format_benchmark(b) for b in benchmarks) + footer
    )
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
