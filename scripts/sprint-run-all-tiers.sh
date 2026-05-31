#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"
export LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
export BENCH_NIGHTLY=1
export BENCH_MIN_RUNS="${BENCH_MIN_RUNS:-2}"
export BENCH_RUNS="${BENCH_RUNS:-2}"
export SKIP_EXPLOITS="${SKIP_EXPLOITS:-1}"

tiers=(tier0 tier1 tier2-md tier2-pde tier2-mech tier3 tier5 tier7)
for t in "${tiers[@]}"; do
  echo "=== $t ==="
  if ! ./scripts/run-benchmark-tier-group.sh "$t"; then
    echo "WARN: tier group $t failed" >&2
  fi
done

./scripts/merge-benchmark-tier-csvs.sh results
wc -l results/latest.csv
./scripts/ingest/ingest-lic.sh
python3 scripts/audit/zero-missing-data-report.py | grep blocking || true
python3 scripts/check-zero-missing-data.py || true
