#!/usr/bin/env bash
# Apply lic Windows/MSYS build shims before setup-lic-for-bench on GHA windows-latest.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC="${LIC_ROOT:-$ROOT/lic}"
PATCH="$ROOT/scripts/patches/lic-win-setenv.patch"
if [[ ! -f "$PATCH" ]]; then
  echo "patch-lic-msys-windows: missing $PATCH" >&2
  exit 1
fi
if grep -q 'set_env_var' "$LIC/compiler/codegen/include/li/platform.hpp" 2>/dev/null; then
  echo "patch-lic-msys-windows: lic already patched"
  exit 0
fi
if ! patch -d "$LIC" --forward -p1 < "$PATCH"; then
  git -C "$LIC" apply "$PATCH"
fi
echo "patch-lic-msys-windows: OK"
