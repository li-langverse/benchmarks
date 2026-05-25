#!/usr/bin/env bash
# Registry graph harness stub — dep closure / cycle detect vs AGE / optional Kùzu.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_graph_registry"
PROFILE="${BENCH_DB_GRAPH_PROFILE:-ci}"
MANIFEST_WRITER="$ROOT/scripts/ingest/write-tier-db-graph-registry-manifest.py"

if [[ ! -f "$TIER_ROOT/suite.toml" ]]; then
  echo "run-db-graph-registry-bench: missing $TIER_ROOT" >&2
  exit 1
fi

if [[ "${BENCH_DB_GRAPH_RUN_HARNESS:-0}" != "1" ]]; then
  echo "run-db-graph-registry-bench: STUB (set BENCH_DB_GRAPH_RUN_HARNESS=1 when harness lands)"
  echo "  profile=$PROFILE  schema=$TIER_ROOT/schema/graph-registry-v1.sql"
  echo "  edges=${BENCH_DB_GRAPH_EDGES:-100000}  threshold=${BENCH_DB_GRAPH_THRESHOLD:-1.2}"
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

echo "run-db-graph-registry-bench: harness not implemented yet" >&2
exit 2
