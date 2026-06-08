#!/usr/bin/env bash
# Install LLVM 22 *development* tree on Windows (LLVMConfig.cmake).
# Chocolatey's LLVM EXE is toolchain-only and lacks a reliable CMake dev package on GHA.
set -euo pipefail
export MSYS2_ARG_CONV_EXCL="*"

LLVM_VERSION="${LI_LLVM_VERSION:-22.1.0}"
LLVM_ORG="llvmorg-${LLVM_VERSION}"
ARCHIVE="clang+llvm-${LLVM_VERSION}-x86_64-pc-windows-msvc.tar.xz"
URL="https://github.com/llvm/llvm-project/releases/download/${LLVM_ORG}/${ARCHIVE}"

ROOT="${LLVM_WIN_ROOT:-${RUNNER_TEMP:-${GITHUB_WORKSPACE:-.}}/.llvm-win-${LLVM_VERSION}}"
CMAKE_DIR="${ROOT}/lib/cmake/llvm"

_env_path() {
  local p="$1"
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -u "$p"
  else
    echo "${p//\\//}"
  fi
}

_extract_archive() {
  local archive="$1" parent="$2"
  rm -rf "$parent/clang+llvm-${LLVM_VERSION}-x86_64-pc-windows-msvc"
  if tar --force-local -xf "$archive" -C "$parent" 2>/dev/null; then
    return 0
  fi
  if tar -xf "$archive" -C "$parent" 2>/dev/null; then
    return 0
  fi
  echo "ci-install-llvm-windows: tar failed; extracting with python" >&2
  # shellcheck source=lib/bench-python.sh
  source "$(cd "$(dirname "$0")" && pwd)/lib/bench-python.sh"
  bench_python - "$archive" "$parent" <<'PY'
import lzma
import os
import sys
import tarfile

archive, parent = sys.argv[1], sys.argv[2]
os.makedirs(parent, exist_ok=True)
with lzma.open(archive) as raw:
    with tarfile.open(fileobj=raw) as tf:
        if hasattr(tarfile, "data_filter"):
            tf.extractall(parent, filter="data")
        else:
            tf.extractall(parent)
PY
}

if [[ -f "${CMAKE_DIR}/LLVMConfig.cmake" ]]; then
  echo "ci-install-llvm-windows: reuse ${CMAKE_DIR}"
else
  echo "ci-install-llvm-windows: download ${ARCHIVE}"
  cache_dir="${GITHUB_WORKSPACE:-.}/.llvm-cache"
  mkdir -p "$cache_dir" "$(dirname "$ROOT")"
  archive_path="${cache_dir}/${ARCHIVE}"
  if [[ ! -s "$archive_path" ]]; then
    curl -fsSL -o "$archive_path" "$URL"
  fi
  rm -rf "$ROOT"
  extract_parent="$(cd "$(dirname "$ROOT")" && pwd)"
  _extract_archive "$archive_path" "$extract_parent"
  extracted="$extract_parent/clang+llvm-${LLVM_VERSION}-x86_64-pc-windows-msvc"
  if [[ ! -d "$extracted" ]]; then
    echo "ci-install-llvm-windows: expected extract dir missing: $extracted" >&2
    exit 1
  fi
  mv "$extracted" "$ROOT"
fi

if [[ ! -f "${CMAKE_DIR}/LLVMConfig.cmake" ]]; then
  echo "ci-install-llvm-windows: LLVMConfig.cmake not found under ${ROOT}" >&2
  exit 1
fi

env_root="$(_env_path "$ROOT")"
env_cmake="${env_root}/lib/cmake/llvm"

if [[ -n "${GITHUB_ENV:-}" ]]; then
  {
    echo "LLVM_DIR=${env_cmake}"
    echo "LLVM_WIN_ROOT=${env_root}"
  } >> "$GITHUB_ENV"
  echo "${env_root}/bin" >> "$GITHUB_PATH"
fi

export LLVM_DIR="${env_cmake}"
export LLVM_WIN_ROOT="${env_root}"
export PATH="${ROOT}/bin:${PATH}"

echo "ci-install-llvm-windows: LLVM_DIR=${LLVM_DIR}"
echo "ci-install-llvm-windows: LLVM_WIN_ROOT=${LLVM_WIN_ROOT}"
"${ROOT}/bin/clang.exe" --version
