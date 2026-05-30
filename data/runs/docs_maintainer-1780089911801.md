# docs_maintainer digest — 2026-05-29

**Run:** `docs_maintainer-1780089911801` · **Heap:** `coord_ecosystem:docs_maintainer:9d7cbf2140c1bb621962` · **north_star_fit:** ecosystem / Doc-a

## Executive summary

- Latest `ecosystem-audit.json` (2026-05-29T21:27Z): **`repos_without_live_docs: []`** — eight package handbook URLs registered in `LIVE_DOCS`; **`live_docs_down: 8`** (all return **404** until **lic** content merges and **li-language** Pages deploys).
- Primary deliverable remains **[lic PR #421](https://github.com/li-langverse/lic/pull/421)** (CI green): eight MkDocs handbook pages, `live-documentation.md`, `official-packages.md` handbook column, phase-plan ↔ provability-gaps headers, package-mirror `handbook.md.template`.
- This run pushed incremental honesty on **`overview.md`** (deploy-pending / `live_docs_down`) and **`provability-gaps.md`** (live-documentation alignment row) onto the same branch.
- Package mirror README/handbook PRs exist for lip, lit, lis, li-net, li-httpd, li-std-* (several CI-red on duplicate agent-kit stacks — merge **#421** first).
- Cross-links master plan ↔ provability-gaps: satisfied on branch via phase-plan headers + handbook pages; no **G-*** status inflated.
- **Human merge** required for **lic#421** and **li-language** Pages deploy — clears `live_docs_down` on next audit.
- Close **lic#400** as superseded by #421 branch content.
- Deferred: roadmap governance edits; batch mirror `docs/handbook.md` from template (six repos).

## Deliverable / findings

| Area | Finding | Action taken |
|------|---------|--------------|
| Missing `LIVE_DOCS` registration | Cleared (benchmarks `LIVE_DOCS` + PR #146) | No new audit keys this run |
| Broken handbook URLs (404) | Content on **lic#421** branch, not on Pages yet | HEAD verified 404 for all eight paths; deploy-pending note in `overview.md` |
| Cross-links master plan ↔ provability-gaps | Partial on `main`, complete on #421 | Branch has headers on phase plans 00–07 + benchmarks plan; gaps register links `live-documentation.md` |
| `official-packages.md` | Handbook column on #421 | Awaiting merge |
| Agent deliverable | lic PR open, CI pass | Incremental commit on `chore/agent-docs_maintainer-live-ecosystem-docs` |

**Evidence (HEAD, 2026-05-29):** `https://li-langverse.github.io/li-language/ecosystem/{lip,lit,lis,li-net,li-httpd,li-std-core,li-std-math,li-demo}/` → **404**.

## Recommended issues/PRs

| Title | Repo | Labels | Notes |
|-------|------|--------|-------|
| docs(ecosystem): live handbook pages for eight org packages | **lic** | `li-swarm`, `agent:docs_maintainer`, `docs` | [PR #421](https://github.com/li-langverse/lic/pull/421) — merge-approved after review |
| docs: live documentation map and phase-plan cross-links | **lic** | `docs` | [PR #400](https://github.com/li-langverse/lic/pull/400) — close as superseded by #421 |
| docs(lip): handbook link to li-language Pages | **lip** | `docs` | [PR #27](https://github.com/li-langverse/lip/pull/27) — CI fail; rebase after #421 |
| docs(lit/lis/…): handbook link to li-language Pages | **lit**, **lis**, **li-net**, **li-httpd**, **li-std-*** | `docs` | Ready PRs #15–#16, #13, etc. — merge after Pages live |
| Deploy li-language Pages after lic merge | **li-language** | `ci`, `docs` | Clears `live_docs_down` |
| docs(swarm): docs_maintainer digest 1780089911801 | **benchmarks** | `docs`, `li-swarm` | This digest |

## Deferred

- **roadmap** governance doc edits (human merge only).
- Mirror-repo `docs/handbook.md` sweep from `lic/scripts/templates/package-mirror/docs/handbook.md.template` (batch after Pages deploy).
- **li-demo#16** / **#17** — failed CI; replace with handbook-link PR after #421.
- MkDocs local build in runner (rely on lic CI).
- **research-findings** missing `ci.yml` (ci_maintainer scope).
