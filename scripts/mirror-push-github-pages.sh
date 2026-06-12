#!/usr/bin/env bash
# Push GitLab main to GitHub mirror and trigger Deploy dashboard (Pages) workflow.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TOKEN="${GITHUB_MIRROR_TOKEN:-${GH_TOKEN:-${GITHUB_TOKEN:-}}}"
GITHUB_REPO="${GITHUB_MIRROR_REPO:-li-langverse/benchmarks}"
GITHUB_REF="${GITHUB_MIRROR_REF:-main}"

if [[ -z "$TOKEN" ]]; then
  echo "mirror-push-github-pages: skip (set GITHUB_MIRROR_TOKEN or GH_TOKEN to refresh benchmarks.lilangverse.xyz)"
  exit 0
fi

echo "==> push ${GITHUB_REF} to github.com/${GITHUB_REPO}"
git push "https://x-access-token:${TOKEN}@github.com/${GITHUB_REPO}.git" "HEAD:${GITHUB_REF}"

echo "==> dispatch pages.yml on ${GITHUB_REPO}"
http_code="$(curl -sS -o /tmp/gh-dispatch.json -w "%{http_code}" \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${TOKEN}" \
  "https://api.github.com/repos/${GITHUB_REPO}/actions/workflows/pages.yml/dispatches" \
  -d "{\"ref\":\"${GITHUB_REF}\"}")"
if [[ "$http_code" != "204" ]]; then
  echo "mirror-push-github-pages: dispatch HTTP ${http_code}" >&2
  cat /tmp/gh-dispatch.json >&2 || true
  exit 1
fi

echo "mirror-push-github-pages: OK — GitHub Pages deploy triggered for ${GITHUB_REF}"
