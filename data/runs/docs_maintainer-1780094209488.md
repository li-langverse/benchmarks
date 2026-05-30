# docs_maintainer digest — 2026-05-29

**Run:** `docs_maintainer-1780094209488` · **Source:** proactive ecosystem sweep · **north_star_fit:** ecosystem / Doc-a (easy pillar — honest handbook + proof cross-links)

## Executive summary

- Preflight `ecosystem-audit.json` (2026-05-29T22:25Z): **10 repos** in `repos_without_live_docs` (not yet registered in audit `LIVE_DOCS` on `main`); **`live_docs_down: []`** — registered handbook roots respond **200**.
- Package ecosystem paths still **404** on li-language Pages (`/ecosystem/lip/` etc.) until [lic#421](https://github.com/li-langverse/lic/pull/421) merges and **lic** Pages deploy on `main`.
- This run merged **lic#421** base and pushed incremental cross-links: governance, **lip** plan, **Vision-LLM** spec ↔ master plan ↔ provability-gaps; removed duplicate proof-db appendix.
- [lic#421](https://github.com/li-langverse/lic/pull/421) CI **green** (Linux/macOS/Windows) — ready for human merge-approved review.
- [benchmarks#146](https://github.com/li-langverse/benchmarks/pull/146) registers package handbook URLs in `LIVE_DOCS` — merge after Pages deploy clears 404s.
- Mirror README/handbook PRs (li-net#13, li-httpd#15, li-std-*#9–#10, lip/lit/lis docs PRs) remain ready but blocked on Pages deploy.
- Master plan open tracker: **5** rows (2i, 7d, 7e, 8p, Vision-LLM); **166** plan-audit findings — provability **Partial** only with evidence.
- **roadmap** Pages **404** — deferred to human governance / Pages setup (not agent self-merge).

## Deliverable / findings

| Area | Finding | Action taken |
|------|---------|--------------|
| `repos_without_live_docs` | 10 org repos absent from audit `LIVE_DOCS` on `main` | No audit-script change — [benchmarks#146](https://github.com/li-langverse/benchmarks/pull/146) queued; merge after Pages live |
| Broken handbook URLs | `/ecosystem/*` paths **404** on deployed Pages | Content on **lic#421**; root handbook **200** |
| Phase-plan ↔ provability-gaps | governance, lip, Vision-LLM lacked Doc-c headers | Added honest-proof footers + alignment rows in `provability-gaps.md` |
| Duplicate appendix | Two `Proof-db discrepancy appendix` blocks | Removed duplicate in “Still open” section |
| Agent deliverable | lic branch pushed | Updates **lic#421** stack via `chore/agent-docs_maintainer-1780094209488` |

**Evidence:** `curl -sI https://li-langverse.github.io/li-language/ecosystem/lip/` → **404**; `https://li-langverse.github.io/li-language/` → **200**.

## Recommended issues/PRs

| Title | Repo | Labels | Notes |
|-------|------|--------|-------|
| docs(ecosystem): live handbook pages for eight org packages | **lic** | `li-swarm`, `agent:docs_maintainer`, `docs` | [PR #421](https://github.com/li-langverse/lic/pull/421) — merge-approved after review |
| chore(audit): register package handbook URLs in LIVE_DOCS | **benchmarks** | `docs`, `li-swarm` | [PR #146](https://github.com/li-langverse/benchmarks/pull/146) — merge after Pages deploy |
| docs(li-net/li-httpd/li-std-*): handbook link | **li-net**, **li-httpd**, **li-std-*** | `docs` | Ready PRs — merge after Pages live |
| docs(lip/lit/lis): handbook link to li-language Pages | **lip**, **lit**, **lis** | `docs` | Rebase CI-red handbook PRs after #421 |
| docs(swarm): docs_maintainer digest 1780094209488 | **benchmarks** | `docs`, `li-swarm` | This digest |

## Deferred

- **roadmap** governance doc edits and GitHub Pages (human merge only; `/roadmap/` **404**).
- Mirror-repo `docs/handbook.md` batch from `lic/scripts/templates/package-mirror/docs/handbook.md.template`.
- MkDocs strict-mode remaining warnings (master-plan heading anchors — pre-existing).
- Org agent-kit drift (9 repos — `agent_kit_maintainer` lane).
- Tier-1 perf red rows — numerics/bench_improver lanes, not docs.
- **research-findings** missing `ci.yml` on `main` — `ci_maintainer` lane.
