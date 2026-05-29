# docs_maintainer digest — 2026-05-29

**Run:** `docs_maintainer-1780092584906` · **Source:** proactive ecosystem sweep · **north_star_fit:** ecosystem / Doc-a (easy pillar — honest handbook + proof cross-links)

## Executive summary

- Preflight `ecosystem-audit.json` (2026-05-29T22:04Z): **`repos_without_live_docs: []`**; **`live_docs_down: 8`** package handbook paths still **404** until [lic#421](https://github.com/li-langverse/lic/pull/421) merges and **lic** Pages deploy on `main`.
- Root handbook (**200**): `li-language`, benchmarks dashboard (**200**), roadmap development overview (**200**).
- This run pushed **`a4630801`** on `chore/agent-docs_maintainer-live-ecosystem-docs`: phase-plan ↔ provability-gaps cross-links for **math-linalg**, **httpd**, **8p**, **Pkg**; extra **G-*** HTML anchors (`g-net`, `g-oop`, …).
- [lic PR #421](https://github.com/li-langverse/lic/pull/421) CI green on Linux/macOS; Windows job was in progress at sweep time — human merge when full gate passes.
- [benchmarks PR #146](https://github.com/li-langverse/benchmarks/pull/146) registers package handbook URLs in `LIVE_DOCS` — merge after lic Pages live so audit reflects deployed paths.
- Cross-links master plan ↔ provability-gaps: compiler phase plans 00–07 + benchmarks + OOP + math/httpd/8p/Pkg now link gap register; **G-*** status not inflated.
- Mirror README/handbook PRs (li-net#13, li-httpd#15, li-std-*#9–#10, lip/lit/lis docs PRs) remain blocked on Pages deploy.
- Deferred: batch `docs/handbook.md` from package-mirror template; roadmap governance edits (human merge only).

## Deliverable / findings

| Area | Finding | Action taken |
|------|---------|--------------|
| Missing `LIVE_DOCS` registration | Cleared on audit branch ([benchmarks#146](https://github.com/li-langverse/benchmarks/pull/146)) | No change this run — awaiting merge |
| Broken handbook URLs (404) | `/ecosystem/{lip,lit,lis,li-net,li-httpd,li-std-core,li-std-math,li-demo}/` on li-language Pages | Content on **lic#421**; HEAD verified **404** (2026-05-29) |
| Phase-plan ↔ provability-gaps | math-linalg, httpd, 8p, Pkg lacked Doc-c headers | Added honest-proof / Doc-c footers + alignment rows in `provability-gaps.md` |
| mkdocs strict anchors | `#g-net` etc. missing | Added explicit `<span id="g-*">` anchors |
| Agent deliverable | lic branch pushed | Commit `a4630801` → updates **lic#421** |

**Evidence:** `curl -sI https://li-langverse.github.io/li-language/ecosystem/lip/` → **404**; root handbook → **200**.

## Recommended issues/PRs

| Title | Repo | Labels | Notes |
|-------|------|--------|-------|
| docs(ecosystem): live handbook pages for eight org packages | **lic** | `li-swarm`, `agent:docs_maintainer`, `docs` | [PR #421](https://github.com/li-langverse/lic/pull/421) — includes `a4630801`; merge-approved after review |
| chore(audit): register package handbook URLs in LIVE_DOCS | **benchmarks** | `docs`, `li-swarm` | [PR #146](https://github.com/li-langverse/benchmarks/pull/146) — merge after Pages deploy |
| docs(li-net/li-httpd/li-std-*): handbook link | **li-net**, **li-httpd**, **li-std-*** | `docs` | Ready PRs — merge after Pages live |
| docs(lip/lit/lis): handbook link to li-language Pages | **lip**, **lit**, **lis** | `docs` | Rebase CI-red PRs after #421 |
| docs(swarm): docs_maintainer digest 1780092584906 | **benchmarks** | `docs`, `li-swarm` | This digest |

## Deferred

- **roadmap** governance doc edits (human merge only).
- Mirror-repo `docs/handbook.md` sweep from `lic/scripts/templates/package-mirror/docs/handbook.md.template`.
- MkDocs strict-mode remaining warnings (master-plan heading anchors — pre-existing).
- Org agent-kit drift (9 repos — `agent_kit_maintainer` lane).
- Tier-1 perf red rows — numerics/bench_improver lanes, not docs.
