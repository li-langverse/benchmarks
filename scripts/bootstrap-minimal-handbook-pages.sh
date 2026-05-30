#!/usr/bin/env bash
# Copy minimal handbook Pages scaffold into a sibling org repo (docs_maintainer).
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <repo-dir> <title> [extra-html-paragraph]" >&2
  exit 1
fi

REPO_DIR="$1"
TITLE="$2"
EXTRA="${3:-}"
REPO_NAME="$(basename "$REPO_DIR")"
PAGES_URL="https://li-langverse.github.io/${REPO_NAME}/"
TEMPLATE_ROOT="$(cd "$(dirname "$0")" && pwd)/templates/minimal-handbook-pages"

mkdir -p "${REPO_DIR}/site" "${REPO_DIR}/.github/workflows" "${REPO_DIR}/docs/release-notes"
cp "${TEMPLATE_ROOT}/pages.yml" "${REPO_DIR}/.github/workflows/pages.yml"

cat >"${REPO_DIR}/site/index.html" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${TITLE}</title>
  <link rel="canonical" href="${PAGES_URL}">
  <style>
    :root { color-scheme: light dark; }
    body { font-family: system-ui, sans-serif; max-width: 52rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }
    a { color: #0969da; }
    nav { display: flex; flex-wrap: wrap; gap: 0.75rem 1.25rem; margin: 1rem 0; }
  </style>
</head>
<body>
  <h1>${TITLE}</h1>
  ${EXTRA}
  <nav aria-label="Handbook">
    <a href="https://github.com/li-langverse/${REPO_NAME}/blob/main/docs/handbook.md">In-repo handbook</a>
    <a href="https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md">Master plan</a>
    <a href="https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md">Provability gaps (G-*)</a>
    <a href="https://li-langverse.github.io/benchmarks/">Benchmarks dashboard</a>
    <a href="https://li-langverse.github.io/li-language/">Language handbook</a>
    <a href="https://li-langverse.github.io/roadmap/development-overview/">Development overview</a>
  </nav>
  <p><small>Benchmark rows are measurements, not proof certificates. Mark <strong>G-*</strong> Partial/Done only with cited evidence.</small></p>
</body>
</html>
EOF

if [[ ! -f "${REPO_DIR}/docs/release-notes/README.md" ]]; then
  cat >"${REPO_DIR}/docs/release-notes/README.md" <<'EOF'
# Release notes

Per-merge notes for user-facing changes. Policy: [roadmap release-notes](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/release-notes.md).
EOF
fi

echo "bootstrapped Pages scaffold in ${REPO_DIR}"
