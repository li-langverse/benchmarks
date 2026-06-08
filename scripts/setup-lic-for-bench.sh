#!/usr/bin/env bash
# Build lic + li-httpd for local / agent benchmark runs (Debian/Ubuntu).
set -euo pipefail
SCRIPT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_PARENT="$(cd "$SCRIPT_ROOT/.." && pwd)"
if [[ -z "${LIC_ROOT:-}" ]]; then
  if [[ -d "$SCRIPT_ROOT/lic" ]]; then
    LIC_ROOT="$SCRIPT_ROOT/lic"
  elif [[ -d "$REPO_PARENT/lic" ]]; then
    LIC_ROOT="$REPO_PARENT/lic"
  else
    LIC_ROOT="$SCRIPT_ROOT/lic"
  fi
fi
# shellcheck source=lib/resolve-lic-bench.sh
source "$SCRIPT_ROOT/scripts/lib/resolve-lic-bench.sh"
if [[ ! -d "$LIC_ROOT" ]]; then
  echo "missing LIC_ROOT=$LIC_ROOT" >&2
  exit 1
fi

case "$(uname -s)" in
  Darwin*)
    export LI_REPO_ROOT="$LIC_ROOT"
    if command -v brew >/dev/null 2>&1 && [[ -z "${LLVM_DIR:-}" ]]; then
      llvm_prefix="$(brew --prefix llvm@22 2>/dev/null || true)"
      if [[ -z "$llvm_prefix" || ! -d "$llvm_prefix/lib/cmake/llvm" ]]; then
        if [[ -n "${GITHUB_ACTIONS:-}" ]]; then
          echo "==> installing llvm@22 via Homebrew" >&2
          brew install llvm@22
          llvm_prefix="$(brew --prefix llvm@22)"
        fi
      fi
      if [[ -n "$llvm_prefix" && -d "$llvm_prefix/lib/cmake/llvm" ]]; then
        export LLVM_DIR="$llvm_prefix/lib/cmake/llvm"
      fi
    fi
    if [[ -z "${LLVM_DIR:-}" ]]; then
      echo "LLVM 22 required on macOS: brew install llvm@22" >&2
      echo "  export LLVM_DIR=\$(brew --prefix llvm@22)/lib/cmake/llvm" >&2
      exit 1
    fi
    export CC="${CC:-clang}"
    export CXX="${CXX:-clang++}"
    echo "==> lic compiler (macOS — skip apt)"
    (cd "$LIC_ROOT" && ./scripts/build.sh)
    echo "OK LIC_ROOT=$LIC_ROOT"
    exit 0
    ;;
  MINGW*|MSYS*|CYGWIN*|Windows*)
    export LI_REPO_ROOT="$LIC_ROOT"
    if [[ -z "${LLVM_DIR:-}" ]]; then
      for d in \
        "/ucrt64/lib/cmake/llvm" \
        "${LLVM_WIN_ROOT:-}/lib/cmake/llvm" \
        "${RUNNER_TEMP:-/tmp}/.llvm-win-22.1.0/lib/cmake/llvm" \
        "/c/Program Files/LLVM/lib/cmake/llvm" \
        "/c/Program Files/LLVM/lib/cmake/llvm-22"; do
        if [[ -f "$d/LLVMConfig.cmake" ]]; then
          export LLVM_DIR="$d"
          break
        fi
      done
    fi
    if [[ -n "${LLVM_WIN_ROOT:-}" && -x "${LLVM_WIN_ROOT}/bin/clang.exe" ]]; then
      export CC="${LLVM_WIN_ROOT}/bin/clang.exe"
      export CXX="${LLVM_WIN_ROOT}/bin/clang++.exe"
      export PATH="${LLVM_WIN_ROOT}/bin:${PATH}"
    fi
    if [[ -z "${LLVM_DIR:-}" ]]; then
      echo "LLVM 22 dev required on Windows: ./scripts/ci-install-llvm-windows.sh" >&2
      exit 1
    fi
    export CC="${CC:-clang}"
    export CXX="${CXX:-clang++}"
    echo "==> lic compiler (Windows — LLVM_DIR=$LLVM_DIR)"
    BUILD_DIR="$LIC_ROOT/build"
    rm -rf "$BUILD_DIR"
    (cd "$LIC_ROOT" && cmake -B build -G Ninja -DLLVM_DIR="$LLVM_DIR")
    chmod +x "$SCRIPT_ROOT/scripts/fix-lic-msys-cmake-flags.sh"
    "$SCRIPT_ROOT/scripts/fix-lic-msys-cmake-flags.sh" "$BUILD_DIR"
    (cd "$LIC_ROOT" && cmake --build build -j "$(nproc 2>/dev/null || echo 4)")
    win_lic_dir="$BUILD_DIR/compiler/lic"
    if [[ -x "$win_lic_dir/lic.exe" && ! -e "$win_lic_dir/lic" ]]; then
      (cd "$win_lic_dir" && ln -sf lic.exe lic)
    fi
    echo "OK LIC_ROOT=$LIC_ROOT LIC=$(resolve_lic_bench_bin "$LIC_ROOT")"
    exit 0
    ;;
esac

_linux_skip_apt() {
  [[ "${LIC_CI_CONTAINER:-}" == "1" ]] && return 0
  ! command -v sudo >/dev/null 2>&1
}

_linux_require_build_toolchain() {
  local missing=()
  for pkg in ninja-build cmake llvm-22-dev clang-22; do
    dpkg -s "$pkg" >/dev/null 2>&1 || missing+=("$pkg")
  done
  if ! command -v clang++ >/dev/null 2>&1 && ! command -v g++ >/dev/null 2>&1; then
    missing+=("clang++/g++")
  fi
  if ((${#missing[@]})); then
    echo "setup-lic-for-bench: missing build packages (no sudo): ${missing[*]}" >&2
    exit 1
  fi
}

export DEBIAN_FRONTEND=noninteractive
if _linux_skip_apt; then
  echo "==> lic compiler (Linux lic-ci — skip apt)"
  _linux_require_build_toolchain
elif [[ -x "$LIC_ROOT/scripts/ci-install-llvm.sh" ]]; then
  sudo LI_LLVM_MAJOR=22 bash "$LIC_ROOT/scripts/ci-install-llvm.sh"
else
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
fi
if ! _linux_skip_apt; then
  need_apt=0
  for pkg in g++-13 wrk nginx apache2 lighttpd nodejs; do
    dpkg -s "$pkg" >/dev/null 2>&1 || need_apt=1
  done
  if [[ "$need_apt" == "1" ]]; then
    sudo apt-get update -qq
    sudo apt-get install -y -qq build-essential g++-13 gcc-13 libstdc++-13-dev \
      wrk nginx apache2 lighttpd nodejs
  fi
fi
# Bun is optional (not in Debian main); tier-5 skips when `bun` is missing.
command -v bun >/dev/null 2>&1 || echo "note: install bun for tier-5 bun oracle (optional)" >&2

export LLVM_DIR="${LLVM_DIR:-/usr/lib/llvm-22/lib/cmake/llvm}"
if _linux_skip_apt; then
  export CC="${CC:-clang-22}"
  export CXX="${CXX:-clang++-22}"
  command -v "$CC" >/dev/null 2>&1 || CC=clang
  command -v "$CXX" >/dev/null 2>&1 || CXX=clang++
else
  export CXX=g++-13 CC=gcc-13
fi
export LI_REPO_ROOT="$LIC_ROOT"
echo "==> lic compiler"
( cd "$LIC_ROOT" && ./scripts/build.sh )

echo "==> li-httpd"
# lic link invokes clang -x ir; gcc cannot compile LLVM IR (BN1 nightly prepare-lic-linux).
HTTPD_CC="${LI_HTTPD_CC:-clang-22}"
HTTPD_CXX="${LI_HTTPD_CXX:-clang++-22}"
if ! command -v "$HTTPD_CC" >/dev/null 2>&1; then
  HTTPD_CC=clang
  HTTPD_CXX=clang++
fi
( cd "$LIC_ROOT" && CC="$HTTPD_CC" CXX="$HTTPD_CXX" bash ./scripts/build-li-httpd.sh )
test -x "$LIC_ROOT/build/li-httpd"
echo "OK LIC_ROOT=$LIC_ROOT"
