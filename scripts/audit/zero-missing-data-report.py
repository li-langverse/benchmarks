#!/usr/bin/env python3
"""Report every gap blocking zero-missing benchmark dashboard data."""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUMMARY = ROOT / "data/latest/summary.json"
CATALOG = ROOT / "catalog.toml"
CATALOG_AUDIT = ROOT / "data/latest/catalog-audit.json"
CSV_PATH = Path(
    __import__("os").environ.get("BENCHMARKS_CSV", str(ROOT / "results/latest.csv"))
)
OUT = ROOT / "data/latest/zero-missing-data-report.json"


def load_catalog_entries() -> list[dict]:
    """Minimal TOML id/base_id parse for coverage checks."""
    text = CATALOG.read_text(encoding="utf-8")
    entries: list[dict] = []
    cur: dict = {}
    for line in text.splitlines():
        m = re.match(r'^id\s*=\s*"([^"]+)"', line)
        if m:
            if cur:
                entries.append(cur)
            cur = {"id": m.group(1)}
            continue
        m = re.match(r'^base_id\s*=\s*"([^"]+)"', line)
        if m and cur:
            cur["base_id"] = m.group(1)
    if cur:
        entries.append(cur)
    return entries


def csv_benchmarks() -> set[str]:
    if not CSV_PATH.is_file():
        return set()
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        return {row["benchmark"] for row in csv.DictReader(f)}


def catalog_ids_without_csv(entries: list[dict], csv_b: set[str]) -> list[str]:
    missing: list[str] = []
    for e in entries:
        bid = e["id"]
        base = e.get("base_id") or bid
        if bid in csv_b or base in csv_b:
            continue
        missing.append(bid)
    return sorted(missing)


def main() -> int:
    report: dict = {"schema": "benchmarks/zero-missing-data-report/v1"}

    entries = load_catalog_entries()
    csv_b = csv_benchmarks()
    report["catalog_id_count"] = len(entries)
    report["csv_benchmark_count"] = len(csv_b)
    report["catalog_ids_without_csv"] = catalog_ids_without_csv(entries, csv_b)

    if SUMMARY.is_file():
        summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
        rows = summary.get("rows", [])
        report["summary_row_count"] = len(rows)
        report["summary_status"] = dict(Counter(r.get("status") for r in rows))
        report["skip_rows"] = [
            {
                "id": r.get("id"),
                "package": r.get("package"),
                "tier": r.get("tier"),
                "os": r.get("os"),
            }
            for r in rows
            if r.get("status") == "skip"
        ]
        report["skip_row_count"] = len(report["skip_rows"])
        report["measured_rows"] = sum(
            1 for r in rows if r.get("measurement_state") == "measured"
        )
    else:
        report["summary_missing"] = True

    if CATALOG_AUDIT.is_file():
        audit = json.loads(CATALOG_AUDIT.read_text(encoding="utf-8"))
        for key in (
            "harness_pending_count",
            "harness_pending_sample",
            "workload_dir_missing_count",
            "workload_dir_missing_sample",
            "missing_problem_size_count",
            "missing_problem_size_sample",
        ):
            if key in audit:
                report[key] = audit[key]

    lig_gpu = ROOT / "data/latest/lig-gpu-matrix.json"
    if lig_gpu.is_file():
        g = json.loads(lig_gpu.read_text(encoding="utf-8"))
        report["lig_gpu_contributions"] = len(g.get("contributions", []))
        report["lig_gpu_open_slots"] = len(g.get("open_slots", []))

    report["blocking_counts"] = {
        "summary_skip_rows": report.get("skip_row_count", 0),
        "catalog_without_csv": len(report.get("catalog_ids_without_csv", [])),
        "harness_pending": report.get("harness_pending_count", 0),
        "workload_dir_missing": report.get("workload_dir_missing_count", 0),
    }
    report["zero_missing_ready"] = all(
        v == 0 for v in report["blocking_counts"].values()
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {OUT}")
    print("blocking:", report["blocking_counts"])
    print("zero_missing_ready:", report["zero_missing_ready"])
    if report.get("skip_row_count", 0):
        print(f"  (see skip_rows in JSON, count={report['skip_row_count']})")

    return 0 if report["zero_missing_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
