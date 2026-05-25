#!/usr/bin/env bash
# Fallback tier_db_parallel harness when ../lidb/scripts/bench/parallel_load.sh is absent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PROFILE="${BENCH_PROFILE:-ci}"
echo "lidb-bench-stub: parallel_load (lidb harness missing; writing stub manifest)"
exec python3 "$ROOT/scripts/ingest/write-tier-db-parallel-manifest.py" --profile "$PROFILE" --stub
