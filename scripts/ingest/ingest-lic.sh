#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
chmod +x "$ROOT/scripts/ingest/ingest-csv-smoke.sh" "$ROOT/scripts/ingest/build-summary-li.sh"
"$ROOT/scripts/ingest/ingest-csv-smoke.sh"
if ! "$ROOT/scripts/ingest/build-summary-li.sh"; then
  python3 "$ROOT/scripts/ingest/build_summary.py" "$LIC_ROOT" "$LIS_ROOT"
fi
"$ROOT/scripts/regression-check.sh" || true
