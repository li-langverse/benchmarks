# Docs maintainer digest — 2026-05-30

**Agent:** `docs_maintainer` · **Heap:** `coord_ecosystem` · **Run:** `1780109879421`  
**Preflight:** `data/latest/ecosystem-audit.json` (2026-05-30T02:59Z), `data/latest/agent-briefing.json`  
**Vision:** [org roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md) · proof → easy → fast  
**north_star_fit:** Ecosystem docs · PH-Pkg governance · Doc-a … Doc-e (provability honesty)

---

## Executive summary

- **10 repos** flagged `repos_without_live_docs` in ecosystem-audit (hardcoded org package list); **`live_docs_down`** is empty for canonical URLs (`benchmarks`, `li-language`).
- **Satellite handbook PRs** exist and CI-green on several repos (`li-httpd#16`, `li-net#14`, `li-std-core#10`, `li-std-math#11`, `roadmap#39`); audit count drops only after **merge + Pages deploy** on `main`.
- **`li-demo#18`** and **`lip#31` / `lit#17`** handbook PRs fail on **package CI**, not Pages workflow — needs `ci_maintainer` / agent-kit fix before merge.
- **lic** primary handbook uses mkdocs → `li-language` Pages; stale live site tracked in [#403](https://github.com/li-langverse/lic/issues/403) (strict build); this pass adds **plan cross-links** in-tree.
- Delivered **lic PR**: `docs/ecosystem/plan-cross-links.md`, master plan ↔ provability-gaps wiring, deduped provability-gaps appendix.
- Cross-link priority satisfied for **master plan ↔ provability-gaps ↔ phase plans** via new Ecosystem nav page.
- Human merge required for **roadmap** and all open handbook PRs — agents do not self-merge.

## Deliverable / findings

### Preflight (`ecosystem-audit.json`)

| Metric | Value |
|--------|-------|
| `repos_without_live_docs` | 10: `lic`, `lip`, `lit`, `lis`, `roadmap`, `li-demo`, `li-httpd`, `li-net`, `li-std-core`, `li-std-math` |
| `live_docs_down` | `[]` |
| Ready handbook-related PRs | `li-httpd#16`, `li-net#14`, `li-std-core#10`, `li-std-math#11`, `roadmap#39`, `benchmarks#178` |
| Failing handbook PRs | `li-demo#18`, `lip#31`, `lit#17`, `lip#27`, `lis#16`, `lit#15` |

### Implemented this run (`lic`)

| File | Change |
|------|--------|
| `docs/ecosystem/plan-cross-links.md` | Master plan ↔ **G-*** ↔ phase plan index + satellite Pages note |
| `docs/verification/provability-gaps.md` | Link to plan cross-links; remove duplicate Proof-db appendix |
| `docs/superpowers/plans/2026-05-14-li-master-plan.md` | Doc § links plan cross-links |
| `mkdocs.yml` / `docs/index.md` | Ecosystem nav + home doc map |
| `docs/release-notes/2026-05-30-plan-cross-links.md` | Release note |

### Satellite repo status (no new code this run)

| Repo | Handbook artifact on branch | Blocker |
|------|----------------------------|---------|
| `lip` | `site/index.html`, `pages.yml`, `docs/handbook.md` | PR CI red (`lip#31`) |
| `lit` | same pattern | PR CI red (`lit#17`) |
| `lis` | same pattern | PR CI red (`lis#16`) |
| `li-demo` | same pattern | Package CI red (`li-demo#18`) |
| `li-httpd`, `li-net`, `li-std-*` | Ready PRs | Await human merge + Pages enable |
| `roadmap` | `pages.yml` + dev overview | Ready `roadmap#39` — human merge |

### Cross-links audit

| Link | Status |
|------|--------|
| Master plan → provability-gaps | ✅ Existing Doc § + enhanced |
| Provability-gaps → phase plans | ✅ Via plan-cross-links + closing-gaps list |
| Phase plans → G-* IDs | ✅ plan-cross-links table |
| Satellite handbooks → lic register | ✅ Template in `lip/site/index.html` (pending deploy) |

## Recommended issues/PRs

| Priority | Title | Repo | Labels |
|----------|-------|------|--------|
| P0 | Merge ready handbook Pages PRs after review | `li-httpd`, `li-net`, `li-std-core`, `li-std-math`, `roadmap` | `surface:docs`, `merge-approved` |
| P0 | Fix package CI on handbook PRs | `li-demo`, `lip`, `lit`, `lis` | `li-swarm`, `agent:ci_maintainer` |
| P0 | [existing] Docs strict build — stale li-language Pages | `lic` | `#403`, `surface:docs` |
| P1 | docs(lic): plan cross-links in mkdocs Ecosystem nav | `lic` | **this run PR** |
| P1 | ecosystem-audit: treat deployed Pages as live for satellite repos | `benchmarks` | `surface:docs` |
| P2 | docs(IA): Game dev vs Language handbook | `lic` | `#422` |

## Deferred

- Enabling GitHub Pages org-wide (human/org setting per repo).
- Fixing `ecosystem-audit.py` hardcoded `missing_docs` list vs HEAD checks on `https://li-langverse.github.io/<repo>/`.
- Full mkdocs mirror of roadmap policy pages (ux-audit P1).
- `lic` strict link-warning burn-down ([#403](https://github.com/li-langverse/lic/issues/403)) — blocks fresh li-language deploy, separate from satellite handbooks.

Swarm run id: `1780109879421` · Agent id: `docs_maintainer`
