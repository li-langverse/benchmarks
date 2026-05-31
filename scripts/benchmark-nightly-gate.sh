#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"
export LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
export SKIP_EXPLOITS="${SKIP_EXPLOITS:-1}"
export SKIP_TIER5_HTTP="${SKIP_TIER5_HTTP:-1}"
export BENCH_MIN_RUNS="${BENCH_MIN_RUNS:-3}"
export BENCH_RUNS="${BENCH_RUNS:-3}"
if [[ "${BENCHMARK_NIGHTLY_GATE_NATIVE:-}" != "1" ]] && command -v wsl >/dev/null 2>&1 && ! grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null; then
  wsl bash -lc "cd /mnt/c/Users/Julian/Documents/Programming/li/benchmarks && BENCHMARK_NIGHTLY_GATE_NATIVE=1 bash scripts/benchmark-nightly-gate.sh"
  exit $?
fi
./scripts/run-benchmark-ci-nightly.sh
test -s results/latest.csv
python3 scripts/check-reporting-platforms.py
python3 scripts/check-dashboard-invariants.py
echo benchmark-nightly-gate-OK
