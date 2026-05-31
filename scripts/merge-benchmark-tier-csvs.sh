#!/usr/bin/env bash
# Merge parallel tier-group CSV shards into results/latest.csv (+ tier-5 HTTP sidecars).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
OUT="${BENCHMARKS_CSV:-$ROOT/results/latest.csv}"
TIER_DIR="${1:-$ROOT/results}"

mkdir -p "$(dirname "$OUT")"
shopt -s nullglob
tier_csvs=("$TIER_DIR"/tier-*.csv)
if [[ ${#tier_csvs[@]} -eq 0 ]]; then
  echo "merge-benchmark-tier-csvs: no tier-*.csv under $TIER_DIR" >&2
  exit 1
fi

python3 "$ROOT/scripts/ingest/merge_bench_csv_artifacts.py" "$OUT" "${tier_csvs[@]}"

if [[ -f "$ROOT/vendor/lis-tier5/results/latest.csv" ]] || [[ -f "$LIC_ROOT/benchmarks/results/http_tier5.csv" ]]; then
  export BENCHMARKS_CSV="$OUT"
  python3 "$ROOT/scripts/merge-tier5-http-into-csv.py" "$ROOT" "$LIC_ROOT"
fi

echo "merged ${#tier_csvs[@]} tier shards -> $OUT"
