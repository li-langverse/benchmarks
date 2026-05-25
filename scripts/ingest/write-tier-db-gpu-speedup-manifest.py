#!/usr/bin/env python3
"""Write data/latest/tier-db-gpu-speedup.json for CI ingest (tier_db_gpu_speedup skeleton)."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/latest/tier-db-gpu-speedup.json"

SCENARIOS = [
    ("gpu_ann_speedup_10k", 10_000),
    ("gpu_ann_speedup_1m", 1_000_000),
]


def scenario_stub(sid: str, n: int) -> dict:
    return {
        "id": sid,
        "metric": "speedup_ratio",
        "unit": "ratio",
        "corpus_size": n,
        "fixed_recall_at_10": 0.95,
        "status": "stub",
        "engines": {"lidb_cpu": None, "lidb_gpu": None},
        "speedup_ratio": None,
        "ph_ids": ["PH-DB-G2"],
        "notes": f"GPU/CPU QPS ratio @ N={n}, recall@10 fixed",
    }


def build_manifest(*, profile: str, status: str) -> dict:
    ids = [s[0] for s in SCENARIOS]
    if profile == "ci":
        ids = ["gpu_ann_speedup_10k"]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "tier_db_gpu_speedup",
        "profile": profile,
        "status": status,
        "compare_oracle": "lidb_cpu_hnsw",
        "gpu_required": False,
        "nightly_optional": True,
        "sources": {
            "suite_toml": "benchmarks/tier_db_gpu_speedup/suite.toml",
            "defaults_toml": "benchmarks/tier_db_gpu_speedup/defaults.toml",
            "schema_sql": "benchmarks/tier_db_vector_ann/schema/vector-ann-v1.sql",
            "results_csv": "benchmarks/tier_db_gpu_speedup/results/latest.csv",
            "catalog_toml": "catalog.toml",
        },
        "scenarios": [scenario_stub(*next(s for s in SCENARIOS if s[0] == sid)) for sid in ids],
        "ci_ingest": {
            "artifact_path": "data/latest/tier-db-gpu-speedup.json",
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
