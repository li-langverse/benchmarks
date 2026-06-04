#!/usr/bin/env python3
"""Mark competitive-vertical catalog rows honest (no bogus tier1/tier2 path reuse).

Sub-phase B (bio_*, drug_*): ``path = unknown``, ``catalog_lifecycle = planned``,
``variant = vertical_stub``.

Sub-phase C: other ``algo_registry`` rows whose id does not match the path stem and
have no dedicated ``benchmarks/workloads/*/id`` directory.

Usage:
  python3 scripts/catalog/mark-catalog-vertical-stubs.py --dry-run
  python3 scripts/catalog/mark-catalog-vertical-stubs.py --write
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
WORKLOADS = ROOT / "benchmarks" / "workloads"
VENDOR_LIS = ROOT / "vendor" / "lis-tier5"

PHASE_B_PREFIXES = ("bio_", "drug_")
PHASE_C_REMAP_PREFIXES = ("am_", "pde_", "robo_")

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
    if repo == "lic":
        lic = Path(__import__("os").environ.get("LIC_ROOT", str(ROOT.parent / "lic")))
        return (lic / rel).is_dir() or (lic / rel).is_file()
    return False


def has_dedicated_workload(bid: str) -> bool:
    if not WORKLOADS.is_dir():
        return False
    for tier in WORKLOADS.iterdir():
        if tier.is_dir() and (tier / bid).is_dir():
            return True
    return False


def should_mark_planned(b: dict) -> str | None:
    bid = b["id"]
    if str(b.get("catalog_lifecycle") or "").lower() == "planned":
        return None
    path = str(b.get("path") or "")
    variant = str(b.get("variant") or "")

    if bid.startswith(PHASE_B_PREFIXES) and variant == "algo_registry":
        stem = Path(path).name if path and path != "unknown" else ""
        if stem and stem != bid:
            return "phase_b_vertical"

    repo = str(b.get("repo") or "lic")

    if variant != "algo_registry":
        if (
            path
            and path != "unknown"
            and not has_dedicated_workload(bid)
            and not path_exists_for_repo(repo, path)
            and bid not in ("tier0_stability",)
        ):
            return "phase_c_missing_harness"
        return None

    stem = Path(path).name if path and path != "unknown" else ""
    if bid.startswith(PHASE_C_REMAP_PREFIXES) and stem and stem != bid:
        return "phase_c_algo_registry_remap"
    if stem and stem != bid and not has_dedicated_workload(bid):
        return "phase_c_algo_registry_remap"
    return None


def apply_marks(benchmarks: list[dict]) -> list[tuple[str, str]]:
    marks: list[tuple[str, str]] = []
    for b in benchmarks:
        reason = should_mark_planned(b)
        if not reason:
            continue
        marks.append((b["id"], reason))
        b["path"] = "unknown"
        b["catalog_lifecycle"] = "planned"
        b["variant"] = "vertical_stub"
        if not b.get("size_label"):
            b["size_label"] = "competitive vertical stub"
    return marks


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
    marks = apply_marks(benchmarks)
    print(f"vertical stubs marked planned: {len(marks)}")
    for bid, reason in marks:
        print(f"  {bid} ({reason})")

    if args.dry_run or not marks:
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
