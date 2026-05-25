#!/usr/bin/env python3
"""Write data/latest/tier-db-vector-ann.json for CI ingest (tier_db_vector_ann skeleton)."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/latest/tier-db-vector-ann.json"

SCENARIOS = [
    ("ann_recall_at_10_10k", "recall_at_10", "ratio", 10_000),
    ("ann_qps_10k", "queries_per_sec", "qps", 10_000),
    ("ann_recall_at_10_1m", "recall_at_10", "ratio", 1_000_000),
]


def scenario_stub(sid: str, metric: str, unit: str, n: int) -> dict:
    return {
        "id": sid,
        "metric": metric,
        "unit": unit,
        "corpus_size": n,
        "dim": 128,
        "status": "stub",
        "engines": {"lidb": None, "faiss_cpu": None, "lidb_gpu": None},
        "recall_at_10": None,
        "ph_ids": ["PH-DB-8", "PH-DB-G2"],
        "notes": f"ANN @ N={n}, k=10",
    }


def build_manifest(*, profile: str, status: str) -> dict:
    ids = [s[0] for s in SCENARIOS]
    if profile == "ci":
        ids = [s[0] for s in SCENARIOS if s[0] != "ann_recall_at_10_1m"]
    scenarios = [scenario_stub(*next(s for s in SCENARIOS if s[0] == sid)) for sid in ids]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "tier_db_vector_ann",
        "profile": profile,
        "status": status,
        "compare_oracle": "faiss_cpu",
        "nightly_optional": True,
        "sources": {
            "suite_toml": "benchmarks/tier_db_vector_ann/suite.toml",
            "defaults_toml": "benchmarks/tier_db_vector_ann/defaults.toml",
            "schema_sql": "benchmarks/tier_db_vector_ann/schema/vector-ann-v1.sql",
            "results_csv": "benchmarks/tier_db_vector_ann/results/latest.csv",
            "catalog_toml": "catalog.toml",
        },
        "scenarios": scenarios,
        "ci_ingest": {
            "artifact_path": "data/latest/tier-db-vector-ann.json",
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
