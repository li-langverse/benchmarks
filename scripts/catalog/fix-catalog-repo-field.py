#!/usr/bin/env python3
"""Set catalog.toml ``repo = \"benchmarks\"`` when the path exists under this repo (ADR).

Also normalizes ``repo = \"lis\"`` tier-5 scenario paths to vendor layout
(``benchmarks/tier5_http/scenarios/…``, not ``benchmarks/workloads/tier5_http/…``).

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


def load_header(text: str) -> str:
    idx = text.find("[[benchmark]]")
    return text[:idx].rstrip() + "\n\n" if idx != -1 else ""


def load_footer(text: str) -> str:
    """Preserve trailing TOML tables (e.g. [reporting]) after [[benchmark]] blocks."""
    last = text.rfind("[[benchmark]]")
    if last < 0:
        return ""
    tail = text[last:]
    end = tail.find("\n\n[")
    if end < 0:
        return ""
    return tail[end:].lstrip("\n")


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


def path_exists_for_repo(repo: str, rel: str) -> bool:
    if not rel or rel == "unknown":
        return False
    if repo == "benchmarks":
        return (ROOT / rel).is_dir() or (ROOT / rel).is_file()
    if repo == "lis" and VENDOR_LIS.is_dir():
        return (VENDOR_LIS / rel).is_dir() or (VENDOR_LIS / rel).is_file()
    return False


def apply_fixes(benchmarks: list[dict]) -> list[tuple[str, str, str]]:
    fixes: list[tuple[str, str, str]] = []
    for b in benchmarks:
        bid = b["id"]
        repo = str(b.get("repo") or "lic")
        path = str(b.get("path") or "")
        if not path or path == "unknown":
            continue

        if path.startswith("benchmarks/workloads/tier5_http/"):
            new_path = path.replace(
                "benchmarks/workloads/tier5_http/", "benchmarks/tier5_http/", 1
            )
            if new_path != path and path_exists_for_repo("lis", new_path):
                fixes.append((bid, f"path {path}", f"path {new_path}"))
                b["path"] = new_path
                path = new_path

        if (
            repo == "lis"
            and b.get("catalog_lifecycle") == "planned"
            and path == "unknown"
            and (VENDOR_LIS / f"benchmarks/tier5_http/scenarios/{bid}").is_dir()
        ):
            new_path = f"benchmarks/tier5_http/scenarios/{bid}"
            fixes.append((bid, "restore lis tier5", new_path))
            b["path"] = new_path
            b.pop("catalog_lifecycle", None)
            if b.get("variant") == "vertical_stub":
                b["variant"] = "algo_registry"
            if b.get("size_label") == "competitive vertical stub":
                b.pop("size_label", None)
            continue

        if bid == "proxy_loopback" and path == "packages/li-net-httpd":
            new_path = "benchmarks/tier5_http/scenarios/proxy_loopback"
            if path_exists_for_repo("lis", new_path):
                fixes.append((bid, f"repo={repo} path={path}", f"repo=lis path={new_path}"))
                b["repo"] = "lis"
                b["path"] = new_path
            continue

        if repo == "lic" and (ROOT / path).is_dir():
            fixes.append((bid, "repo=lic", "repo=benchmarks"))
            b["repo"] = "benchmarks"

    return fixes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and not args.write:
        print("pass --dry-run or --write", file=sys.stderr)
        return 1

    import tomllib

    text = CATALOG.read_text(encoding="utf-8")
    benchmarks = [dict(b) for b in tomllib.loads(text).get("benchmark", [])]
    fixes = apply_fixes(benchmarks)
    print(f"repo/path fixes: {len(fixes)}")
    for row in fixes[:25]:
        print(f"  {row[0]}: {row[1]} -> {row[2]}")
    if len(fixes) > 25:
        print(f"  ... and {len(fixes) - 25} more")

    if args.dry_run or not fixes:
        return 0
    header = load_header(text)
    footer = load_footer(text)
    body = header + "\n\n".join(format_benchmark(b) for b in benchmarks)
    if footer:
        body += "\n\n" + footer.rstrip() + "\n"
    else:
        body += "\n"
    CATALOG.write_text(body, encoding="utf-8")
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
