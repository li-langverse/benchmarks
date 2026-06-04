#!/usr/bin/env bash
# Merge tier shards into results/latest.csv and verify OS tags for nightly macOS/Windows uploads.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TIER_DIR="${1:-$ROOT/results}"
OUT="${BENCHMARKS_CSV:-$ROOT/results/latest.csv}"

if [[ -z "${EXPECT_OS:-}" ]]; then
  case "$(uname -s)" in
    Darwin*) EXPECT_OS=macos ;;
    MINGW*|MSYS*|CYGWIN*|Windows*) EXPECT_OS=windows ;;
    Linux*) EXPECT_OS=linux ;;
    *) EXPECT_OS=unknown ;;
  esac
fi

rm -f "$OUT"
shopt -s nullglob
tier_csvs=("$TIER_DIR"/tier-*.csv)
if [[ ${#tier_csvs[@]} -eq 0 ]]; then
  echo "finalize-nightly-os-csv: no tier-*.csv under $TIER_DIR" >&2
  exit 1
fi

"$ROOT/scripts/merge-benchmark-tier-csvs.sh" "$TIER_DIR"
# shellcheck source=lib/bench-python.sh
source "$ROOT/scripts/lib/bench-python.sh"
bench_python "$ROOT/scripts/retag-csv-os.py" "$OUT" --os "$EXPECT_OS"
bench_python "$ROOT/scripts/check-csv-os-tags.py" "$OUT" --expect-os "$EXPECT_OS" --min-rows 1
echo "finalize-nightly-os-csv: OK ($OUT, expect_os=$EXPECT_OS, tiers=${#tier_csvs[@]})"
