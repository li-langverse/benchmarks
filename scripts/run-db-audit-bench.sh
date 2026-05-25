#!/usr/bin/env bash
# lidb audit-log harness stub — query log completeness + tamper evidence.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_audit"
PROFILE="${BENCH_DB_AUDIT_PROFILE:-ci}"
MANIFEST_WRITER="$ROOT/scripts/ingest/write-tier-db-audit-manifest.py"

if [[ ! -f "$TIER_ROOT/suite.toml" ]]; then
  echo "run-db-audit-bench: missing $TIER_ROOT" >&2
  exit 1
fi

if [[ "${BENCH_DB_AUDIT_RUN_HARNESS:-0}" != "1" ]]; then
  echo "run-db-audit-bench: STUB (set BENCH_DB_AUDIT_RUN_HARNESS=1 when harness lands)"
  echo "  profile=$PROFILE  schema=$TIER_ROOT/schema/audit-log-v1.sql"
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

echo "run-db-audit-bench: harness not implemented yet" >&2
exit 2
