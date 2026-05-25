#!/usr/bin/env bash
# lidb memory audit harness stub — RSS idle and peak under load.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_memory"
PROFILE="${BENCH_DB_MEMORY_PROFILE:-ci}"
MANIFEST_WRITER="$ROOT/scripts/ingest/write-tier-db-memory-manifest.py"

if [[ ! -f "$TIER_ROOT/suite.toml" ]]; then
  echo "run-db-memory-bench: missing $TIER_ROOT" >&2
  exit 1
fi

if [[ "${BENCH_DB_MEMORY_RUN_HARNESS:-0}" != "1" ]]; then
  echo "run-db-memory-bench: STUB (set BENCH_DB_MEMORY_RUN_HARNESS=1 to run lidb harness)"
  echo "  profile=$PROFILE  schema=$TIER_ROOT/schema/memory-baseline-v1.sql"
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
if [[ -n "$LIDB_ROOT" && -f "$LIDB_ROOT/scripts/bench/memory_footprint.sh" ]]; then
  HARNESS="$LIDB_ROOT/scripts/bench/memory_footprint.sh"
elif [[ -f "$ROOT/scripts/lidb-bench-stub/memory_footprint.sh" ]]; then
  HARNESS="$ROOT/scripts/lidb-bench-stub/memory_footprint.sh"
fi

if [[ -z "$HARNESS" ]]; then
  echo "run-db-memory-bench: no harness (lidb or benchmarks stub)" >&2
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

export BENCH_PROFILE="$PROFILE"
export BENCH_HARNESS_JSON="$ROOT/data/latest/tier-db-memory.json"
bash "$HARNESS"
