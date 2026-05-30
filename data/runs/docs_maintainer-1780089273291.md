# docs_maintainer digest — 2026-05-29

**Run:** `docs_maintainer-1780089273291` · **Heap:** `coord_ecosystem` · **north_star_fit:** ecosystem / Doc-a

## Executive summary

- Preflight (`ecosystem-audit.json`): **`repos_without_live_docs: []`** — all eight package URLs registered in `LIVE_DOCS`; **`live_docs_down: 8`** (handbook paths 404 until **lic** Pages deploy).
- Pushed phase-plan cross-links (**02**, **03**, **07** honest-proof footers) to [lic#421](https://github.com/li-langverse/lic/pull/421) (CI green).
- Opened mirror handbook PRs: **lit#15**, **lis#16**, **li-net#13**, **li-httpd#15**, **li-std-core#9**, **li-std-math#10** (companion to existing **lip#27**, **li-demo#17**).
- Root site `https://li-langverse.github.io/li-language/` and **provability-gaps** return **200**; ecosystem package paths still **404** pre-merge.
- **Human merge** on **lic#421** unblocks Pages deploy and clears `live_docs_down` on next audit.
- Close superseded **lic#400** / **lic#392** after **#421** merges.
- Deferred: **roadmap** governance edits; **research-findings** `ci.yml` (ci_maintainer).

## Deliverable / findings

| Area | Finding | Action taken |
|------|---------|--------------|
| Missing `LIVE_DOCS` registration | None (audit count 0) | No benchmarks audit change |
| Broken handbook URLs | Content on **lic#421** branch, not deployed | Eight `docs/ecosystem/*.md` + mkdocs nav; mirror `docs/handbook.md` + README rows |
| Cross-links master plan ↔ provability-gaps | Phase 02/03/07 lacked footer | Added standard footer; 00–06 + benchmarks plan already linked |
| Mirror repo traceability | README lacked published handbook row | Six new PRs + lip/li-demo prior PRs |
| Overclaim guard | Unchanged | Handbook pages use **Partial** tables; provability-gaps URL on Pages (200) |

**HEAD evidence (2026-05-29):** `ecosystem/lip/` … `ecosystem/li-demo/` → **404**; `verification/provability-gaps/` → **200**.

## Recommended issues/PRs

| Title | Repo | Labels | Notes |
|-------|------|--------|-------|
| docs(ecosystem): live handbook pages for eight org packages | **lic** | `li-swarm`, `agent:docs_maintainer`, `docs` | [PR #421](https://github.com/li-langverse/lic/pull/421) — **merge-approved** after review |
| docs(lip): handbook link to li-language Pages | **lip** | `docs` | [PR #27](https://github.com/li-langverse/lip/pull/27) |
| docs(li-demo): handbook traceability row | **li-demo** | `docs` | [PR #17](https://github.com/li-langverse/li-demo/pull/17) — fix CI or replace |
| docs(lit): handbook link to li-language Pages | **lit** | `docs` | [PR #15](https://github.com/li-langverse/lit/pull/15) |
| docs(lis): handbook link to li-language Pages | **lis** | `docs` | [PR #16](https://github.com/li-langverse/lis/pull/16) |
| docs(li-net): handbook link to li-language Pages | **li-net** | `docs` | [PR #13](https://github.com/li-langverse/li-net/pull/13) |
| docs(li-httpd): handbook link to li-language Pages | **li-httpd** | `docs` | [PR #15](https://github.com/li-langverse/li-httpd/pull/15) |
| docs(li-std-core): handbook link to li-language Pages | **li-std-core** | `docs` | [PR #9](https://github.com/li-langverse/li-std-core/pull/9) |
| docs(li-std-math): handbook link to li-language Pages | **li-std-math** | `docs` | [PR #10](https://github.com/li-langverse/li-std-math/pull/10) |
| Deploy li-language Pages after lic merge | **li-language** | `ci`, `docs` | Clears `live_docs_down` |

## Deferred

- **roadmap** self-merge (human only).
- **lic#400**, **lic#392** close after **#421** lands.
- **li-demo#16** superseded by **#17** (agent-kit / smoke failures).
- MkDocs local build in runner (rely on lic CI).
- **research-findings** missing `ci.yml` on main — **ci_maintainer** P0.
