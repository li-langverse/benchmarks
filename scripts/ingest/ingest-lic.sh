#!/usr/bin/env bash
# Ingest lic benchmark CSV into data/latest/summary.json
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/../li}"
CSV="${1:-$LIC_ROOT/benchmarks/results/latest.csv}"
python3 "$ROOT/scripts/ingest/build_summary.py" "$LIC_ROOT" "$CSV"
"$ROOT/scripts/regression-check.sh"
