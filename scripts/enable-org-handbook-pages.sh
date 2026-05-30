#!/usr/bin/env bash
# Enable GitHub Actions Pages on org handbook repos (docs_maintainer).
# Content must already exist on main (site/index.html + pages.yml).
set -euo pipefail

REPOS=(
  lip lit lis li-net li-httpd li-std-core li-std-math li-demo
)

for repo in "${REPOS[@]}"; do
  echo "==> $repo"
  gh api -X POST "repos/li-langverse/${repo}/pages" -f build_type=workflow \
    2>/dev/null || echo "  (Pages may already be enabled)"
  gh api -X POST "repos/li-langverse/${repo}/actions/workflows/pages.yml/dispatches" \
    -f ref=main 2>/dev/null || echo "  (dispatch skipped — no pages.yml on main yet)"
done

echo ""
echo "When workflows finish, verify:"
for repo in "${REPOS[@]}"; do
  echo "  https://li-langverse.github.io/${repo}/"
done
