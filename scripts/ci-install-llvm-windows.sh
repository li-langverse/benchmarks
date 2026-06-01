#!/usr/bin/env bash
# Install LLVM 22 *development* tree on Windows (LLVMConfig.cmake).
# Chocolatey's LLVM EXE is toolchain-only and lacks CMake package files.
set -euo pipefail

LLVM_VERSION="${LI_LLVM_VERSION:-22.1.0}"
LLVM_ORG="llvmorg-${LLVM_VERSION}"
ARCHIVE="clang+llvm-${LLVM_VERSION}-x86_64-pc-windows-msvc.tar.xz"
URL="https://github.com/llvm/llvm-project/releases/download/${LLVM_ORG}/${ARCHIVE}"

ROOT="${LLVM_WIN_ROOT:-${GITHUB_WORKSPACE:-.}/.llvm-win-${LLVM_VERSION}}"
CMAKE_DIR="${ROOT}/lib/cmake/llvm"

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
  tar -xf "$archive_path" -C "$(dirname "$ROOT")"
  extracted="$(dirname "$ROOT")/clang+llvm-${LLVM_VERSION}-x86_64-pc-windows-msvc"
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

if [[ -n "${GITHUB_ENV:-}" ]]; then
  {
    echo "LLVM_DIR=${CMAKE_DIR}"
    echo "CC=${ROOT}/bin/clang.exe"
    echo "CXX=${ROOT}/bin/clang++.exe"
  } >> "$GITHUB_ENV"
  echo "${ROOT}/bin" >> "$GITHUB_PATH"
fi

export LLVM_DIR="${CMAKE_DIR}"
export CC="${ROOT}/bin/clang.exe"
export CXX="${ROOT}/bin/clang++.exe"
export PATH="${ROOT}/bin:${PATH}"

echo "ci-install-llvm-windows: LLVM_DIR=${LLVM_DIR}"
"${CC}" --version
