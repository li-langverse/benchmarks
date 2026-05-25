#!/usr/bin/env bash
# Verify dashboard-next static export has core routes and bench drill-down pages.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${DASHBOARD_OUT:-$ROOT/dashboard-next/out}"
MIN_BENCH_PAGES="${MIN_BENCH_PAGES:-145}"
MATRIX_PAGE="${OUT}/matrix/index.html"

if [ ! -f "${OUT}/index.html" ]; then
  echo "check-dashboard-static-routes: FAIL missing ${OUT}/index.html (run npm run build first)" >&2
  exit 1
fi

if [ ! -f "${MATRIX_PAGE}" ]; then
  echo "check-dashboard-static-routes: FAIL missing ${MATRIX_PAGE}" >&2
  exit 1
fi

bench_count=0
if [ -d "${OUT}/bench" ]; then
  bench_count="$(find "${OUT}/bench" -mindepth 2 -maxdepth 2 -name index.html 2>/dev/null | wc -l | tr -d ' ')"
fi
if [ "${bench_count:-0}" -lt "${MIN_BENCH_PAGES}" ]; then
  echo "check-dashboard-static-routes: FAIL bench pages ${bench_count} < ${MIN_BENCH_PAGES}" >&2
  exit 1
fi

if [ ! -f "${OUT}/latest/summary.json" ]; then
  echo "check-dashboard-static-routes: WARN missing ${OUT}/latest/summary.json (Pages runtime fetch)" >&2
fi

echo "PASS check-dashboard-static-routes (index, matrix, bench pages=${bench_count})"
