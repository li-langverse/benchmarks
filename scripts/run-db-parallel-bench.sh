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
  echo "run-db-parallel-bench: STUB (set BENCH_DB_PARALLEL_RUN_HARNESS=1 when harness lands)"
  echo "  profile=$PROFILE  schema=$TIER_ROOT/schema/parallel-load-v1.sql"
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

echo "run-db-parallel-bench: harness not implemented yet" >&2
exit 2
