#!/usr/bin/env bash
# lidb parallel audit harness stub — concurrent readers/writers.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_parallel"
PROFILE="${BENCH_DB_PARALLEL_PROFILE:-ci}"
MANIFEST_WRITER="$ROOT/scripts/ingest/write-tier-db-parallel-manifest.py"

if [[ ! -f "$TIER_ROOT/suite.toml" ]]; then
  echo "run-db-parallel-bench: missing $TIER_ROOT" >&2
  exit 1
fi

if [[ "${BENCH_DB_PARALLEL_RUN_HARNESS:-0}" != "1" ]]; then
  echo "run-db-parallel-bench: STUB (set BENCH_DB_PARALLEL_RUN_HARNESS=1 to run lidb harness)"
  echo "  profile=$PROFILE  schema=$TIER_ROOT/schema/parallel-load-v1.sql"
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

LIDB_ROOT="${LIDB_ROOT:-}"
if [[ -z "$LIDB_ROOT" ]]; then
  if cd "$ROOT/../lidb" 2>/dev/null; then
    LIDB_ROOT="$(pwd)"
  fi
fi

HARNESS=""
if [[ -n "$LIDB_ROOT" && -f "$LIDB_ROOT/scripts/bench/parallel_load.sh" ]]; then
  HARNESS="$LIDB_ROOT/scripts/bench/parallel_load.sh"
elif [[ -f "$ROOT/scripts/lidb-bench-stub/parallel_load.sh" ]]; then
  HARNESS="$ROOT/scripts/lidb-bench-stub/parallel_load.sh"
fi

if [[ -z "$HARNESS" ]]; then
  echo "run-db-parallel-bench: no harness (lidb or benchmarks stub)" >&2
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

export BENCH_PROFILE="$PROFILE"
export BENCH_HARNESS_JSON="$ROOT/data/latest/tier-db-parallel.json"
bash "$HARNESS"
