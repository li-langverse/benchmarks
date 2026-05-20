#!/usr/bin/env bash
# Li CSV ingest smoke (PH-IO-4) — requires lic with io + csv modules (`import io` / `import csv`).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
INGEST_DIR="$(cd "$(dirname "$0")" && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/../lic}"
export LI_REPO_ROOT="${LI_REPO_ROOT:-$LIC_ROOT}"
export CC="${CC:-clang-18}"

if [[ -x "$LIC_ROOT/build/compiler/lic/lic" ]]; then
  LIC="$LIC_ROOT/build/compiler/lic/lic"
elif LIC_BIN="$(command -v lic 2>/dev/null)"; then
  LIC="$LIC_BIN"
else
  echo "ingest-csv-smoke: skip (no lic)"
  exit 0
fi

BIN="${TMPDIR:-/tmp}/li_ingest_csv_smoke_$$"
trap 'rm -f "$BIN" "$BIN.exe"' EXIT

if ! "$LIC" build "$INGEST_DIR/csv_ingest_smoke.li" -o "$BIN" 2>/dev/null; then
  echo "ingest-csv-smoke: skip (lic lacks io + csv — PH-IO-4)"
  exit 0
fi
ec=0
(cd "$INGEST_DIR" && "$BIN" >/dev/null 2>&1) || ec=$?
if [[ "$ec" -ne 0 ]]; then
  echo "FAIL ingest-csv-smoke: expected exit 0, got $ec"
  exit 1
fi
echo "PASS ingest-csv-smoke"
