#!/usr/bin/env bash
# Prepare lic (and optional HTTP deps) for a parallel nightly tier job on Linux.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GROUP="${1:-}"
if [[ -z "$GROUP" ]]; then
  echo "usage: ci-setup-lic-nightly-linux.sh <tier-group>" >&2
  exit 2
fi

export LIC_ROOT="${LIC_ROOT:-$ROOT/lic}"
export LIS_ROOT="${LIS_ROOT:-$ROOT/lis}"

chmod +x "$ROOT/scripts/"*.sh "$LIC_ROOT/scripts/"*.sh 2>/dev/null || true

if [[ -x "$LIC_ROOT/scripts/ci-install-llvm.sh" ]]; then
  sudo LI_LLVM_MAJOR=22 bash "$LIC_ROOT/scripts/ci-install-llvm.sh"
fi

need_http=0
case "$GROUP" in
  tier5|tier5-exploits) need_http=1 ;;
esac

if [[ "$need_http" == "1" ]]; then
  export DEBIAN_FRONTEND=noninteractive
  need_apt=0
  for pkg in wrk nginx apache2 lighttpd nodejs; do
    dpkg -s "$pkg" >/dev/null 2>&1 || need_apt=1
  done
  if [[ "$need_apt" == "1" ]]; then
    sudo apt-get update -qq
    sudo apt-get install -y -qq build-essential g++-13 gcc-13 libstdc++-13-dev \
      wrk nginx apache2 lighttpd nodejs
  fi
  command -v bun >/dev/null 2>&1 || echo "note: bun optional for tier5 (skipped when missing)" >&2
fi

if [[ "${SKIP_BUILD:-0}" == "1" ]]; then
  if [[ ! -x "$LIC_ROOT/build/compiler/lic/lic" ]]; then
    echo "ci-setup-lic-nightly-linux: SKIP_BUILD=1 but lic missing (run prepare-lic-linux first)" >&2
    exit 1
  fi
  if [[ "$need_http" == "1" ]] && [[ ! -x "$LIC_ROOT/build/li-httpd" ]]; then
    echo "ci-setup-lic-nightly-linux: SKIP_BUILD=1 but li-httpd missing" >&2
    exit 1
  fi
  echo "ci-setup-lic-nightly-linux: reuse lic build ($GROUP)"
  exit 0
fi

if [[ "$need_http" == "1" ]]; then
  "$ROOT/scripts/setup-lic-for-bench.sh"
else
  export LLVM_DIR="${LLVM_DIR:-/usr/lib/llvm-22/lib/cmake/llvm}"
  export CXX=g++-13 CC=gcc-13 LI_REPO_ROOT="$LIC_ROOT"
  (cd "$LIC_ROOT" && ./scripts/build.sh)
fi

test -x "$LIC_ROOT/build/compiler/lic/lic"
if [[ "$need_http" == "1" ]]; then
  test -x "$LIC_ROOT/build/li-httpd"
fi
echo "ci-setup-lic-nightly-linux: OK ($GROUP)"
