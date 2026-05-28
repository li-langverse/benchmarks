#!/usr/bin/env bash
# Cloud Agent VM: fetch/pull all li-langverse org repos, build lic (LLVM 22), dashboard-next.
# Use as the Cursor Cloud "install / update" script:
#   bash /agent/repos/benchmarks/scripts/cloud-agent-install.sh
set -euo pipefail

AGENT_ROOT="${AGENT_ROOT:-/agent}"
REPOS_ROOT="${REPOS_ROOT:-$AGENT_ROOT/repos}"
ORG="${LI_ORG:-li-langverse}"
# Pinned to lic CI / master plan (sole LLVM backend).
export LI_LLVM_MAJOR="${LI_LLVM_MAJOR:-22}"

SKIP_PULL="${SKIP_PULL:-0}"
SKIP_LIC_BUILD="${SKIP_LIC_BUILD:-0}"
SKIP_DASHBOARD="${SKIP_DASHBOARD:-0}"
# Clone org repos listed on GitHub but missing under REPOS_ROOT (off by default).
CLONE_MISSING="${CLONE_MISSING:-0}"

log() { echo "==> $*"; }

# Union: GitHub org repos (non-archived, limit 100) + any git checkout under REPOS_ROOT.
list_org_repo_names() {
  python3 - "$REPOS_ROOT" "$ORG" <<'PY'
import json
import subprocess
import sys
from pathlib import Path

repos_root = Path(sys.argv[1])
org = sys.argv[2]
names: set[str] = set()

if repos_root.is_dir():
    for child in sorted(repos_root.iterdir()):
        if child.is_dir() and (child / ".git").is_dir():
            names.add(child.name)

proc = subprocess.run(
    ["gh", "repo", "list", org, "--limit", "100", "--json", "name,isArchived"],
    capture_output=True,
    text=True,
    check=False,
)
if proc.returncode == 0 and proc.stdout.strip():
    for row in json.loads(proc.stdout):
        if not row.get("isArchived"):
            names.add(row["name"])
elif proc.returncode != 0:
    print(
        f"WARN: gh repo list failed ({proc.returncode}) — using {len(names)} local checkouts only",
        file=sys.stderr,
    )

for name in sorted(names):
    print(name)
PY
}

default_branch_for() {
  local repo="$1"
  local dir="$REPOS_ROOT/$repo"
  if [[ -d "$dir/.git" ]]; then
  (
    cd "$dir"
    if git show-ref --verify --quiet refs/remotes/origin/main 2>/dev/null; then
      echo main
      exit 0
    fi
    if git show-ref --verify --quiet refs/remotes/origin/master 2>/dev/null; then
      echo master
      exit 0
    fi
    git remote show origin 2>/dev/null | awk '/HEAD branch/ {print $NF; exit}'
  )
  else
    echo main
  fi
}

pull_one_repo() {
  local repo="$1"
  local dir="$REPOS_ROOT/$repo"

  if [[ ! -d "$dir/.git" ]]; then
    if [[ "$CLONE_MISSING" == "1" ]] && command -v gh >/dev/null 2>&1; then
      log "clone $repo"
      mkdir -p "$REPOS_ROOT"
      gh repo clone "$ORG/$repo" "$dir" -- --depth 1 || {
        echo "WARN: clone failed for $repo" >&2
        return 0
      }
    else
      return 0
    fi
  fi

  local base
  base="$(default_branch_for "$repo")"
  base="${base:-main}"

  log "git fetch $repo (base=$base)"
  (
    cd "$dir"
    git fetch origin
    cur="$(git branch --show-current 2>/dev/null || true)"
    if [[ "$cur" != "$base" ]]; then
      if ! git diff --quiet || ! git diff --cached --quiet; then
        log "WARN: $repo has local changes on $cur — skip checkout $base"
      else
        git checkout "$base" 2>/dev/null || true
        git pull --ff-only "origin" "$base" 2>/dev/null || true
      fi
    else
      git pull --ff-only "origin" "$base" 2>/dev/null || true
    fi
  )
}

pull_repos() {
  local repos=()
  local repo
  mapfile -t repos < <(list_org_repo_names)
  log "pull ${#repos[@]} org repos under $REPOS_ROOT"
  for repo in "${repos[@]}"; do
    [[ -n "$repo" ]] || continue
    pull_one_repo "$repo"
  done
}

bootstrap_lic() {
  local lic="$REPOS_ROOT/lic"
  local bootstrap="$lic/scripts/cloud-vm-bootstrap.sh"
  [[ -f "$bootstrap" ]] || {
    echo "missing $bootstrap — run from a synced lic checkout" >&2
    return 1
  }
  export LIC_ROOT="$lic" BENCHMARKS_ROOT="$REPOS_ROOT/benchmarks"
  LI_CLOUD_SKIP_BENCHMARKS=1 LI_CLOUD_SKIP_PYTEST=1 \
    LI_CLOUD_SKIP_BUILD="$([[ "$SKIP_LIC_BUILD" == "1" ]] && echo 1 || echo 0)" \
    bash "$bootstrap"
}

build_li_language_optional() {
  local ll="$REPOS_ROOT/li-language"
  [[ -d "$ll/.git" ]] || return 0
  if grep -q 'LLVM 18 required' "$ll/CMakeLists.txt" 2>/dev/null; then
    if [[ "${LI_LLVM_MAJOR}" != "18" ]]; then
      log "skip li-language (pins LLVM 18; org uses LLVM ${LI_LLVM_MAJOR})"
      return 0
    fi
  fi
  local lic="$REPOS_ROOT/lic"
  # shellcheck source=/dev/null
  source "$lic/scripts/llvm-env.sh"
  li_detect_llvm_dir || return 0
  li_detect_compilers
  export CC CXX LLVM_DIR
  log "build li-language (optional mirror)"
  (
    cd "$ll"
    cmake -B build -G Ninja "-DLLVM_DIR=${LLVM_DIR}"
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
  if ! command -v npm >/dev/null 2>&1; then
    echo "WARN: npm not found — skip dashboard" >&2
    return 0
  fi
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
  bootstrap_lic
  build_li_language_optional
  [[ "$SKIP_DASHBOARD" == "1" ]] || dashboard_deps
  install_python_tools
  log "update-cloud-agent-env complete (LLVM ${LI_LLVM_MAJOR}, org=${ORG})"
  log "Cloud install script: bash $REPOS_ROOT/benchmarks/scripts/cloud-agent-install.sh"
}

main "$@"
