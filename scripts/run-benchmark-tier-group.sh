#!/usr/bin/env bash
# Run one nightly tier group; writes results/tier-<group>.csv (parallel CI shards).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=lib/bench-python.sh
source "$ROOT/scripts/lib/bench-python.sh"
GROUP="${1:-${BENCH_TIER_GROUP:-}}"
if [[ -z "$GROUP" ]]; then
  echo "usage: run-benchmark-tier-group.sh <tier0|tier12|tier7|tier7-N|tier3|tier5|tier5-exploits>" >&2
  exit 2
fi

REPO_PARENT="$(cd "$ROOT/.." && pwd)"
if [[ -z "${LIC_ROOT:-}" ]]; then
  if [[ -d "$ROOT/lic" ]]; then
    LIC_ROOT="$ROOT/lic"
  elif [[ -d "$REPO_PARENT/lic" ]]; then
    LIC_ROOT="$REPO_PARENT/lic"
  else
    LIC_ROOT="$ROOT/lic"
  fi
fi
LIS_ROOT="${LIS_ROOT:-$REPO_PARENT/lis}"
# shellcheck source=lib/resolve-lic-bench.sh
source "$ROOT/scripts/lib/resolve-lic-bench.sh"
RUNS="${BENCH_RUNS:-6}"
export BENCH_JOBS="${BENCH_JOBS:-$(nproc 2>/dev/null || echo 4)}"
export BENCH_ADAPTIVE_RUNS="${BENCH_ADAPTIVE_RUNS:-1}"
export BENCH_EQUALIZE_RUNS="${BENCH_EQUALIZE_RUNS:-1}"
export BENCH_MIN_RUNS="${BENCH_MIN_RUNS:-6}"
export BENCH_SUBSEC_MIN_RUNS="${BENCH_SUBSEC_MIN_RUNS:-20}"
export BENCH_TARGET_SAMPLE_SEC="${BENCH_TARGET_SAMPLE_SEC:-1.0}"
export BENCH_MAX_RUNS="${BENCH_MAX_RUNS:-200}"
SKIP_BUILD="${SKIP_BUILD:-1}"
if [[ "${BENCH_NIGHTLY:-0}" == "1" ]]; then
  SKIP_TIER0="${SKIP_TIER0:-0}"
else
  SKIP_TIER0="${SKIP_TIER0:-1}"
fi
SKIP_EXPLOITS="${SKIP_EXPLOITS:-0}"

require_tier_csv() {
  if [[ ! -s "$BENCHMARKS_CSV" ]]; then
    echo "ERROR: $BENCHMARKS_CSV empty or missing after $GROUP" >&2
    exit 1
  fi
}

export BENCHMARKS_CSV="$ROOT/results/tier-${GROUP}.csv"
export LIS_ROOT
export_lic_bench_paths "$LIC_ROOT"
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
    "$ROOT/scripts/run-bench.sh" --tier 0 || {
      echo "WARN: tier0 had failures (li-tests/verify)" >&2
    }
    ;;

  tier1)
    log "tier 1 — micro (runs=$RUNS jobs=${BENCH_JOBS})"
    export BENCH_RUNS="$RUNS"
    bench_python "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --tier 1 || {
      echo "WARN: tier 1 had failures" >&2
    }
    ;;
  tier2-md)
    log "tier 2 — MD physics shard (runs=$RUNS jobs=${BENCH_JOBS})"
    export BENCH_RUNS="$RUNS"
    bench_python "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --tier 2 --tier2-group md || {
      echo "WARN: tier2-md had failures" >&2
    }
    ;;
  tier2-pde)
    log "tier 2 — PDE physics shard (runs=$RUNS jobs=${BENCH_JOBS})"
    export BENCH_RUNS="$RUNS"
    bench_python "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --tier 2 --tier2-group pde || {
      echo "WARN: tier2-pde had failures" >&2
    }
    ;;
  tier2-mech)
    log "tier 2 — mechanics physics shard (runs=$RUNS jobs=${BENCH_JOBS})"
    export BENCH_RUNS="$RUNS"
    bench_python "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --tier 2 --tier2-group mech || {
      echo "WARN: tier2-mech had failures" >&2
    }
    ;;
  tier12)
    log "tier 1+2 — micro + physics (runs=$RUNS jobs=${BENCH_JOBS})"
    export BENCH_RUNS="$RUNS"
    bench_python "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --tier all || {
      echo "WARN: tier 1+2 had failures" >&2
    }
    ;;


  tier7|tier7-*)
    REGISTRY_SHARD_COUNT="${REGISTRY_SHARD_COUNT:-1}"
    REGISTRY_SHARD_ARGS=()
    if [[ "$GROUP" =~ ^tier7-[0-9]+$ ]]; then
      shard="${GROUP#tier7-}"
      REGISTRY_SHARD_ARGS=(--registry-shard "$shard" --registry-shard-count "$REGISTRY_SHARD_COUNT")
      # One CI worker per shard; scale wall clock via REGISTRY_SHARD_COUNT, not in-job oversubscription.
      export BENCH_JOBS="${REGISTRY_BENCH_JOBS:-1}"
      log "tier 7 — algo_registry shard $shard/$REGISTRY_SHARD_COUNT (runs=$RUNS jobs=${BENCH_JOBS})"
    else
      log "tier 7 — algo_registry all aliases (runs=$RUNS jobs=${BENCH_JOBS})"
    fi
    export REGISTRY_RUN_TIMINGS="${REGISTRY_RUN_TIMINGS:-1}"
    export BENCH_RUNS="$RUNS"
    bench_python "$ROOT/scripts/run-registry-tier-benches.py" \
      --runs "$RUNS" --jobs "$BENCH_JOBS" "${REGISTRY_SHARD_ARGS[@]}"
    ;;
  tier3)
    log "tier 3 — ecosystem (compile, security, async; jobs=${BENCH_JOBS})"
    bench_python "$ROOT/harness/bench_ecosystem.py" \
      --runs "$RUNS" --jobs "$BENCH_JOBS" --latest "$BENCHMARKS_CSV"
    ;;
  tier5)
    if [[ "${SKIP_TIER5_HTTP:-0}" == "1" ]]; then
      echo "ERROR: tier5 required but SKIP_TIER5_HTTP=1" >&2
      exit 1
    fi
    if [[ ! -f "$ROOT/scripts/run-tier5-http-bench.sh" ]]; then
      echo "ERROR: missing $ROOT/scripts/run-tier5-http-bench.sh (sync vendor/lis-tier5)" >&2
      exit 1
    fi
    log "tier 5 — HTTP multi-oracle"
    export BENCH_HTTP_PROFILE="${BENCH_HTTP_PROFILE:-nightly}"
    export BENCH_HTTP_ORACLES="${BENCH_HTTP_ORACLES:-nginx,apache,lighttpd,node,bun,li}"
    "$ROOT/scripts/run-tier5-http-bench.sh"
    log "tier 5 — supplemental proxy_loopback"
    export HTTP_BENCH_RUNS="${HTTP_BENCH_RUNS:-6}"
    export BENCH_MIN_RUNS="${BENCH_MIN_RUNS}"
    export BENCH_SUBSEC_MIN_RUNS="${BENCH_SUBSEC_MIN_RUNS}"
    bench_python "$ROOT/scripts/tier5-http-bench.py" --lic-root "$LIC_ROOT" --runs "$HTTP_BENCH_RUNS" || {
      echo "WARN: supplemental tier5-http-bench failed (wrk/proxy); merging harness CSV only" >&2
    }
    log "tier 5 — merge HTTP CSV into tier shard"
    export BENCHMARKS_CSV
    bench_python "$ROOT/scripts/merge-tier5-http-into-csv.py" "$ROOT" "$LIC_ROOT"
    ;;
  tier5-exploits)
    if [[ "$SKIP_EXPLOITS" == "1" ]]; then
      echo "ERROR: tier5-exploits required but SKIP_EXPLOITS=1" >&2
      exit 1
    fi
    if [[ ! -f "$ROOT/scripts/run-tier5-http-exploits.sh" ]]; then
      echo "ERROR: missing $ROOT/scripts/run-tier5-http-exploits.sh" >&2
      exit 1
    fi
    log "tier 5 — HTTP exploits (TIER5_EXPLOIT_PROFILE=${TIER5_EXPLOIT_PROFILE:-pr})"
    export TIER5_EXPLOIT_PROFILE="${TIER5_EXPLOIT_PROFILE:-${BENCH_HTTP_PROFILE:-pr}}"
    export TIER5_EXPLOIT_LANGS="${TIER5_EXPLOIT_LANGS:-nginx,li}"
    exploit_src="$ROOT/vendor/lis-tier5/results/exploit_report.csv"
    "$ROOT/scripts/run-tier5-http-exploits.sh" || {
      if [[ "${BENCH_NIGHTLY:-0}" == "1" ]] && [[ -s "$exploit_src" ]]; then
        echo "WARN: tier5-exploits harness failures recorded in $exploit_src" >&2
      else
        exit 1
      fi
    }
    bench_python "$ROOT/scripts/exploit-report-to-tier-csv.py" "$exploit_src" "$BENCHMARKS_CSV"
    ;;
  *)
    echo "unknown tier group: $GROUP" >&2
    exit 2
    ;;
esac


_lic_csv="$LIC_ROOT/benchmarks/results/latest.csv"
if [[ "${BENCH_NIGHTLY:-0}" != "1" ]] && [[ ! -s "$BENCHMARKS_CSV" ]] && [[ -s "$_lic_csv" ]]; then
  cp "$_lic_csv" "$BENCHMARKS_CSV"
  log "copied harness CSV from $_lic_csv"
fi

require_tier_csv
log "done — $BENCHMARKS_CSV ($(wc -l < "$BENCHMARKS_CSV") lines)"
