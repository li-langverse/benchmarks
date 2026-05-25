#!/usr/bin/env bash
# Fallback tier_db_memory harness when ../lidb/scripts/bench/memory_footprint.sh is absent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PROFILE="${BENCH_PROFILE:-ci}"
echo "lidb-bench-stub: memory_footprint (lidb harness missing; writing stub manifest)"
exec python3 "$ROOT/scripts/ingest/write-tier-db-memory-manifest.py" --profile "$PROFILE" --stub
