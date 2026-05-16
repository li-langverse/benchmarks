#!/usr/bin/env bash
# PH-IO-7 — Li summary.json build (requires lic with std/summary).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
INGEST_DIR="$(cd "$(dirname "$0")" && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
export LI_REPO_ROOT="${LI_REPO_ROOT:-$LIC_ROOT}"
export CC="${CC:-clang-18}"

if [[ -x "$LIC_ROOT/build/compiler/lic/lic" ]]; then
  LIC="$LIC_ROOT/build/compiler/lic/lic"
elif LIC_BIN="$(command -v lic 2>/dev/null)"; then
  LIC="$LIC_BIN"
else
  echo "build-summary-li: skip (no lic)"
  exit 1
fi

mkdir -p "$ROOT/build"
BIN="build/ingest_summary_li_$$"
trap 'rm -f "$ROOT/$BIN" "$ROOT/$BIN.exe"' EXIT

(cd "$ROOT" && "$LIC" build "$INGEST_DIR/build_summary.li" -o "$BIN")
ec=0
(cd "$ROOT" && "./$BIN") || ec=$?
if [[ "$ec" -ne 0 ]]; then
  echo "FAIL build-summary-li: exit $ec"
  exit 1
fi
if [[ ! -f "$ROOT/data/latest/summary.json" ]]; then
  echo "FAIL build-summary-li: missing data/latest/summary.json"
  exit 1
fi
echo "PASS build-summary-li"
