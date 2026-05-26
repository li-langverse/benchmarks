#!/usr/bin/env bash
# Registry OLTP harness — validate tier config (CI); optional real lidb vs Postgres bench.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_registry"
PROFILE="${BENCH_DB_REGISTRY_PROFILE:-ci}"
MANIFEST_WRITER="$ROOT/scripts/ingest/write-tier-db-registry-manifest.py"
HARNESS_PY="$TIER_ROOT/harness/registry_oltp.py"
HARNESS_STUB="$TIER_ROOT/harness/registry_oltp_stub.py"
JSON_OUT="${BENCH_HARNESS_JSON:-$ROOT/data/latest/tier-db-registry-harness.json}"

if [[ ! -f "$TIER_ROOT/suite.toml" ]]; then
  echo "run-db-registry-bench: missing $TIER_ROOT (tier_db_registry skeleton)" >&2
  exit 1
fi

# CI / default: config validation + stub manifest (no lidb/postgres required).
if [[ "${BENCH_DB_REGISTRY_RUN_HARNESS:-0}" != "1" ]]; then
  echo "run-db-registry-bench: validate tier_db_registry (profile=$PROFILE)"
  python3 "$HARNESS_PY" --validate-only --profile "$PROFILE"
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  echo "  schema=$TIER_ROOT/schema/registry-v1.sql"
  echo "  Real P95: BENCH_DB_REGISTRY_RUN_HARNESS=1 POSTGRES_URL=... LIDB_ROOT=../lidb"
  exit 0
fi

LIDB_ROOT="${LIDB_ROOT:-}"
if [[ -z "$LIDB_ROOT" ]]; then
  if cd "$ROOT/../lidb" 2>/dev/null; then
    LIDB_ROOT="$(pwd)"
  fi
fi
export LIDB_ROOT

ENGINE="${BENCH_DB_REGISTRY_ENGINE:-auto}"
echo "run-db-registry-bench: harness (profile=$PROFILE engine=$ENGINE)"

# Prefer real harness in benchmarks; lidb wrapper delegates here when present.
if [[ -f "$HARNESS_PY" ]]; then
  set +e
  python3 "$HARNESS_PY" \
    --profile "$PROFILE" \
    --engine "$ENGINE" \
    --json-out "$JSON_OUT"
  HARNESS_RC=$?
  set -e

  if [[ $HARNESS_RC -eq 2 ]]; then
    echo "run-db-registry-bench: no engines — falling back to SQLite stub" >&2
    export BENCH_DB_REGISTRY_ALLOW_SQLITE_STUB=1
    python3 "$HARNESS_STUB" --profile "$PROFILE" --run-timing --json-out "$JSON_OUT"
    python3 "$MANIFEST_WRITER" --profile "$PROFILE" --from-harness "$JSON_OUT" --status unknown
    exit 0
  fi

  if [[ $HARNESS_RC -ne 0 ]]; then
    echo "run-db-registry-bench: harness failed (rc=$HARNESS_RC)" >&2
    python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
    exit "$HARNESS_RC"
  fi

  MANIFEST_ARGS=(--profile "$PROFILE" --from-harness "$JSON_OUT")
  if [[ -f "$JSON_OUT" ]]; then
    HARNESS_STATUS="$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['status'])" "$JSON_OUT")"
    MANIFEST_ARGS+=(--status "$HARNESS_STATUS")
  fi
  python3 "$MANIFEST_WRITER" "${MANIFEST_ARGS[@]}"
  exit 0
fi

# Legacy: lidb shell wrapper or benchmarks SQLite stub script
HARNESS=""
if [[ -n "$LIDB_ROOT" && -f "$LIDB_ROOT/scripts/bench/registry_oltp.sh" ]]; then
  HARNESS="$LIDB_ROOT/scripts/bench/registry_oltp.sh"
elif [[ -f "$ROOT/scripts/lidb-bench-stub/registry_oltp.sh" ]]; then
  HARNESS="$ROOT/scripts/lidb-bench-stub/registry_oltp.sh"
fi

if [[ -z "$HARNESS" ]]; then
  echo "run-db-registry-bench: no harness script" >&2
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

export BENCH_PROFILE="$PROFILE"
export BENCH_HARNESS_JSON="$JSON_OUT"
bash "$HARNESS"
