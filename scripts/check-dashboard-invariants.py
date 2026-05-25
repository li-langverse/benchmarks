#!/usr/bin/env python3
"""CI gate: dashboard summary.json and catalog.toml invariants."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.toml"
SUMMARY = ROOT / "data/latest/summary.json"
MIN_ROWS = 150
BANNED_STUB_IDS = frozenset({"lig_viewport_stub", "li_math_gemm_stub"})
REQUIRED_PILLARS = frozenset(
    {
        "numerics",
        "compiler",
        "server",
        "physics",
        "proofs",
        "security",
        "database",
        "graphics",
        "tooling",
    }
)
REQUIRED_ROW_KEYS = ("validity_status", "ratio_vs_sota")


def fail(msg: str) -> None:
    print(f"check-dashboard-invariants: FAIL {msg}", file=sys.stderr)
    sys.exit(1)


def chart_index(summary: dict) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for cat in summary.get("categories", {}).values():
        for ch in cat.get("charts", []):
            bid = ch.get("id")
            if bid:
                out[bid] = ch
    return out


def main() -> int:
    import tomllib

    if not CATALOG.is_file():
        fail(f"missing {CATALOG}")
    if not SUMMARY.is_file():
        fail(f"missing {SUMMARY}")

    catalog = tomllib.loads(CATALOG.read_text())
    benches = catalog.get("benchmark", [])
    catalog_ids = [b["id"] for b in benches]
    catalog_set = set(catalog_ids)

    summary = json.loads(SUMMARY.read_text())
    rows = summary.get("rows", [])
    row_by_bench = {r["benchmark"]: r for r in rows}

    if len(catalog_ids) != len(catalog_set):
        fail("duplicate catalog ids")

    if len(rows) < MIN_ROWS:
        fail(f"summary rows {len(rows)} < minimum {MIN_ROWS}")

    if len(rows) != len(catalog_set):
        fail(f"row count {len(rows)} != catalog count {len(catalog_set)}")

    missing = catalog_set - set(row_by_bench)
    if missing:
        fail(f"catalog ids missing from summary.rows: {sorted(missing)[:5]} … ({len(missing)} total)")

    extra = set(row_by_bench) - catalog_set
    if extra:
        fail(f"summary rows not in catalog: {sorted(extra)[:5]} … ({len(extra)} total)")

    banned_in_catalog = catalog_set & BANNED_STUB_IDS
    if banned_in_catalog:
        fail(f"banned stub ids in catalog: {sorted(banned_in_catalog)}")

    stub_suffix = [i for i in catalog_ids if i.endswith("_stub")]
    if stub_suffix:
        fail(f"*_stub catalog ids not allowed: {stub_suffix[:5]}")

    policy = summary.get("reporting", {}).get("sota_policy")
    if policy != "best_competitor_lang_excludes_li":
        fail(f"unexpected sota_policy: {policy!r}")

    for row in rows:
        if row.get("sota_lang") == "li":
            fail(f"sota_lang=li on {row['benchmark']}")
        for key in REQUIRED_ROW_KEYS:
            if key not in row:
                fail(f"row {row['benchmark']} missing {key}")

    pillars = set(summary.get("pillars", {}))
    if pillars != REQUIRED_PILLARS:
        fail(f"pillars mismatch: have {sorted(pillars)} need {sorted(REQUIRED_PILLARS)}")

    charts = chart_index(summary)
    for b in benches:
        ps = str(b.get("problem_size") or "").strip()
        if not ps:
            continue
        bid = b["id"]
        sl = (charts.get(bid) or {}).get("size_label") or row_by_bench.get(bid, {}).get(
            "size_label"
        )
        if not sl or sl == "harness pending":
            # allow pending only when path is unknown (stub harness)
            if b.get("path") != "unknown":
                fail(f"{bid}: problem_size set but size_label missing on measured path")

    print(
        f"PASS check-dashboard-invariants "
        f"({len(rows)} rows, {len(pillars)} pillars, policy={policy})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
