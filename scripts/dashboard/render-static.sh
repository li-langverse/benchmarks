#!/usr/bin/env bash
# PH-IO-5 — static dashboard via lic std/plot (no Node).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DASH_DIR="$(cd "$(dirname "$0")" && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"
export LI_REPO_ROOT="${LI_REPO_ROOT:-$LIC_ROOT}"
export CC="${CC:-clang-18}"

if [[ ! -f "$ROOT/data/latest/summary.json" ]]; then
  echo "render-static: missing data/latest/summary.json (run ingest first)"
  exit 1
fi

if [[ -x "$LIC_ROOT/build/compiler/lic/lic" ]]; then
  LIC="$LIC_ROOT/build/compiler/lic/lic"
elif LIC_BIN="$(command -v lic 2>/dev/null)"; then
  LIC="$LIC_BIN"
else
  echo "render-static: skip (no lic with std/plot)"
  exit 0
fi

mkdir -p "$ROOT/static-dashboard/latest" "$ROOT/static-dashboard/assets"
BIN="${TMPDIR:-/tmp}/li_render_dashboard_$$"
trap 'rm -f "$BIN" "$BIN.exe"' EXIT

"$LIC" build "$DASH_DIR/render_dashboard.li" -o "$BIN"
ec=0
(cd "$ROOT" && "$BIN") || ec=$?
if [[ "$ec" -ne 0 ]]; then
  echo "FAIL render-static: plot_render_dashboard exit $ec"
  exit 1
fi

cp "$ROOT/data/latest/summary.json" "$ROOT/static-dashboard/latest/summary.json"
if [[ ! -f "$ROOT/static-dashboard/assets/style.css" ]]; then
  echo "render-static: missing assets/style.css (plot runtime should write it)"
  exit 1
fi
if ! grep -q '<svg' "$ROOT/static-dashboard/index.html"; then
  echo "FAIL render-static: index.html has no SVG charts"
  exit 1
fi
echo "PASS render-static → static-dashboard/"
