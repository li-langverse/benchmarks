#!/usr/bin/env bash
# Cloud Agent VM: fetch/pull org repos, build lic, install dashboard-next deps.
# Use as the Cursor Cloud "install / update" script:
#   bash /agent/repos/benchmarks/scripts/update-cloud-agent-env.sh
set -euo pipefail

AGENT_ROOT="${AGENT_ROOT:-/agent}"
REPOS_ROOT="${REPOS_ROOT:-$AGENT_ROOT/repos}"
SKIP_PULL="${SKIP_PULL:-0}"
SKIP_LIC_BUILD="${SKIP_LIC_BUILD:-0}"
SKIP_DASHBOARD="${SKIP_DASHBOARD:-0}"

log() { echo "==> $*"; }

pull_repos() {
  local repo dir
  for repo in benchmarks lic lip lit lis roadmap li-demo li-httpd li-language li-net li-std-core li-std-math; do
    dir="$REPOS_ROOT/$repo"
    [[ -d "$dir/.git" ]] || continue
    log "git fetch $repo"
    (
      cd "$dir"
      git fetch origin
      if git show-ref --verify --quiet refs/heads/main; then
        cur="$(git branch --show-current 2>/dev/null || true)"
        if [[ "$cur" != "main" ]]; then
          if ! git diff --quiet || ! git diff --cached --quiet; then
            log "WARN: $repo has local changes on $cur — skip checkout main"
          else
            git checkout main 2>/dev/null || true
            git pull --ff-only origin main 2>/dev/null || true
          fi
        else
          git pull --ff-only origin main 2>/dev/null || true
        fi
      fi
    )
  done
}

build_lic() {
  local lic="$REPOS_ROOT/lic"
  [[ -f "$lic/scripts/llvm-env.sh" ]] || {
    echo "missing $lic/scripts/llvm-env.sh" >&2
    return 1
  }
  # shellcheck source=/dev/null
  source "$lic/scripts/llvm-env.sh"
  if ! li_detect_llvm_dir; then
    log "LLVM not found — installing pinned LLVM (sudo)"
    if [[ -f "$lic/scripts/ci-install-llvm.sh" ]] && command -v sudo >/dev/null 2>&1; then
      sudo bash "$lic/scripts/ci-install-llvm.sh"
    fi
    li_detect_llvm_dir || {
      li_llvm_install_hint
      return 1
    }
  fi
  li_detect_compilers
  export CC CXX LLVM_DIR LI_LLVM_MAJOR
  log "build lic (LLVM_DIR=$LLVM_DIR CC=$CC)"
  (cd "$lic" && ./scripts/build.sh)
}

build_li_language_optional() {
  local ll="$REPOS_ROOT/li-language"
  [[ -d "$ll/.git" ]] || return 0
  if grep -q 'LLVM 18 required' "$ll/CMakeLists.txt" 2>/dev/null; then
    if [[ "${LI_LLVM_MAJOR:-22}" != "18" ]]; then
      log "skip li-language (pins LLVM 18; lic uses ${LI_LLVM_MAJOR:-22})"
      return 0
    fi
  fi
  # shellcheck source=/dev/null
  source "$REPOS_ROOT/lic/scripts/llvm-env.sh"
  li_detect_llvm_dir || return 0
  li_detect_compilers
  export CC CXX LLVM_DIR
  log "build li-language (optional mirror)"
  (
    cd "$ll"
    cmake -B build -G Ninja -DLLVM_DIR="$LLVM_DIR"
    cmake --build build -j "$(nproc)"
  ) || echo "WARN: li-language build failed (non-fatal)" >&2
}

dashboard_deps() {
  local bench="$REPOS_ROOT/benchmarks"
  local dash="$bench/dashboard-next"
  if [[ ! -f "$dash/package.json" ]]; then
    dash="$bench/dashboard"
  fi
  [[ -f "$dash/package.json" ]] || {
    echo "no dashboard-next or dashboard package.json under $bench" >&2
    return 1
  }
  log "npm ci ($dash)"
  (cd "$dash" && npm ci)
}

install_python_tools() {
  if command -v pip3 >/dev/null 2>&1; then
    pip3 install -q pytest
  elif command -v pip >/dev/null 2>&1; then
    pip install -q pytest
  else
    echo "WARN: pip not found — skip pytest" >&2
  fi
}

main() {
  [[ "$SKIP_PULL" == "1" ]] || pull_repos
  if [[ "$SKIP_LIC_BUILD" != "1" ]]; then
    build_lic
    build_li_language_optional
  fi
  [[ "$SKIP_DASHBOARD" == "1" ]] || dashboard_deps
  install_python_tools
  log "update-cloud-agent-env complete"
}

main "$@"
