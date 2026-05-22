#!/usr/bin/env bash
# Publish benchmarks repo to GitHub and enable Pages (requires repo to exist + push access).
set -euo pipefail
BENCH_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WRAPPER=""
for d in "$BENCH_ROOT/../lic" "$BENCH_ROOT/../li"; do
  if [[ -x "$d/scripts/with-github-env.sh" ]]; then
    WRAPPER="$d/scripts/with-github-env.sh"
    break
  fi
done
if [[ -z "$WRAPPER" ]]; then
  echo "error: missing lic/scripts/with-github-env.sh (set GH_TOKEN + gh auth)" >&2
  exit 1
fi
export WITH_GITHUB_ENV="$WRAPPER"

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

echo "==> deploy Pages (local build — no Actions)"
"$BENCH_ROOT/scripts/deploy-pages-local.sh" --build

echo ""
echo "Live: https://li-langverse.github.io/benchmarks/"
echo "To use Actions instead: ./scripts/deploy-pages-local.sh --workflow"
