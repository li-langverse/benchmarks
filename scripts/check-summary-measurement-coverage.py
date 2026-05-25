#!/usr/bin/env python3
"""CI gate: summary.json must not regress to all-unknown tier colors."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/latest/summary.json"

MIN_COLORED_ABSOLUTE = 5
MIN_COLORED_FRACTION_MEASURED = 0.10
COLORED = frozenset({"green", "yellow", "red"})
HARNESS_IDS = ("simd_dot", "matmul_naive", "horner_pure_li")


def fail(msg: str) -> None:
    print(f"check-summary-measurement-coverage: FAIL {msg}", file=sys.stderr)
    sys.exit(1)


def tier_colored_total(tier_counts: dict) -> int:
    total = 0
    for bucket in tier_counts.values():
        if not isinstance(bucket, dict):
            continue
        for color in COLORED:
            total += int(bucket.get(color, 0) or 0)
    return total


def resolve_lic_csv(summary: dict) -> Path | None:
    lic_root = os.environ.get("LIC_ROOT", "").strip()
    if lic_root:
        candidate = Path(lic_root) / "benchmarks/results/latest.csv"
        if candidate.is_file():
            return candidate
    src = (summary.get("sources") or {}).get("lic_csv")
    if src:
        p = Path(src)
        if p.is_file():
            return p
        alt = ROOT / "lic" / "benchmarks/results/latest.csv"
        if alt.is_file():
            return alt
    return None


def main() -> int:
    if not SUMMARY.is_file():
        fail(f"missing {SUMMARY}")

    summary = json.loads(SUMMARY.read_text())
    rows = summary.get("rows", [])
    if not rows:
        fail("summary.rows is empty")

    colored_count = sum(1 for r in rows if r.get("status") in COLORED)
    measured_rows = [r for r in rows if r.get("measurement_state") == "measured"]
    if measured_rows:
        required = max(
            MIN_COLORED_ABSOLUTE,
            int(len(measured_rows) * MIN_COLORED_FRACTION_MEASURED + 0.999),
        )
        scope = f"{len(measured_rows)} measured rows"
    else:
        required = MIN_COLORED_ABSOLUTE
        scope = f"{len(rows)} rows (no measurement_state)"

    if colored_count < required:
        fail(
            f"only {colored_count} rows with status in {sorted(COLORED)}; "
            f"need >= {required} for {scope}"
        )

    tier_total = tier_colored_total(summary.get("tier_counts") or {})
    if tier_total < 1:
        fail(
            f"tier_counts green+yellow+red sum is {tier_total}; need >= 1 globally"
        )

    lic_csv = resolve_lic_csv(summary)
    if lic_csv:
        sys.path.insert(0, str(ROOT / "scripts/ingest"))
        from build_summary import has_csv_rows, load_catalog, merge_csv_rows

        catalog = load_catalog()
        raw = merge_csv_rows([lic_csv])
        row_by_bench = {r["benchmark"]: r for r in rows}
        bad: list[str] = []
        for bench_id in HARNESS_IDS:
            cfg = catalog.get(bench_id)
            if not cfg:
                continue
            if not has_csv_rows(raw, bench_id, cfg):
                continue
            row = row_by_bench.get(bench_id)
            if not row:
                bad.append(f"{bench_id}: missing summary row")
            elif row.get("status") == "unknown":
                bad.append(f"{bench_id}: CSV present but status unknown")
        if bad:
            fail("; ".join(bad))

    print(
        "PASS check-summary-measurement-coverage "
        f"({colored_count} colored rows, tier colored sum={tier_total}"
        + (f", lic_csv={lic_csv}" if lic_csv else "")
        + ")"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
