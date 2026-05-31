#!/usr/bin/env bash
# Run one nightly tier group; writes results/tier-<group>.csv (parallel CI shards).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GROUP="${1:-${BENCH_TIER_GROUP:-}}"
if [[ -z "$GROUP" ]]; then
  echo "usage: run-benchmark-tier-group.sh <tier0|tier12|tier7|tier3|tier5|tier5-exploits>" >&2
  exit 2
fi

LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
RUNS="${BENCH_RUNS:-6}"
export BENCH_JOBS="${BENCH_JOBS:-$(nproc 2>/dev/null || echo 4)}"
export BENCH_ADAPTIVE_RUNS="${BENCH_ADAPTIVE_RUNS:-1}"
export BENCH_MIN_RUNS="${BENCH_MIN_RUNS:-6}"
export BENCH_SUBSEC_MIN_RUNS="${BENCH_SUBSEC_MIN_RUNS:-20}"
export BENCH_TARGET_SAMPLE_SEC="${BENCH_TARGET_SAMPLE_SEC:-1.0}"
export BENCH_MAX_RUNS="${BENCH_MAX_RUNS:-200}"
SKIP_BUILD="${SKIP_BUILD:-1}"
SKIP_TIER0="${SKIP_TIER0:-1}"
SKIP_EXPLOITS="${SKIP_EXPLOITS:-0}"

export BENCHMARKS_CSV="${BENCHMARKS_CSV:-$ROOT/results/tier-${GROUP}.csv}"
export LIC_ROOT LIS_ROOT LI_REPO_ROOT="$LIC_ROOT"
export PATH="$LIC_ROOT/build/compiler/lic:$PATH"
export LIC="$LIC_ROOT/build/compiler/lic/lic"
export LI_HTTPD_BIN="$LIC_ROOT/build/li-httpd"
export BENCH_NIGHTLY="${BENCH_NIGHTLY:-1}"

log() { echo "==> [$GROUP] $*"; }

if [[ ! -x "$LIC" ]]; then
  echo "missing lic binary at $LIC (run setup-lic-for-bench or restore lic-build artifact)" >&2
  exit 1
fi

if command -v clang-22 >/dev/null 2>&1; then
  export CC="${CC:-clang-22}"
  export CXX="${CXX:-clang++-22}"
elif command -v clang-18 >/dev/null 2>&1; then
  export CC="${CC:-clang-18}"
  export CXX="${CXX:-clang++-18}"
else
  export CC="${CC:-clang}"
  export CXX="${CXX:-clang++}"
fi

mkdir -p "$(dirname "$BENCHMARKS_CSV")"

case "$GROUP" in
  tier0)
    log "tier 0 — li-tests + verify + stability"
    if ! "$ROOT/scripts/run-bench.sh" --tier 0; then
      echo "WARN: tier0 failed — continuing" >&2
    fi
    ;;

  tier1)
    log "tier 1 — micro (runs=$RUNS jobs=${BENCH_JOBS})"
    export BENCH_RUNS="$RUNS"
    python3 "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --tier 1 || {
      echo "WARN: tier 1 had failures" >&2
    }
    ;;
  tier2-md)
    log "tier 2 — MD physics shard (runs=$RUNS jobs=${BENCH_JOBS})"
    export BENCH_RUNS="$RUNS"
    python3 "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --tier 2 --tier2-group md || {
      echo "WARN: tier2-md had failures" >&2
    }
    ;;
  tier2-pde)
    log "tier 2 — PDE physics shard (runs=$RUNS jobs=${BENCH_JOBS})"
    export BENCH_RUNS="$RUNS"
    python3 "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --tier 2 --tier2-group pde || {
      echo "WARN: tier2-pde had failures" >&2
    }
    ;;
  tier2-mech)
    log "tier 2 — mechanics physics shard (runs=$RUNS jobs=${BENCH_JOBS})"
    export BENCH_RUNS="$RUNS"
    python3 "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --tier 2 --tier2-group mech || {
      echo "WARN: tier2-mech had failures" >&2
    }
    ;;
  tier12)
    log "tier 1+2 — micro + physics (runs=$RUNS jobs=${BENCH_JOBS})"
    export BENCH_RUNS="$RUNS"
    python3 "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --tier all || {
      echo "WARN: tier 1+2 had failures" >&2
    }
    ;;


  tier7)
    log "tier 7 — algo_registry family-template aliases"
    "$ROOT/scripts/run-bench.sh" --tier 7 --runs "$RUNS" --skip-verify || {
      echo "WARN: tier7 registry aliases failed" >&2
    }
    ;;
  tier3)
    log "tier 3 — ecosystem (compile, security, async; jobs=${BENCH_JOBS})"
    python3 "$ROOT/harness/bench_ecosystem.py" --runs "$RUNS" --jobs "$BENCH_JOBS"
    ;;
  tier5)
    if [[ "${SKIP_TIER5_HTTP:-0}" == "1" ]]; then
      log "tier 5 skipped (SKIP_TIER5_HTTP=1)"
      exit 0
    fi
    log "tier 5 — HTTP multi-oracle"
    export BENCH_HTTP_PROFILE="${BENCH_HTTP_PROFILE:-nightly}"
    export BENCH_HTTP_ORACLES="${BENCH_HTTP_ORACLES:-nginx,apache,lighttpd,node,bun,li}"
    if [[ -f "$ROOT/scripts/run-tier5-http-bench.sh" ]]; then
      "$ROOT/scripts/run-tier5-http-bench.sh" || echo "WARN: multi-oracle tier5 failed" >&2
    else
      echo "WARN: missing run-tier5-http-bench.sh" >&2
    fi
    log "tier 5 — supplemental proxy_loopback"
    export HTTP_BENCH_RUNS="${HTTP_BENCH_RUNS:-6}"
    export BENCH_MIN_RUNS="${BENCH_MIN_RUNS}"
    export BENCH_SUBSEC_MIN_RUNS="${BENCH_SUBSEC_MIN_RUNS}"
    python3 "$ROOT/scripts/tier5-http-bench.py" --lic-root "$LIC_ROOT" --runs "$HTTP_BENCH_RUNS" || {
      echo "WARN: tier5 supplemental http failed" >&2
    }
    ;;
  tier5-exploits)
    if [[ "$SKIP_EXPLOITS" == "1" ]] || [[ ! -f "$ROOT/scripts/run-tier5-http-exploits.sh" ]]; then
      log "tier 5 exploits skipped"
      exit 0
    fi
    log "tier 5 — HTTP exploits (TIER5_EXPLOIT_PROFILE=${TIER5_EXPLOIT_PROFILE:-pr})"
    export TIER5_EXPLOIT_PROFILE="${TIER5_EXPLOIT_PROFILE:-pr}"
    export TIER5_EXPLOIT_LANGS="${TIER5_EXPLOIT_LANGS:-nginx,apache,li}"
    if ! "$ROOT/scripts/run-tier5-http-exploits.sh"; then
      echo "WARN: tier5 HTTP exploits had failures" >&2
    fi
    ;;
  *)
    echo "unknown tier group: $GROUP" >&2
    exit 2
    ;;
esac


_lic_csv="$LIC_ROOT/benchmarks/results/latest.csv"
if [[ ! -s "$BENCHMARKS_CSV" ]] && [[ -s "$_lic_csv" ]]; then
  cp "$_lic_csv" "$BENCHMARKS_CSV"
  log "copied harness CSV from $_lic_csv"
fi

if [[ ! -s "$BENCHMARKS_CSV" ]]; then
  echo "WARN: $BENCHMARKS_CSV empty or missing after $GROUP" >&2
fi
log "done — $BENCHMARKS_CSV"
