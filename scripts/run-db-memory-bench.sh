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
  echo "run-db-memory-bench: STUB (set BENCH_DB_MEMORY_RUN_HARNESS=1 when harness lands)"
  echo "  profile=$PROFILE  schema=$TIER_ROOT/schema/memory-baseline-v1.sql"
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

echo "run-db-memory-bench: harness not implemented yet" >&2
exit 2
