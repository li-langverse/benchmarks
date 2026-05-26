#!/usr/bin/env bash
# Fallback tier_db_registry harness — SQLite stub or delegate to registry_oltp.py.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_registry"
PROFILE="${BENCH_PROFILE:-ci}"
HARNESS_REAL="$TIER_ROOT/harness/registry_oltp.py"
HARNESS_STUB="$TIER_ROOT/harness/registry_oltp_stub.py"
JSON_OUT="${BENCH_HARNESS_JSON:-$ROOT/data/latest/tier-db-registry-harness.json}"
MANIFEST_WRITER="$ROOT/scripts/ingest/write-tier-db-registry-manifest.py"

if [[ -f "$HARNESS_REAL" && "${BENCH_DB_REGISTRY_FORCE_SQLITE_STUB:-0}" != "1" ]]; then
  ENGINE="${BENCH_DB_REGISTRY_ENGINE:-auto}"
  set +e
  python3 "$HARNESS_REAL" --profile "$PROFILE" --engine "$ENGINE" --json-out "$JSON_OUT"
  RC=$?
  set -e
  if [[ $RC -eq 0 ]]; then
    STATUS="$(python3 -c "import json; print(json.load(open('$JSON_OUT'))['status'])")"
    exec python3 "$MANIFEST_WRITER" --profile "$PROFILE" --from-harness "$JSON_OUT" --status "$STATUS"
  fi
  if [[ $RC -ne 2 ]]; then
    exit "$RC"
  fi
  echo "lidb-bench-stub: real engines unavailable — SQLite stub" >&2
fi

echo "lidb-bench-stub: registry_oltp (SQLite stub timing)"

RUN_TIMING=0
if [[ "$PROFILE" == "nightly" || "${BENCH_DB_REGISTRY_RUN_HARNESS:-0}" == "1" ]]; then
  RUN_TIMING=1
fi

ARGS=(--profile "$PROFILE")
if [[ "$RUN_TIMING" == "1" ]]; then
  ARGS+=(--run-timing --json-out "$JSON_OUT")
else
  ARGS+=(--validate-only)
fi

python3 "$HARNESS_STUB" "${ARGS[@]}"

MANIFEST_ARGS=(--profile "$PROFILE")
if [[ "$RUN_TIMING" == "1" ]]; then
  MANIFEST_ARGS+=(--from-harness "$JSON_OUT" --status unknown)
else
  MANIFEST_ARGS+=(--stub)
fi

exec python3 "$MANIFEST_WRITER" "${MANIFEST_ARGS[@]}"
