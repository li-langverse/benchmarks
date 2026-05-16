#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/../li}"
LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"
chmod +x "$ROOT/scripts/ingest/ingest-csv-smoke.sh"
"$ROOT/scripts/ingest/ingest-csv-smoke.sh"
python3 "$ROOT/scripts/ingest/build_summary.py" "$LIC_ROOT" "$LIS_ROOT"
"$ROOT/scripts/regression-check.sh" || true
