#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
VENDOR_ROOT="${LIS_VENDOR_ROOT:-$ROOT/vendor/lis-tier5}"

# Prefer real lis checkout; fall back to vendored harness (until lis main has tier5 CSV).
LIS_CSV=""
if [[ -f "$LIS_ROOT/results/latest.csv" ]]; then
  LIS_CSV="$LIS_ROOT/results/latest.csv"
elif [[ -f "$VENDOR_ROOT/results/latest.csv" ]]; then
  LIS_ROOT="$VENDOR_ROOT"
  LIS_CSV="$VENDOR_ROOT/results/latest.csv"
fi

LIC_CSV="$LIC_ROOT/benchmarks/results/latest.csv"

chmod +x "$ROOT/scripts/ingest/ingest-csv-smoke.sh" "$ROOT/scripts/ingest/build-summary-li.sh"
"$ROOT/scripts/ingest/ingest-csv-smoke.sh"

if [[ -f "$LIC_CSV" ]]; then
  if ! "$ROOT/scripts/ingest/build-summary-li.sh"; then
    python3 "$ROOT/scripts/ingest/build_summary.py" "$LIC_ROOT" "$LIS_ROOT"
  fi
elif [[ -f "$LIS_CSV" ]]; then
  echo "ingest: no lic CSV — merging HTTP only from $LIS_CSV"
  python3 "$ROOT/scripts/ingest/merge_lis_http_into_summary.py" "$LIS_CSV"
else
  echo "ingest: skip summary (no lic or lis CSV)" >&2
fi

python3 "$ROOT/scripts/record-benchmark-history.py" || true
"$ROOT/scripts/regression-check.sh" || true
