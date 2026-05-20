#!/usr/bin/env bash
# Run lis tier-5 bench (nginx+wrk) and plot PNGs into data/visuals/latest/.
# Does not rewrite data/latest/summary.json — avoids ingest conflicts with other agents.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIS_ROOT="${LIS_ROOT:-$ROOT/../lis}"

if [[ ! -f "$LIS_ROOT/benchmarks/tier5_http/harness/bench_http.py" ]]; then
  echo "error: set LIS_ROOT to a lis checkout (harness missing)" >&2
  exit 1
fi

export MPLBACKEND=Agg
PROFILE="${BENCH_HTTP_PROFILE:-ci}"
echo "==> bench_http.py --profile $PROFILE"
(cd "$LIS_ROOT" && python3 benchmarks/tier5_http/harness/bench_http.py --profile "$PROFILE")
echo "==> plot HTTP visuals"
LIS_ROOT="$LIS_ROOT" LIC_ROOT="${LIC_ROOT:-}" "$ROOT/scripts/render-benchmark-visuals.sh"
echo "CSV: $LIS_ROOT/results/latest.csv"
echo "Plots: $ROOT/data/visuals/latest/http_*.png"
