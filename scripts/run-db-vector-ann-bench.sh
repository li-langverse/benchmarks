#!/usr/bin/env bash
# Vector ANN harness stub — recall@k / QPS vs Faiss CPU vs optional lidb-gpu.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIER_ROOT="$ROOT/benchmarks/tier_db_vector_ann"
PROFILE="${BENCH_DB_VECTOR_PROFILE:-ci}"
MANIFEST_WRITER="$ROOT/scripts/ingest/write-tier-db-vector-ann-manifest.py"

if [[ ! -f "$TIER_ROOT/suite.toml" ]]; then
  echo "run-db-vector-ann-bench: missing $TIER_ROOT" >&2
  exit 1
fi

if [[ "${BENCH_DB_VECTOR_RUN_HARNESS:-0}" != "1" ]]; then
  echo "run-db-vector-ann-bench: STUB (set BENCH_DB_VECTOR_RUN_HARNESS=1 when harness lands)"
  echo "  profile=$PROFILE  dim=${BENCH_DB_VECTOR_DIM:-128}"
  python3 "$MANIFEST_WRITER" --profile "$PROFILE" --stub
  exit 0
fi

echo "run-db-vector-ann-bench: harness not implemented yet" >&2
exit 2
