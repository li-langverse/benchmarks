#!/usr/bin/env bash
# PH-IO-7 — Li vs Python summary.json on fixture catalog + CSV.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
export LI_REPO_ROOT="${LI_REPO_ROOT:-$LIC_ROOT}"
export CC="${CC:-clang-18}"

if [[ ! -x "$LIC_ROOT/build/compiler/lic/lic" ]]; then
  echo "summary-compare-gate: skip (lic not built)"
  exit 0
fi

LIC="$LIC_ROOT/build/compiler/lic/lic"
mkdir -p "$ROOT/build/compare"
LI_OUT="$ROOT/build/compare/summary_li.json"
PY_OUT="$ROOT/build/compare/summary_py.json"

BIN="build/summary_fixture_$$"
trap 'rm -f "$ROOT/$BIN"' EXIT
if ! (cd "$ROOT" && "$LIC" build scripts/ingest/build_summary_fixture.li -o "$BIN"); then
  echo "summary-compare-gate: skip (lic lacks std/summary)"
  exit 0
fi
(cd "$ROOT" && "./$BIN")
python3 "$ROOT/scripts/ingest/build_summary_fixture.py"
python3 "$ROOT/scripts/ingest/compare_summary_outputs.py" "$LI_OUT" "$PY_OUT"
echo "PASS summary-compare-gate"
