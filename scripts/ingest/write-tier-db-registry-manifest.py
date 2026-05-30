#!/usr/bin/env python3
"""Write data/latest/tier-db-registry.json for CI ingest (tier_db_registry)."""
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
PH_GATE = "PH-DB-5"
PH_DEPENDENCIES = ["PH-DB-1", "PH-DB-4"]

NOTES = {
    "registry_publish": "P95 publish path: package + version + attestation insert",
    "registry_read_by_name": "P95 lookup by package name",
    "registry_read_latest": "P95 latest version for package name",
}


def scenario_stub(sid: str, *, status: str = "stub") -> dict:
    return {
        "id": sid,
        "metric": "latency_p95",
        "unit": "ms",
        "lower_is_better": True,
        "threshold_ratio_vs_postgres": THRESHOLD,
        "status": status,
        "engines": {"lidb": None, "postgres": None},
        "ratio_vs_postgres": None,
        "ph_ids": [PH_GATE],
        "ph_dependencies": PH_DEPENDENCIES,
        "notes": NOTES.get(sid, ""),
    }


def scenario_from_harness_row(sid: str, row: dict) -> dict:
    p95 = row.get("value")
    return {
        "id": sid,
        "metric": "latency_p95",
        "unit": "ms",
        "lower_is_better": True,
        "threshold_ratio_vs_postgres": THRESHOLD,
        "status": "unknown",
        "engines": {
            "lidb": None,
            "postgres": None,
            "sqlite_stub": {"p95_ms": p95, "p50_ms": row.get("p50_ms")},
        },
        "ratio_vs_postgres": None,
        "ph_ids": [PH_GATE],
        "ph_dependencies": PH_DEPENDENCIES,
        "notes": (
            f"{NOTES.get(sid, '')} — sqlite_stub timing only; "
            "awaiting lidb vs Postgres P95"
        ),
    }


def scenario_from_compare_row(row: dict) -> dict:
    ratio = row.get("ratio_vs_postgres")
    status = row.get("status") or "unknown"
    if ratio is not None and status not in ("passed", "failed"):
        status = "passed" if ratio <= THRESHOLD else "failed"
    return {
        "id": row["benchmark"],
        "metric": "latency_p95",
        "unit": "ms",
        "lower_is_better": True,
        "threshold_ratio_vs_postgres": THRESHOLD,
        "status": status,
        "engines": {
            "lidb": {"p95_ms": row.get("lidb_p95_ms"), "p50_ms": row.get("lidb_p50_ms")},
            "postgres": {"p95_ms": row.get("postgres_p95_ms")},
        },
        "ratio_vs_postgres": ratio,
        "ph_ids": [PH_GATE],
        "ph_dependencies": PH_DEPENDENCIES,
        "notes": NOTES.get(row["benchmark"], ""),
    }



def build_manifest(
    *,
    profile: str,
    status: str,
    harness: dict | None = None,
) -> dict:
    scenarios: list[dict]
    engine_mode = None
    if harness and harness.get("rows"):
        by_id = {r["benchmark"]: r for r in harness["rows"]}
        if harness.get("engine_mode") in ("lidb_vs_postgres", "lidb_only"):
            scenarios = [
                scenario_from_compare_row(by_id[sid])
                if sid in by_id
                else scenario_stub(sid, status="unknown")
                for sid in SCENARIO_IDS
            ]
        else:
            scenarios = [
                scenario_from_harness_row(sid, by_id[sid])
                if sid in by_id
                else scenario_stub(sid, status="unknown")
                for sid in SCENARIO_IDS
            ]
        engine_mode = harness.get("engine_mode", "sqlite_local_stub")
    else:
        scenarios = [scenario_stub(s) for s in SCENARIO_IDS]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "tier_db_registry",
        "profile": profile,
        "status": status,
        "compare_oracle": "postgres",
        "postgres_min_version": "15",
        "nightly_optional": True,
        "engine_mode": engine_mode,
        "ph_plan": {
            "PH-DB-1": "lidb engine + 001_registry.sql (schema parity)",
            "PH-DB-4": "lip registry API + central registry DB",
            "PH-DB-5": "tier_db_registry P95 vs Postgres 15+ (this tier)",
        },
        "sources": {
            "suite_toml": "benchmarks/tier_db_registry/suite.toml",
            "defaults_toml": "benchmarks/tier_db_registry/defaults.toml",
            "schema_sql": "benchmarks/tier_db_registry/schema/registry-v1.sql",
            "schema_sqlite_stub": "benchmarks/tier_db_registry/schema/registry-sqlite-v1.sql",
            "fixtures_seed": "benchmarks/tier_db_registry/fixtures/seed.toml",
            "harness_py": "benchmarks/tier_db_registry/harness/registry_oltp_stub.py",
            "results_csv": "benchmarks/tier_db_registry/results/latest.csv",
            "catalog_toml": "catalog.toml",
        },
        "scenarios": scenarios,
        "ci_ingest": {
            "artifact_path": "data/latest/tier-db-registry.json",
            "merge_into_summary": False,
            "dashboard_section": "database",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="ci", choices=("ci", "nightly"))
    ap.add_argument("--stub", action="store_true", help="Mark manifest status stub")
    ap.add_argument("--status", default=None)
    ap.add_argument(
        "--from-harness",
        type=Path,
        help="Harness JSON from registry_oltp_stub.py (--run-timing)",
    )
    ap.add_argument(
        "--from-compare",
        type=Path,
        help="Compare JSON from lidb/scripts/bench/registry_oltp_compare.py",
    )
    args = ap.parse_args()

    harness: dict | None = None
    if args.from_compare:
        harness = json.loads(args.from_compare.read_text(encoding="utf-8"))
    elif args.from_harness:
        harness = json.loads(args.from_harness.read_text(encoding="utf-8"))

    if args.status:
        status = args.status
    elif args.stub or harness is None:
        status = "stub"
    elif harness and harness.get("engine_mode") == "lidb_vs_postgres":
        rows = harness.get("rows") or []
        if rows and all(r.get("status") == "passed" for r in rows if r.get("ratio_vs_postgres") is not None):
            status = "passed"
        elif any(r.get("ratio_vs_postgres") is not None for r in rows):
            status = "failed"
        else:
            status = "unknown"
    else:
        status = "unknown"

    manifest = build_manifest(profile=args.profile, status=status, harness=harness)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} (profile={args.profile}, status={status})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
