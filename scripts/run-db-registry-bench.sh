#!/usr/bin/env bash
# Registry OLTP harness stub — publish/read P95 vs Postgres 15+ (same schema).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_registry"
PROFILE="${BENCH_DB_REGISTRY_PROFILE:-ci}"
MANIFEST_WRITER="$ROOT/scripts/ingest/write-tier-db-registry-manifest.py"

if [[ ! -f "$TIER_ROOT/suite.toml" ]]; then
  echo "run-db-registry-bench: missing $TIER_ROOT (tier_db_registry skeleton)" >&2
  exit 1
fi

# Future: run lidb vs postgres with schema/registry-v1.sql, emit results/latest.csv
if [[ "${BENCH_DB_REGISTRY_RUN_HARNESS:-0}" != "1" ]]; then
  echo "run-db-registry-bench: STUB (set BENCH_DB_REGISTRY_RUN_HARNESS=1 when harness lands)"
  echo "  profile=$PROFILE  schema=$TIER_ROOT/schema/registry-v1.sql"
  echo "  targets: P95 latency_ms vs postgres (threshold_ratio=${BENCH_DB_REGISTRY_THRESHOLD:-1.2})"
  echo "  nightly: optional — use BENCH_DB_REGISTRY_PROFILE=nightly for timed runs"
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

echo "run-db-registry-bench: harness not implemented yet (BENCH_DB_REGISTRY_RUN_HARNESS=1)" >&2
exit 2
