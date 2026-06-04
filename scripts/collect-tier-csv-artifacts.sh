#!/usr/bin/env bash
# Collect tier-*.csv from download-artifact merge-multiple tree into results/.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ARTIFACTS_ROOT="${1:-$ROOT/artifacts/tiers}"
OUT_DIR="${2:-$ROOT/results}"

mkdir -p "$OUT_DIR"
found=0
if [[ -d "$ARTIFACTS_ROOT" ]]; then
  while IFS= read -r -d '' f; do
    cp "$f" "$OUT_DIR/$(basename "$f")"
    found=$((found + 1))
  done < <(find "$ARTIFACTS_ROOT" -type f \( -name 'tier-*.csv' -o -name 'tier-tier*.csv' \) -print0 2>/dev/null || true)
fi
echo "collect-tier-csv-artifacts: copied $found shard(s) into $OUT_DIR"
ls -la "$OUT_DIR" || true
if [[ "$found" -eq 0 ]]; then
  echo "collect-tier-csv-artifacts: no tier-*.csv under $ARTIFACTS_ROOT" >&2
  find "$ARTIFACTS_ROOT" 2>/dev/null | head -50 || true
  exit 1
fi
