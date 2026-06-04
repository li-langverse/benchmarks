#!/usr/bin/env bash
# Run the full Li org benchmark suite and refresh dashboard summary (agents: run after every implementation).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=lib/bench-python.sh
source "$ROOT/scripts/lib/bench-python.sh"
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
PROFILE="${BENCH_PROFILE:-full}"
RUNS="${BENCH_RUNS:-6}"
export BENCH_JOBS="${BENCH_JOBS:-$(nproc 2>/dev/null || echo 4)}"
export BENCH_ADAPTIVE_RUNS="${BENCH_ADAPTIVE_RUNS:-1}"
export BENCH_MIN_RUNS="${BENCH_MIN_RUNS:-6}"
export BENCH_SUBSEC_MIN_RUNS="${BENCH_SUBSEC_MIN_RUNS:-20}"
export BENCH_TARGET_SAMPLE_SEC="${BENCH_TARGET_SAMPLE_SEC:-1.0}"
export BENCH_MAX_RUNS="${BENCH_MAX_RUNS:-200}"
SKIP_BUILD="${SKIP_BUILD:-0}"
SKIP_TIER0="${SKIP_TIER0:-0}"
SKIP_EXPLOITS="${SKIP_EXPLOITS:-0}"

log() { echo "==> $*"; }

if [[ ! -d "$LIC_ROOT" ]]; then
  echo "LIC_ROOT=$LIC_ROOT missing — clone li-langverse/lic next to benchmarks" >&2
  exit 1
fi

export BENCHMARKS_CSV="${BENCHMARKS_CSV:-$ROOT/results/latest.csv}"
export LIS_ROOT

if [[ "$SKIP_BUILD" != "1" ]]; then
  log "setup lic + li-httpd"
  "$ROOT/scripts/setup-lic-for-bench.sh"
fi

export_lic_bench_paths "$LIC_ROOT"
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

if [[ "$SKIP_TIER0" != "1" ]]; then
  log "tier 0 — li-tests + verify + stability"
  if ! "$ROOT/scripts/run-bench.sh" --tier 0; then
    echo "WARN: tier0 failed (li-tests/verify) — continuing perf tiers" >&2
  fi
fi

log "tier 1+2 — micro + physics (runs=$RUNS jobs=${BENCH_JOBS})"
export BENCH_RUNS="$RUNS"
python3 "$ROOT/scripts/run-lic-tier-benches.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --tier all || {
  echo "WARN: tier 1+2 had failures — continuing" >&2
}

log "tier 7 — algo_registry family-template aliases"
export REGISTRY_RUN_TIMINGS="${REGISTRY_RUN_TIMINGS:-1}"
"$ROOT/scripts/run-bench.sh" --tier 7 --runs "$RUNS" --skip-verify

log "tier 3 — ecosystem (compile, security, async; jobs=${BENCH_JOBS})"
bench_python "$ROOT/harness/bench_ecosystem.py" --runs "$RUNS" --jobs "$BENCH_JOBS" --latest "$BENCHMARKS_CSV"

if [[ "${SKIP_TIER5_HTTP:-0}" == "1" ]]; then
  log "tier 5 — HTTP multi-oracle skipped (SKIP_TIER5_HTTP=1)"
else
log "tier 5 — HTTP multi-oracle (nginx, apache, lighttpd, node, bun, li)"
export BENCH_HTTP_PROFILE="${BENCH_HTTP_PROFILE:-nightly}"
export BENCH_HTTP_ORACLES="${BENCH_HTTP_ORACLES:-nginx,apache,lighttpd,node,bun,li}"
if [[ -f "$ROOT/scripts/run-tier5-http-bench.sh" ]]; then
  "$ROOT/scripts/run-tier5-http-bench.sh" || echo "WARN: multi-oracle tier5 failed" >&2
else
  echo "WARN: missing run-tier5-http-bench.sh (sync vendor/lis-tier5)" >&2
fi

log "tier 5 — supplemental proxy_loopback (li_epoll + li c_epoll vs nginx)"
export HTTP_BENCH_RUNS="${HTTP_BENCH_RUNS:-6}"
export BENCH_MIN_RUNS="${BENCH_MIN_RUNS}"
export BENCH_SUBSEC_MIN_RUNS="${BENCH_SUBSEC_MIN_RUNS}"
python3 "$ROOT/scripts/tier5-http-bench.py" --lic-root "$LIC_ROOT" --runs "$HTTP_BENCH_RUNS" || {
  echo "WARN: tier5 supplemental http failed" >&2
}
fi

if [[ "$SKIP_EXPLOITS" != "1" ]] && [[ -f "$ROOT/scripts/run-tier5-http-exploits.sh" ]]; then
  log "tier 5 — HTTP exploits (TIER5_EXPLOIT_PROFILE=${TIER5_EXPLOIT_PROFILE:-pr})"
  export TIER5_EXPLOIT_PROFILE="${TIER5_EXPLOIT_PROFILE:-pr}"
  export TIER5_EXPLOIT_LANGS="${TIER5_EXPLOIT_LANGS:-nginx,apache,li}"
  "$ROOT/scripts/run-tier5-http-exploits.sh"
  exploit_tmp="$ROOT/results/tier-tier5-exploits.csv"
  bench_python "$ROOT/scripts/exploit-report-to-tier-csv.py" \
    "$ROOT/vendor/lis-tier5/results/exploit_report.csv" "$exploit_tmp"
  if [[ -s "$exploit_tmp" ]]; then
    python3 "$ROOT/scripts/ingest/merge_bench_csv_artifacts.py" "$BENCHMARKS_CSV" "$exploit_tmp"
  fi
else
  log "tier 5 — HTTP exploits skipped (SKIP_EXPLOITS=1)"
fi

# Merge tier-5 CSV rows into latest.csv for ingest
export BENCHMARKS_CSV
bench_python "$ROOT/scripts/merge-tier5-http-into-csv.py" "$ROOT" "$LIC_ROOT"
test -s "$BENCHMARKS_CSV"

cd "$ROOT"
log "ingest + summary.json"
LIC_ROOT="$LIC_ROOT" LIS_ROOT="$LIS_ROOT" ./scripts/ingest/ingest-lic.sh || true

log "benchmark status report"
./scripts/benchmark-failures-report.sh || true

log "full benchmark matrix (perf + HTTP oracles + exploits)"
python3 "$ROOT/scripts/benchmark-matrix-report.py" --json-only || true
echo "matrix: $ROOT/data/latest/benchmark-matrix.md"

log "done — see data/latest/summary.json and data/latest/benchmark-matrix.md"
