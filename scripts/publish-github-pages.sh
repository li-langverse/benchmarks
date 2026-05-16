#!/usr/bin/env bash
# Publish benchmarks repo to GitHub and enable Pages (requires repo to exist + push access).
set -euo pipefail
BENCH_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LI_ROOT="$(cd "$BENCH_ROOT/../li" && pwd)"
WRAPPER="${LI_ROOT}/scripts/with-github-env.sh"

if [[ ! -x "$WRAPPER" ]]; then
  echo "error: missing $WRAPPER" >&2
  exit 1
fi

echo "==> build dashboard"
cd "$BENCH_ROOT/dashboard"
npm ci
npm run build
mkdir -p dist/latest
cp "$BENCH_ROOT/data/latest/summary.json" dist/latest/

echo "==> ensure remote"
cd "$BENCH_ROOT"
if ! git remote get-url origin &>/dev/null; then
  git remote add origin https://github.com/li-langverse/benchmarks.git
fi

"$WRAPPER" gh auth setup-git 2>/dev/null || true

if ! "$WRAPPER" gh repo view li-langverse/benchmarks &>/dev/null; then
  echo ""
  echo "ACTION NEEDED: Create empty repo https://github.com/organizations/li-langverse/repositories/new"
  echo "  Name: benchmarks"
  echo "  Public, no README/license (we push existing tree)"
  echo "Then re-run: $0"
  exit 1
fi

echo "==> push main"
"$WRAPPER" git push -u origin main

echo "==> enable GitHub Pages (workflow)"
"$WRAPPER" gh api repos/li-langverse/benchmarks/pages \
  -X POST \
  -f build_type=workflow \
  2>/dev/null || echo "(pages may already be enabled)"

echo "==> run Deploy dashboard workflow"
"$WRAPPER" gh workflow run pages.yml --repo li-langverse/benchmarks
"$WRAPPER" gh run list --repo li-langverse/benchmarks --workflow=pages.yml --limit 3

echo ""
echo "When CI finishes: https://li-langverse.github.io/benchmarks/"
