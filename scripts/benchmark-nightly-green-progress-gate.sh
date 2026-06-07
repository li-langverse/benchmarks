#!/usr/bin/env bash
# Fast local gate: lic link smoke + harness unit tests (no full nightly dispatch).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"
REPO_PARENT="$(cd "$ROOT/.." && pwd)"
if [[ ! -d "$LIC_ROOT/.git" && -d "$REPO_PARENT/lic" ]]; then
  LIC_ROOT="$REPO_PARENT/lic"
fi

log() { echo "benchmark-nightly-green-progress: $*"; }
fail() { echo "benchmark-nightly-green-progress: FAIL $*" >&2; exit 1; }

[[ -d "$LIC_ROOT" ]] || fail "missing LIC_ROOT at $LIC_ROOT"

export LIC_ROOT LI_REPO_ROOT="$LIC_ROOT"
export BENCH_EQUALIZE_RUNS="${BENCH_EQUALIZE_RUNS:-1}"
export BENCH_MIN_RUNS="${BENCH_MIN_RUNS:-6}"
export BENCH_RUNS="${BENCH_RUNS:-6}"

log "lic link smoke (tier3 + registry alias)"
LIC_BIN="$LIC_ROOT/build/compiler/lic/lic"
[[ -x "$LIC_BIN" ]] || fail "missing lic binary at $LIC_BIN (run lic/scripts/build.sh)"
mkdir -p "$LIC_ROOT/build/bench"

smoke_build_li() {
  local src="$1"
  local out="$2"
  local bench_root extra_c
  bench_root="$(cd "$(dirname "$src")/.." && pwd)"
  extra_c=""
  if [[ -d "$bench_root/common" ]]; then
    extra_c="$(find "$bench_root/common" -maxdepth 1 -name '*.c' -print -quit)"
  fi
  if [[ -n "$extra_c" ]]; then
    LI_EXTRA_C="$extra_c" "$LIC_BIN" build "$src" -o "$out" --release --allow-open-vc --no-lean-verify
  else
    "$LIC_BIN" build "$src" -o "$out" --release --allow-open-vc --no-lean-verify
  fi
}

WORKLOADS="$ROOT/benchmarks/workloads"
tier3_li="$WORKLOADS/tier3_ecosystem/async_await_chain/li/main.li"
registry_li="$WORKLOADS/tier2_physics/heat_equation_2d/li/main.li"
for src in "$tier3_li" "$registry_li"; do
  [[ -f "$src" ]] || fail "missing harness source $src"
  out="$LIC_ROOT/build/bench/_gate_smoke_$(basename "$(dirname "$(dirname "$src")")").out"
  smoke_build_li "$src" "$out"
  [[ -x "$out" ]] || fail "lic build did not produce executable for $src"
done

log "harness timing + registry shard tests"
python3 -m unittest \
  harness.test_timing_equalize \
  harness.test_csv_bench_io \
  tests.test_bench_registry_shard \
  -v

if [[ -f "$ROOT/results/latest.csv" && -f "$ROOT/data/latest/summary.json" ]]; then
  log "optional measurement-quality on committed summary + CSV"
  export MEASUREMENT_STRICT_PARITY="${MEASUREMENT_STRICT_PARITY:-1}"
  export BENCHMARKS_CSV="$ROOT/results/latest.csv"
  python3 "$ROOT/scripts/check-summary-measurement-quality.py" || {
    fail "check-summary-measurement-quality failed (fix BN2 before completion)"
  }
else
  log "skip measurement-quality (no results/latest.csv or summary.json yet)"
fi

log "PASS progress gate"
