#!/usr/bin/env bash
# tier_crypto smoke runner — full microbench wiring follows in I4b.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SMOKE=0
if [[ "${1:-}" == "--smoke" ]]; then
  SMOKE=1
fi
BASE="$ROOT/baseline.csv"
[[ -f "$BASE" ]] || { echo "tier_crypto: missing baseline.csv" >&2; exit 1; }
grep -q 'sha256' "$BASE" || { echo "tier_crypto: baseline missing sha256 row" >&2; exit 1; }
if [[ "$SMOKE" -eq 1 ]]; then
  echo "tier_crypto: smoke OK (baseline present)"
  exit 0
fi
echo "tier_crypto: use --smoke until harness wired" >&2
exit 1
