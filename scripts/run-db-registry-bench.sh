#!/usr/bin/env bash
# Registry OLTP harness — validate tier config (CI); optional SQLite stub or lidb vs Postgres.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_registry"
PROFILE="${BENCH_DB_REGISTRY_PROFILE:-ci}"
MANIFEST_WRITER="$ROOT/scripts/ingest/write-tier-db-registry-manifest.py"
HARNESS_PY="$TIER_ROOT/harness/registry_oltp_stub.py"

if [[ ! -f "$TIER_ROOT/suite.toml" ]]; then
  echo "run-db-registry-bench: missing $TIER_ROOT (tier_db_registry skeleton)" >&2
  exit 1
fi

# CI / default: config validation + stub manifest (no lidb/postgres required).
if [[ "${BENCH_DB_REGISTRY_RUN_HARNESS:-0}" != "1" ]]; then
  echo "run-db-registry-bench: validate tier_db_registry (profile=$PROFILE)"
  python3 "$HARNESS_PY" --profile "$PROFILE" --validate-only
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  echo "  schema=$TIER_ROOT/schema/registry-v1.sql"
  echo "  P95 parity: set BENCH_DB_REGISTRY_RUN_HARNESS=1 when lidb + Postgres harness lands"
  exit 0
fi

LIDB_ROOT="${LIDB_ROOT:-}"
if [[ -z "$LIDB_ROOT" ]]; then
  if cd "$ROOT/../lidb" 2>/dev/null; then
    LIDB_ROOT="$(pwd)"
  fi
fi

HARNESS=""
if [[ -n "$LIDB_ROOT" && -f "$LIDB_ROOT/scripts/bench/registry_oltp.sh" ]]; then
  HARNESS="$LIDB_ROOT/scripts/bench/registry_oltp.sh"
elif [[ -f "$ROOT/scripts/lidb-bench-stub/registry_oltp.sh" ]]; then
  HARNESS="$ROOT/scripts/lidb-bench-stub/registry_oltp.sh"
fi

if [[ -z "$HARNESS" ]]; then
  echo "run-db-registry-bench: no harness (lidb or benchmarks stub)" >&2
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

export BENCH_PROFILE="$PROFILE"
export BENCH_HARNESS_JSON="$ROOT/data/latest/tier-db-registry-harness.json"
bash "$HARNESS"
