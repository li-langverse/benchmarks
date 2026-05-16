#!/usr/bin/env bash
# Cursor sessionStart — remind agents of mandatory gates.
set -euo pipefail
cat <<'EOF'
Ecosystem-first: docs/ecosystem/tooling-catalog.md — use catalog scripts/skills before one-offs.
If blocked: python3 scripts/file-ecosystem-gap-issue.py (labels ecosystem-gap, plan-needed).
Read ../roadmap/docs/ecosystem/engineering-standards.md and vision-and-roadmap.md.
Strict gates: functionality, security, performance. std/** = 100% coverage; lip publish >= 80%.
Perf status: https://li-langverse.github.io/benchmarks/
PR-only: feature branch + PR; merge via merge-approved + pr-merge-gate when reviewed.
Release notes: CHANGELOG + docs/release-notes/ (skill write-li-release-notes) before every merge-worthy PR.
EOF
exit 0
