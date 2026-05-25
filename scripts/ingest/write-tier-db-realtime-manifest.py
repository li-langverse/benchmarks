#!/usr/bin/env python3
"""Write data/latest/tier-db-realtime.json for CI ingest (tier_db_realtime skeleton)."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIER = "tier_db_realtime"
OUT = ROOT / "data/latest/tier-db-realtime.json"
SCENARIOS = [
    ("ws_publish_latency", "latency_p95", "ms", "WebSocket publish→client P95"),
]


def scenario_stub(sid: str, metric: str, unit: str, notes: str) -> dict:
    return {
        "id": sid,
        "metric": metric,
        "unit": unit,
        "lower_is_better": True,
        "threshold_ratio_vs_postgres": 1.2,
        "status": "stub",
        "engines": {"lidb": None, "postgres": None},
        "ratio_vs_postgres": None,
        "ph_ids": ["WP-N4", "PH-DB-RT"],
        "notes": notes,
    }


def build_manifest(*, profile: str, status: str) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": TIER,
        "profile": profile,
        "status": status,
        "compare_oracle": "postgres",
        "postgres_min_version": "15",
        "nightly_optional": True,
        "sources": {
            "suite_toml": f"benchmarks/{TIER}/suite.toml",
            "defaults_toml": f"benchmarks/{TIER}/defaults.toml",
            "schema_sql": f"benchmarks/{TIER}/schema/realtime-channel-v1.sql",
            "results_csv": f"benchmarks/{TIER}/results/latest.csv",
            "catalog_toml": "catalog.toml",
        },
        "scenarios": [scenario_stub(*s) for s in SCENARIOS],
        "ci_ingest": {
            "artifact_path": "data/latest/tier-db-realtime.json",
            "merge_into_summary": False,
            "dashboard_section": "database",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="ci", choices=("ci", "nightly"))
    ap.add_argument("--stub", action="store_true")
    ap.add_argument("--status", default="stub")
    args = ap.parse_args()
    status = "stub" if args.stub else args.status
    manifest = build_manifest(profile=args.profile, status=status)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} (profile={args.profile}, status={status})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
