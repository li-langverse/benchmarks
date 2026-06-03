#!/usr/bin/env bash
# Fix LLVM→Ninja CXX define quoting on MSYS2 UCRT64 (broken -D_GLIBCXX_USE_CXX11_ABI="1 -D_...").
set -euo pipefail
BUILD="${1:?build dir}"
# shellcheck source=lib/bench-python.sh
source "$(cd "$(dirname "$0")" && pwd)/lib/bench-python.sh"
bench_python - "$BUILD" <<'PY'
from __future__ import annotations

import re
import sys
from pathlib import Path

build = Path(sys.argv[1])
bad_literal = (
    '-D_GLIBCXX_USE_CXX11_ABI="1 -D_FILE_OFFSET_BITS=64 '
    '-D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS"'
)
good = (
    "-D_GLIBCXX_USE_CXX11_ABI=1 -D_FILE_OFFSET_BITS=64 "
    "-D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS"
)
mangled = re.compile(
    r'-D_GLIBCXX_USE_CXX11_ABI="1\s+-D_FILE_OFFSET_BITS=64\s+'
    r'-D__STDC_CONSTANT_MACROS\s+-D__STDC_FORMAT_MACROS\s+-D__STDC_LIMIT_MACROS"'
)
changed = 0
for path in build.rglob("*.ninja"):
    text = path.read_text(encoding="utf-8", errors="replace")
    new_text, n = mangled.subn(good, text)
    if n == 0 and bad_literal in text:
        new_text = text.replace(bad_literal, good)
        n = 1
    if n:
        path.write_text(new_text, encoding="utf-8")
        changed += 1
if changed:
    print(f"fix-lic-msys-cmake-flags: repaired {changed} ninja file(s)")
else:
    print("fix-lic-msys-cmake-flags: no mangled flags found (ok)")
PY
