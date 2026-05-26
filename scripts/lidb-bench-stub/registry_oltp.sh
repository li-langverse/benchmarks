#!/usr/bin/env bash
# Fallback tier_db_registry harness when ../lidb/scripts/bench/registry_oltp.sh is absent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_registry"
PROFILE="${BENCH_PROFILE:-ci}"
HARNESS_PY="$TIER_ROOT/harness/registry_oltp_stub.py"
JSON_OUT="${BENCH_HARNESS_JSON:-$ROOT/data/latest/tier-db-registry-harness.json}"

echo "lidb-bench-stub: registry_oltp (lidb harness missing; SQLite stub timing)"

RUN_TIMING=0
if [[ "$PROFILE" == "nightly" ]]; then
  RUN_TIMING=1
fi

ARGS=(--profile "$PROFILE")
if [[ "$RUN_TIMING" == "1" ]]; then
  ARGS+=(--run-timing --json-out "$JSON_OUT")
else
  ARGS+=(--validate-only)
fi

python3 "$HARNESS_PY" "${ARGS[@]}"

MANIFEST_ARGS=(--profile "$PROFILE")
if [[ "$RUN_TIMING" == "1" ]]; then
  MANIFEST_ARGS+=(--from-harness "$JSON_OUT" --status unknown)
else
  MANIFEST_ARGS+=(--stub)
fi

exec python3 "$ROOT/scripts/ingest/write-tier-db-registry-manifest.py" "${MANIFEST_ARGS[@]}"
