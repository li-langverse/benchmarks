#!/usr/bin/env bash
# Ingest lis tier5_http CSV (and refresh lic data when present).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
VENDOR_ROOT="${LIS_VENDOR_ROOT:-$ROOT/vendor/lis-tier5}"
export LIS_VENDOR_ROOT="$VENDOR_ROOT"

run_bench() {
  local root="$1"
  if [[ -f "$root/benchmarks/tier5_http/harness/bench_http.py" ]]; then
    (cd "$root" && python3 benchmarks/tier5_http/harness/bench_http.py --profile ci)
    return 0
  fi
  return 1
}

if [[ ! -f "$LIS_ROOT/results/latest.csv" ]]; then
  if run_bench "$LIS_ROOT"; then
    :
  elif run_bench "$VENDOR_ROOT"; then
    LIS_ROOT="$VENDOR_ROOT"
  else
    echo "ingest-lis: no lis CSV and bench_http unavailable" >&2
    exit 1
  fi
fi

export LIS_ROOT
"$ROOT/scripts/ingest/ingest-lic.sh"
