#!/usr/bin/env bash
# CI nightly entry: full suite on Linux; core tiers on macOS/Windows.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
export LIC_ROOT LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
export LI_REPO_ROOT="$LIC_ROOT"
export BENCH_JOBS="${BENCH_JOBS:-$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)}"
export BENCH_MIN_RUNS="${BENCH_MIN_RUNS:-20}"
export BENCH_ADAPTIVE_RUNS="${BENCH_ADAPTIVE_RUNS:-1}"

if command -v clang-22 >/dev/null 2>&1; then
  export CC="${CC:-clang-22}"
  export CXX="${CXX:-clang++-22}"
elif command -v clang-18 >/dev/null 2>&1; then
  export CC="${CC:-clang-18}"
  export CXX="${CXX:-clang++-18}"
fi

log() { echo "==> $*"; }

case "$(uname -s)" in
  Linux*) log "nightly profile: full (Linux)"; export SKIP_EXPLOITS="${SKIP_EXPLOITS:-0}" ;;
  Darwin*) log "nightly profile: core (macOS)"; export SKIP_EXPLOITS=1 SKIP_TIER5_HTTP=1 ;;
  MINGW*|MSYS*|CYGWIN*|Windows*) log "nightly profile: core (Windows)"; export SKIP_EXPLOITS=1 SKIP_TIER5_HTTP=1 ;;
  *) log "nightly profile: core"; export SKIP_EXPLOITS=1 SKIP_TIER5_HTTP=1 ;;
esac

export BENCH_NIGHTLY=1
if [[ "${1:-}" == "tier" && -n "${2:-}" ]]; then
  export BENCHMARKS_CSV="$ROOT/results/tier-${2}.csv"
  mkdir -p "$(dirname "$BENCHMARKS_CSV")"
  exec "$ROOT/scripts/run-benchmark-tier-group.sh" "$2"
fi
export BENCHMARKS_CSV="${BENCHMARKS_CSV:-$ROOT/results/latest.csv}"
mkdir -p "$(dirname "$BENCHMARKS_CSV")"
exec "$ROOT/scripts/run-full-benchmark-suite.sh"

