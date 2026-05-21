#!/usr/bin/env bash
# Copy tier5_http harness from a lis checkout into vendor/lis-tier5/.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${LIS_ROOT:-$ROOT/../lis}"
DEST="$ROOT/vendor/lis-tier5"

if [[ ! -d "$SRC/benchmarks/tier5_http" ]]; then
  echo "error: $SRC/benchmarks/tier5_http missing" >&2
  exit 1
fi

rm -rf "$DEST/benchmarks/tier5_http"
mkdir -p "$DEST/benchmarks"
cp -a "$SRC/benchmarks/tier5_http" "$DEST/benchmarks/"
[[ -f "$SRC/benchmarks/tier5_http/README.md" ]] && cp "$SRC/benchmarks/tier5_http/README.md" "$DEST/README.md"
echo "synced tier5_http -> $DEST/benchmarks/tier5_http"
