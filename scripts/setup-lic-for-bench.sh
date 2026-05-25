#!/usr/bin/env bash
# Build lic + li-httpd for local / agent benchmark runs (Debian/Ubuntu).
set -euo pipefail
SCRIPT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIC_ROOT="${LIC_ROOT:-$SCRIPT_ROOT/lic}"
if [[ ! -d "$LIC_ROOT" ]]; then
  echo "missing LIC_ROOT=$LIC_ROOT" >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
need_apt=0
for pkg in ninja-build cmake llvm-22-dev libzstd-dev clang-22 g++-13 wrk nginx \
  apache2 lighttpd nodejs; do
  dpkg -s "$pkg" >/dev/null 2>&1 || need_apt=1
done
if [[ "$need_apt" == "1" ]]; then
  sudo apt-get update -qq
  sudo apt-get install -y -qq build-essential g++-13 gcc-13 clang-22 \
    ninja-build cmake llvm-22-dev libzstd-dev libstdc++-13-dev libomp-22-dev \
    wrk nginx apache2 lighttpd nodejs
fi
# Bun is optional (not in Debian main); tier-5 skips when `bun` is missing.
command -v bun >/dev/null 2>&1 || echo "note: install bun for tier-5 bun oracle (optional)" >&2

export LLVM_DIR="${LLVM_DIR:-/usr/lib/llvm-22/lib/cmake/llvm}"
export CXX=g++-13 CC=gcc-13 LI_REPO_ROOT="$LIC_ROOT"
echo "==> lic compiler"
( cd "$LIC_ROOT" && ./scripts/build.sh )
echo "==> li-httpd"
( cd "$LIC_ROOT" && CC=clang-22 CXX=clang++-22 ./build/compiler/lic/lic build \
  packages/li-net-httpd/src/lib.li -o build/li-httpd )
# Requires `import std.runtime.seam` in lib.li (trusted ABI); package-only build may omit Li codegen.
test -x "$LIC_ROOT/build/li-httpd"
echo "OK LIC_ROOT=$LIC_ROOT"
