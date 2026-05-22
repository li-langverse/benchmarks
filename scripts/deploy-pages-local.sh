#!/usr/bin/env bash
# Publish https://li-langverse.github.io/benchmarks/ from a local build (no GitHub Actions).
#
# One-time (or if Pages still says "GitHub Actions"): this script switches the repo to
# deploy from the gh-pages branch. PR CI can keep using pages.yml; production updates
# do not need workflow_dispatch.
#
# Usage:
#   ./scripts/deploy-pages-local.sh              # deploy existing dashboard/dist
#   ./scripts/deploy-pages-local.sh --build      # npm build + copy summary.json first
#   ./scripts/deploy-pages-local.sh --workflow   # trigger pages.yml instead (uses Actions)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_SLUG="${PAGES_REPO:-li-langverse/benchmarks}"
DIST="${ROOT}/dashboard/dist"
DO_BUILD=0
USE_WORKFLOW=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build) DO_BUILD=1 ;;
    --workflow) USE_WORKFLOW=1 ;;
    -h|--help)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
  shift
done

run_gh() {
  if [[ -n "${WITH_GITHUB_ENV:-}" && -x "$WITH_GITHUB_ENV" ]]; then
    "$WITH_GITHUB_ENV" gh "$@"
  else
    gh "$@"
  fi
}

find_with_github_env() {
  for d in "$ROOT/../lic" "$ROOT/../li"; do
    if [[ -x "$d/scripts/with-github-env.sh" ]]; then
      export WITH_GITHUB_ENV="$d/scripts/with-github-env.sh"
      return 0
    fi
  done
  return 1
}

if [[ "$USE_WORKFLOW" == "1" ]]; then
  find_with_github_env || true
  echo "==> trigger Deploy dashboard workflow (uses Actions)"
  run_gh workflow run pages.yml --repo "$REPO_SLUG"
  run_gh run list --repo "$REPO_SLUG" --workflow=pages.yml --limit 3
  echo "When green: https://li-langverse.github.io/benchmarks/"
  exit 0
fi

if [[ "$DO_BUILD" == "1" ]]; then
  echo "==> build Vite dashboard"
  if [[ ! -f "$ROOT/data/latest/summary.json" ]]; then
    echo "error: missing data/latest/summary.json — run ./scripts/ingest/ingest-lic.sh or ./scripts/run-full-benchmark-suite.sh" >&2
    exit 1
  fi
  cd "$ROOT/dashboard"
  npm ci
  npm run build
  mkdir -p dist/latest
  cp "$ROOT/data/latest/summary.json" dist/latest/
fi

if [[ ! -f "$DIST/index.html" ]]; then
  echo "error: $DIST/index.html missing — re-run with --build" >&2
  exit 1
fi
if [[ ! -f "$DIST/latest/summary.json" ]]; then
  echo "error: $DIST/latest/summary.json missing — run ingest then --build" >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "error: gh CLI required (or set GH_TOKEN and git push access to $REPO_SLUG)" >&2
  exit 1
fi
find_with_github_env || true
if [[ -z "${GH_TOKEN:-}" ]]; then
  run_gh auth status >/dev/null 2>&1 || {
    echo "error: gh not authenticated — use lic/scripts/with-github-env.sh or gh auth login" >&2
    exit 1
  }
fi

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT
cp -a "$DIST"/. "$WORKDIR"/
touch "$WORKDIR/.nojekyll"

echo "==> push gh-pages branch"
(
  cd "$WORKDIR"
  git init -q
  git config user.name "benchmarks-pages"
  git config user.email "benchmarks-pages@users.noreply.github.com"
  git add -A
  git commit -qm "chore: local Pages deploy $(date -u +%Y-%m-%dT%H:%MZ)"
  git branch -M gh-pages
  if [[ -n "${GH_TOKEN:-}" ]]; then
    git push -f "https://x-access-token:${GH_TOKEN}@github.com/${REPO_SLUG}.git" gh-pages
  else
    git remote add origin "https://github.com/${REPO_SLUG}.git"
    run_gh auth setup-git 2>/dev/null || true
    git push -f origin gh-pages
  fi
)

echo "==> ensure Pages source = gh-pages branch (not Actions workflow)"
run_gh api "repos/${REPO_SLUG}/pages" -X PUT \
  --input - <<'JSON' 2>/dev/null || echo "(Pages API: set branch gh-pages / root manually if this failed)"
{
  "build_type": "legacy",
  "source": { "branch": "gh-pages", "path": "/" }
}
JSON

echo ""
echo "Published (branch deploy, no Actions run): https://li-langverse.github.io/benchmarks/"
echo "Refresh data next time: ./scripts/run-full-benchmark-suite.sh && $0 --build"
