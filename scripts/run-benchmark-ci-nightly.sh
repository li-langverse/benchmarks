#!/usr/bin/env bash
# CI nightly entry: full suite on Linux; tier 0–3 + 1/2 on macOS/Windows (no tier-5 oracles).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
export LIC_ROOT LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
export LI_REPO_ROOT="$LIC_ROOT"
export BENCH_RUNS="${BENCH_RUNS:-6}"
export BENCH_MIN_RUNS="${BENCH_MIN_RUNS:-6}"
export BENCH_SUBSEC_MIN_RUNS="${BENCH_SUBSEC_MIN_RUNS:-20}"
export BENCH_ADAPTIVE_RUNS="${BENCH_ADAPTIVE_RUNS:-1}"
export BENCH_JOBS="${BENCH_JOBS:-$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)}"

if command -v clang-22 >/dev/null 2>&1; then
  export CC="${CC:-clang-22}"
  export CXX="${CXX:-clang++-22}"
elif command -v clang-18 >/dev/null 2>&1; then
  export CC="${CC:-clang-18}"
  export CXX="${CXX:-clang++-18}"
fi

log() { echo "==> $*"; }

case "$(uname -s)" in
  Linux*)
    log "nightly profile: full (Linux)"
    export SKIP_EXPLOITS="${SKIP_EXPLOITS:-0}"
    exec "$ROOT/scripts/run-full-benchmark-suite.sh"
    ;;
  Darwin*)
    log "nightly profile: core (macOS — no tier-5 HTTP oracles)"
    export SKIP_EXPLOITS=1
    export SKIP_TIER5_HTTP=1
    ;;
  MINGW*|MSYS*|CYGWIN*|Windows*)
    log "nightly profile: core (Windows — no tier-5 HTTP oracles)"
    export SKIP_EXPLOITS=1
    export SKIP_TIER5_HTTP=1
    ;;
  *)
    log "nightly profile: core (unknown OS)"
    export SKIP_EXPLOITS=1
    export SKIP_TIER5_HTTP=1
    ;;
esac

export SKIP_BUILD="${SKIP_BUILD:-0}"
if [[ "$SKIP_BUILD" != "1" ]]; then
  log "build lic"
  (cd "$LIC_ROOT" && ./scripts/build.sh)
fi

export LIC="$LIC_ROOT/build/compiler/lic/lic"
export PATH="$LIC_ROOT/build/compiler/lic:$PATH"
cd "$LIC_ROOT"
mkdir -p benchmarks/results

RUNS="${BENCH_RUNS:-6}"
python3 benchmarks/harness/bench.py --tier 0 || true
if [[ -f "$ROOT/scripts/run-lic-tier-benches.py" ]]; then
  python3 "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" || true
else
  python3 benchmarks/harness/bench.py --tier 12 --runs "$RUNS" || true
fi
python3 benchmarks/harness/bench.py --tier 7 --runs "$RUNS" --skip-verify || true
python3 benchmarks/harness/bench_ecosystem.py --runs "$RUNS" --jobs "$BENCH_JOBS" || true

cd "$ROOT"
LIC_ROOT="$LIC_ROOT" LIS_ROOT="$LIS_ROOT" ./scripts/ingest/ingest-lic.sh || true
log "nightly core complete ($(uname -s))"
