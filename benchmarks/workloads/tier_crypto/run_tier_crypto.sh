#!/usr/bin/env bash
# tier_crypto — run validity + throughput harness (not smoke).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$ROOT/../../.." && pwd)"
HARNESS="$REPO/harness/bench_crypto.py"
PROFILE="${TIER_CRYPTO_PROFILE:-ci}"
EXTRA=()
if [[ "${1:-}" == "--smoke" ]]; then
  echo "tier_crypto: --smoke retired; use --profile ci" >&2
  PROFILE=ci
elif [[ "${1:-}" == "--profile" ]]; then
  PROFILE="${2:-ci}"
  shift 2 || true
fi
[[ -f "$HARNESS" ]] || { echo "tier_crypto: missing $HARNESS" >&2; exit 1; }
export LIC_ROOT="${LIC_ROOT:-$REPO/../lic}"
python3 "$HARNESS" --profile "$PROFILE" "$@"
echo "tier_crypto-gate-runner: OK"
