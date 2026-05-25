#!/usr/bin/env python3
"""Write data/latest/tier-db-token-efficiency.json for CI ingest."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIER_ROOT = ROOT / "benchmarks/tier_db_token_efficiency"
COMPUTE = TIER_ROOT / "compute_tokens.py"
OUT = ROOT / "data/latest/tier-db-token-efficiency.json"
SCENARIOS = TIER_ROOT / "scenarios.json"


def run_compute() -> dict:
    tmp = OUT.with_suffix(".compute.json")
    subprocess.run(
        [sys.executable, str(COMPUTE), str(tmp)],
        check=True,
        cwd=str(ROOT),
    )
    return json.loads(tmp.read_text(encoding="utf-8"))


def build_manifest(*, profile: str, report: dict) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "tier_db_token_efficiency",
        "profile": profile,
        "status": "measured",
        "metric": "tokens",
        "encoder": report.get("encoder"),
        "baseline_surface": report.get("baseline_surface", "sql"),
        "sources": {
            "suite_toml": "benchmarks/tier_db_token_efficiency/suite.toml",
            "scenarios_json": "benchmarks/tier_db_token_efficiency/scenarios.json",
            "compute_script": "benchmarks/tier_db_token_efficiency/compute_tokens.py",
            "ecosystem_doc": "docs/ecosystem/tier-db-token-efficiency.md",
            "lidb_audit": "lidb/docs/liq-token-efficiency-audit.md",
        },
        "summary": report.get("summary", {}),
        "scenarios": report.get("scenarios", []),
        "ci_ingest": {
            "artifact_path": "data/latest/tier-db-token-efficiency.json",
            "merge_into_summary": False,
            "dashboard_section": "database",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="ci", choices=("ci", "nightly"))
    args = ap.parse_args()
    report = run_compute()
    manifest = build_manifest(profile=args.profile, report=report)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    compute_tmp = OUT.with_suffix(".compute.json")
    if compute_tmp.exists():
        compute_tmp.unlink()
    print(f"wrote {OUT} (encoder={manifest.get('encoder')}, n={manifest['summary'].get('scenario_count')})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
