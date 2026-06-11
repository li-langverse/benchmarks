#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
export BENCHMARKS_CSV="${BENCHMARKS_CSV:-$ROOT/results/latest.csv}"
chmod +x "$ROOT/scripts/ingest/ingest-csv-smoke.sh" "$ROOT/scripts/ingest/build-summary-li.sh"
"$ROOT/scripts/ingest/ingest-csv-smoke.sh"
if ! "$ROOT/scripts/ingest/build-summary-li.sh"; then
  python3 "$ROOT/scripts/ingest/build_summary.py" "$LIC_ROOT" "$LIS_ROOT"
fi
python3 "$ROOT/scripts/patch-summary-oracle-csv.py" || true
python3 "$ROOT/scripts/ingest/validate-gpu-contribution.py" || true
python3 "$ROOT/scripts/ingest/build-lig-gpu-matrix.py" "${LIC_ROOT:-}" || true
python3 "$ROOT/scripts/record-benchmark-history.py" || true
"$ROOT/scripts/regression-check.sh" || true
python3 "$ROOT/scripts/benchmark-matrix-report.py" --json-only 2>/dev/null || true
