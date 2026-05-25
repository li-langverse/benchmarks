#!/usr/bin/env python3
"""Write data/latest/tier-db-graph-registry.json for CI ingest (tier_db_graph_registry skeleton)."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/latest/tier-db-graph-registry.json"
SCENARIO_IDS = ["graph_dep_closure", "graph_cycle_detect"]
THRESHOLD = 1.2


def scenario_stub(sid: str) -> dict:
    notes = {
        "graph_dep_closure": "Transitive package_deps closure from root package",
        "graph_cycle_detect": "Cycle detection on synthetic registry dep DAG",
    }
    return {
        "id": sid,
        "metric": "latency_p95",
        "unit": "ms",
        "lower_is_better": True,
        "threshold_ratio_vs_oracle": THRESHOLD,
        "status": "stub",
        "engines": {"lidb_cte": None, "postgres_age": None, "kuzu": None},
        "ratio_vs_oracle": None,
        "ph_ids": ["PH-DB-G1"],
        "notes": notes.get(sid, ""),
    }


def build_manifest(*, profile: str, status: str) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "tier_db_graph_registry",
        "profile": profile,
        "status": status,
        "compare_oracle": "postgres_age",
        "postgres_min_version": "15",
        "nightly_optional": True,
        "sources": {
            "suite_toml": "benchmarks/tier_db_graph_registry/suite.toml",
            "defaults_toml": "benchmarks/tier_db_graph_registry/defaults.toml",
            "schema_sql": "benchmarks/tier_db_graph_registry/schema/graph-registry-v1.sql",
            "base_schema_sql": "benchmarks/tier_db_registry/schema/registry-v1.sql",
            "results_csv": "benchmarks/tier_db_graph_registry/results/latest.csv",
            "catalog_toml": "catalog.toml",
        },
        "scenarios": [scenario_stub(s) for s in SCENARIO_IDS],
        "ci_ingest": {
            "artifact_path": "data/latest/tier-db-graph-registry.json",
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
