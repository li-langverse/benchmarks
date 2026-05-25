#!/usr/bin/env python3
"""Write data/latest/tier-db-registry.json for CI ingest (tier_db_registry skeleton)."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIER_ROOT = ROOT / "benchmarks/tier_db_registry"
OUT = ROOT / "data/latest/tier-db-registry.json"
SCENARIO_IDS = [
    "registry_publish",
    "registry_read_by_name",
    "registry_read_latest",
]
THRESHOLD = 1.2


def scenario_stub(sid: str) -> dict:
    notes = {
        "registry_publish": "P95 publish path: package + version + attestation insert",
        "registry_read_by_name": "P95 lookup by package name",
        "registry_read_latest": "P95 latest version for package name",
    }
    return {
        "id": sid,
        "metric": "latency_p95",
        "unit": "ms",
        "lower_is_better": True,
        "threshold_ratio_vs_postgres": THRESHOLD,
        "status": "stub",
        "engines": {"lidb": None, "postgres": None},
        "ratio_vs_postgres": None,
        "ph_ids": ["PH-DB-5"],
        "notes": notes.get(sid, ""),
    }


def build_manifest(*, profile: str, status: str) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "tier_db_registry",
        "profile": profile,
        "status": status,
        "compare_oracle": "postgres",
        "postgres_min_version": "15",
        "nightly_optional": True,
        "sources": {
            "suite_toml": "benchmarks/tier_db_registry/suite.toml",
            "defaults_toml": "benchmarks/tier_db_registry/defaults.toml",
            "schema_sql": "benchmarks/tier_db_registry/schema/registry-v1.sql",
            "results_csv": "benchmarks/tier_db_registry/results/latest.csv",
            "catalog_toml": "catalog.toml",
        },
        "scenarios": [scenario_stub(s) for s in SCENARIO_IDS],
        "ci_ingest": {
            "artifact_path": "data/latest/tier-db-registry.json",
            "merge_into_summary": False,
            "dashboard_section": "database",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="ci", choices=("ci", "nightly"))
    ap.add_argument("--stub", action="store_true", help="Mark manifest status stub (default)")
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
