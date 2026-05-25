#!/usr/bin/env bash
# lidb security audit harness stub — injection + RLS bypass probes.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_security"
PROFILE="${BENCH_DB_SECURITY_PROFILE:-ci}"
MANIFEST_WRITER="$ROOT/scripts/ingest/write-tier-db-security-manifest.py"

if [[ ! -f "$TIER_ROOT/suite.toml" ]]; then
  echo "run-db-security-bench: missing $TIER_ROOT" >&2
  exit 1
fi

if [[ "${BENCH_DB_SECURITY_RUN_HARNESS:-0}" != "1" ]]; then
  echo "run-db-security-bench: STUB (set BENCH_DB_SECURITY_RUN_HARNESS=1 when harness lands)"
  echo "  profile=$PROFILE  schema=$TIER_ROOT/schema/security-audit-v1.sql"
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

echo "run-db-security-bench: harness not implemented yet" >&2
exit 2
