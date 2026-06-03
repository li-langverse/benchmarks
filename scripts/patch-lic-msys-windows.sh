#!/usr/bin/env bash
# Apply lic Windows/MSYS build shims before setup-lic-for-bench on GHA windows-latest.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=lib/bench-python.sh
source "$ROOT/scripts/lib/bench-python.sh"
LIC="${LIC_ROOT:-$ROOT/lic}"
PLATFORM_HPP="$LIC/compiler/codegen/include/li/platform.hpp"
RESOURCE_CPP="$LIC/compiler/common/resource_options.cpp"
MAIN_CPP="$LIC/compiler/lic/main.cpp"

if grep -q 'set_env_var' "$PLATFORM_HPP" 2>/dev/null; then
  echo "patch-lic-msys-windows: lic already patched"
  exit 0
fi

bench_python <<'PY'
from __future__ import annotations

import os
from pathlib import Path

lic = Path(os.environ["LIC_ROOT"])
platform_hpp = lic / "compiler/codegen/include/li/platform.hpp"
resource_cpp = lic / "compiler/common/resource_options.cpp"
main_cpp = lic / "compiler/lic/main.cpp"

helper = """
/// Portable environment variable setter (POSIX setenv / Windows _putenv_s).
inline void set_env_var(const char* name, const char* value, int overwrite = 1) {
#if defined(_WIN32)
  (void)overwrite;
  _putenv_s(name, value);
#else
  setenv(name, value, overwrite);
#endif
}

"""

text = platform_hpp.read_text(encoding="utf-8")
if "set_env_var" not in text:
    text = text.replace("}  // namespace li\n", helper + "}  // namespace li\n")
    platform_hpp.write_text(text, encoding="utf-8")

text = resource_cpp.read_text(encoding="utf-8")
if "void set_env_var" not in text:
    needle = "namespace li {\nnamespace {\n\n"
    insert = """namespace li {
namespace {

#if defined(_WIN32)
void set_env_var(const char* name, const char* value, int /*overwrite*/) {
  _putenv_s(name, value);
}
#else
void set_env_var(const char* name, const char* value, int overwrite) {
  setenv(name, value, overwrite);
}
#endif

"""
    if needle not in text:
        raise SystemExit(f"resource_options.cpp layout unexpected in {resource_cpp}")
    text = text.replace(needle, insert, 1)
text = text.replace(
    'setenv("LI_COMPILE_JOBS"',
    'set_env_var("LI_COMPILE_JOBS"',
)
resource_cpp.write_text(text, encoding="utf-8")

text = main_cpp.read_text(encoding="utf-8")
for old, new in [
    ('setenv("LI_BUILD_DIR"', 'li::set_env_var("LI_BUILD_DIR"'),
    ('setenv("LI_COMPILE_JOBS"', 'li::set_env_var("LI_COMPILE_JOBS"'),
    ('setenv("LI_MAX_MEMORY_MB"', 'li::set_env_var("LI_MAX_MEMORY_MB"'),
]:
    text = text.replace(old, new)
main_cpp.write_text(text, encoding="utf-8")

cmake_lists = lic / "CMakeLists.txt"
cmake_text = cmake_lists.read_text(encoding="utf-8")
needle = "include(HandleLLVMOptions)"
if needle in cmake_text and "if(NOT WIN32)" not in cmake_text:
    cmake_text = cmake_text.replace(
        needle,
        "if(NOT WIN32)\ninclude(HandleLLVMOptions)\nendif()",
        1,
    )
    cmake_lists.write_text(cmake_text, encoding="utf-8")
print("patch-lic-msys-windows: applied set_env_var shims")
PY

echo "patch-lic-msys-windows: OK"
