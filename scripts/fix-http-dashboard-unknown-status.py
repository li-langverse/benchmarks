#!/usr/bin/env python3
"""Mark tier-5 http linux charts/rows advisory when status/validity are unknown.

Competitor-only http snapshots (no li series) must not fail audit-dashboard-gaps
or inflate skip-row budgets from refresh-dashboard-completeness.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/latest/summary.json"
SOURCE = "http:competitor_only_or_harness_pending"


def patch_chart(ch: dict) -> bool:
    series = ch.get("series") or []
    has_li = any(s.get("lang") == "li" for s in series)
    st = ch.get("status")
    vs = ch.get("validity_status")
    if st not in (None, "", "unknown") and vs not in (None, "", "unknown"):
        return False
    if series and not has_li:
        ch["validity_status"] = "advisory"
        ch["validity_source"] = ch.get("validity_source") or SOURCE
        ch["status"] = "advisory"
        return True
    if st in (None, "", "unknown") or vs in (None, "", "unknown"):
        ch["validity_status"] = "advisory"
        ch["validity_source"] = ch.get("validity_source") or SOURCE
        ch["status"] = "advisory"
        return True
    return False


def patch_row(row: dict) -> bool:
    if row.get("category") != "http":
        return False
    st = row.get("status")
    vs = row.get("validity_status")
    if st not in (None, "", "unknown") and vs not in (None, "", "unknown"):
        return False
    row["validity_status"] = "advisory"
    row["validity_source"] = row.get("validity_source") or SOURCE
    row["status"] = "advisory"
    return True


def main() -> int:
    if not SUMMARY.is_file():
        print(f"missing {SUMMARY}", file=sys.stderr)
        return 1
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    charts_patched = 0
    for cat_data in (summary.get("categories") or {}).values():
        for ch in cat_data.get("charts") or []:
            if patch_chart(ch):
                charts_patched += 1
    rows_patched = sum(1 for row in summary.get("rows") or [] if patch_row(row))
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(
        f"fix-http-dashboard-unknown-status: charts={charts_patched} rows={rows_patched}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
