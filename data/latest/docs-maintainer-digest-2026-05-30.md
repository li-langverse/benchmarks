# Docs maintainer digest — 2026-05-30

## Executive summary

- Preflight: **10** repos in `repos_without_live_docs`; **`live_docs_down`** empty (benchmarks + li-language OK).
- Updated **ecosystem-audit** to HEAD-check canonical handbook URLs; **lic** maps to **li-language** Pages (no duplicate `/lic/` site).
- Bootstrapped minimal **GitHub Pages** (`site/index.html` + `pages.yml`) for **lip**, **lit**, **lis**, and five package mirrors.
- **roadmap**: static `site/index.html` redirect to development-overview (fixes `/roadmap/` 404).
- **lic**: in-repo `docs/handbook/README.md` with master plan ↔ provability-gaps ↔ benchmarks cross-links.
- GraphQL rate limit blocked `agent-repo-workflow.sh prepare`; changes committed from sibling clones.
- Pages URLs return **404 until** each repo merges to `main` and org enables Actions Pages.
- Post-merge: re-run `python3 scripts/ecosystem-audit.py` to verify shrinking `repos_without_live_docs`.

## Deliverable / findings

| Repo | Change | Live URL (after deploy) |
|------|--------|-------------------------|
| benchmarks | Audit + bootstrap script + templates + this digest | https://li-langverse.github.io/benchmarks/ |
| lic | `docs/handbook/README.md`, README link | https://li-langverse.github.io/li-language/ |
| roadmap | `site/index.html`, workflow verify | https://li-langverse.github.io/roadmap/development-overview/ |
| lip | Pages scaffold, README, CHANGELOG | https://li-langverse.github.io/lip/ |
| lit | Pages scaffold, README | https://li-langverse.github.io/lit/ |
| lis | Pages + `docs/handbook.md` | https://li-langverse.github.io/lis/ |
| li-net, li-httpd, li-std-core, li-std-math, li-demo | handbook + Pages | `https://li-langverse.github.io/<repo>/` |

**Cross-links:** Existing [plan-cross-links.md](../../docs/ecosystem/plan-cross-links.md) in benchmarks; lic handbook links master plan, provability-gaps, roadmap vision, benchmarks dashboard.

**Honesty:** Static landing pages state bench ≠ proof; no **G-*** status changes in this pass.

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| docs: minimal GitHub Pages handbook + plan cross-links | lip | `li-swarm`, `agent:docs_maintainer`, `documentation` |
| docs: lit handbook Pages landing | lit | same |
| docs: lis handbook + Pages | lis | same |
| docs: package mirror handbook Pages | li-net, li-httpd, li-std-core, li-std-math, li-demo | same |
| docs: roadmap site root redirect | roadmap | `documentation` (human merge) |
| docs: lic in-repo handbook index | lic | same |
| chore(docs): ecosystem audit HEAD-check live handbook URLs | benchmarks | same |

## Deferred

- Enable GitHub Pages (Actions) per repo after merge — org admin step.
- Full mkdocs handbooks for lip/lis (beyond static landing).
- Update `roadmap/docs/development-overview.md` live-docs table after deploy (separate maintainer pass).
- `agent-repo-workflow.sh prepare` when GraphQL quota resets.

## Error

- `agent-repo-workflow.sh prepare --repo lip`: `GraphQL: API rate limit already exceeded` — used sibling clones instead.
