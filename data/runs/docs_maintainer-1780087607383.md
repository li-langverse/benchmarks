# docs_maintainer digest — 2026-05-29

**Run:** `docs_maintainer-1780087607383` · **Heap:** `coord_ecosystem` · **north_star_fit:** ecosystem / Doc-a

## Executive summary

- Preflight audit: **`repos_without_live_docs: []`** (URLs registered in `benchmarks/scripts/ecosystem-audit.py` `LIVE_DOCS`); **`live_docs_down: 8`** — all package handbook URLs return **404** until **lic** → **li-language** Pages deploy.
- Implemented eight MkDocs handbook pages (lip, lit, lis, li-net, li-httpd, li-std-core, li-std-math, li-demo) with honest **Partial** status and master-plan ↔ provability-gaps cross-links on branch `chore/agent-docs_maintainer-live-ecosystem-docs`.
- Merged **PR #400** live-documentation map, phase-plan footer cross-links, and package-mirror `handbook.md.template` into the same branch (supersedes overlapping PR #400 content).
- Open **lic PR #421** updated with merge commit; CI was green before this push — re-run expected.
- Package repos **lip** and **li-demo** README/handbook now point at published handbook URLs (deploy-pending note).
- **Human merge required** for lic PR; Pages deploy clears `live_docs_down` on next audit.
- Close stale **li-demo#16** (LLVM 22 CI failure + placeholder smoke text) in favor of new handbook-link PR.
- Deferred: mirror README updates for lit, lis, li-net, li-httpd, li-std-* (template in lic); roadmap self-merge.

## Deliverable / findings

| Area | Finding | Action taken |
|------|---------|--------------|
| Missing live docs registration | Resolved in benchmarks `LIVE_DOCS` (PR #146 merged / ready) | No new audit registration needed |
| Broken handbook URLs (404) | Content not yet on **li-language** Pages | Eight `docs/ecosystem/*.md` pages + mkdocs nav; awaiting merge + deploy |
| Cross-links master plan ↔ provability-gaps | Partial in main | Handbook pages link both; phase plans 00–06 + benchmarks plan footers added; `live-documentation.md` index |
| `official-packages.md` | Missing handbook column on main | Handbook column + `PKG-lis` row + live-documentation link |
| Package mirror in-repo docs | Stale “until Pages exists” wording | `handbook.md.template`; lip/li-demo updated |

**Evidence (HEAD checks, 2026-05-29):** all eight `https://li-langverse.github.io/li-language/ecosystem/{lip,lit,lis,li-net,li-httpd,li-std-core,li-std-math,li-demo}/` → **404**.

## Recommended issues/PRs

| Title | Repo | Labels | Notes |
|-------|------|--------|-------|
| docs(ecosystem): live handbook pages for eight org packages | **lic** | `li-swarm`, `agent:docs_maintainer`, `docs` | [PR #421](https://github.com/li-langverse/lic/pull/421) — **merge-approved** after review |
| docs: live documentation map and phase-plan cross-links | **lic** | `docs` | [PR #400](https://github.com/li-langverse/lic/pull/400) — **close as superseded** by #421 branch |
| docs(lip): handbook link to li-language Pages | **lip** | `li-swarm`, `agent:docs_maintainer`, `docs` | New branch `chore/agent-docs_maintainer-handbook-link` |
| docs(li-demo): handbook traceability row | **li-demo** | `li-swarm`, `agent:docs_maintainer`, `docs` | Replaces failed #16 |
| chore(docs): mirror handbook links (lit, lis, li-net, …) | **lit**, **lis**, **li-net**, **li-httpd**, **li-std-core**, **li-std-math** | `docs` | Apply `lic/scripts/templates/package-mirror/docs/handbook.md.template` |
| Deploy li-language Pages after lic merge | **li-language** | `ci`, `docs` | Clears `live_docs_down` in ecosystem audit |

## Deferred

- **roadmap** governance doc edits (human merge only).
- Full mirror-repo README sweep (six repos) — template committed in lic; batch follow-up PRs.
- **li-demo#16** close/revert (bad agent smoke + LLVM 22 CI on PR branch).
- MkDocs local build verification (mkdocs not installed in runner env; CI on lic PR is the gate).
- **research-findings** missing `ci.yml` on main (P0 ci_maintainer, not docs scope).
