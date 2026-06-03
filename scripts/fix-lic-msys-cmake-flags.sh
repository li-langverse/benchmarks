#!/usr/bin/env bash
# Fix LLVM→Ninja CXX define quoting on MSYS2 UCRT64 (broken -D_GLIBCXX_USE_CXX11_ABI="1 -D_...").
set -euo pipefail
BUILD="${1:?build dir}"
# shellcheck source=lib/bench-python.sh
source "$(cd "$(dirname "$0")" && pwd)/lib/bench-python.sh"
bench_python <<'PY'
from __future__ import annotations

import sys
from pathlib import Path

build = Path(sys.argv[1])
bad = (
    '-D_GLIBCXX_USE_CXX11_ABI="1 -D_FILE_OFFSET_BITS=64 '
    '-D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS"'
)
good = (
    "-D_GLIBCXX_USE_CXX11_ABI=1 -D_FILE_OFFSET_BITS=64 "
    "-D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS"
)
changed = 0
for path in build.rglob("*.ninja"):
    text = path.read_text(encoding="utf-8", errors="replace")
    if bad not in text:
        continue
    path.write_text(text.replace(bad, good), encoding="utf-8")
    changed += 1
if changed:
    print(f"fix-lic-msys-cmake-flags: repaired {changed} ninja file(s)")
else:
    print("fix-lic-msys-cmake-flags: no mangled flags found (ok)")
PY
