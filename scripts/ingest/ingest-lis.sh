#!/usr/bin/env bash
# Ingest lis tier5_http CSV (and refresh lic data).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"

if [[ ! -f "$LIS_ROOT/results/latest.csv" ]]; then
  echo "Generating lis stub bench CSV..."
  (cd "$LIS_ROOT" && python3 benchmarks/tier5_http/harness/bench_http.py static_small --profile ci)
  (cd "$LIS_ROOT" && python3 benchmarks/tier5_http/harness/bench_http.py keepalive_pipelining --profile ci 2>/dev/null || true)
fi

"$ROOT/scripts/ingest/ingest-lic.sh"
