#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export BENCH_TIER_DB_ROOT="$ROOT" BENCH_PROFILE=ci
bash "${LIDB_ROOT:-$ROOT/../lidb}/scripts/bench/tier_db_csv.sh"
python3 "$ROOT/scripts/ingest/build_summary.py" "${LIC_ROOT:-$ROOT/../lic}" "${LIS_ROOT:-$ROOT/../lis}"
