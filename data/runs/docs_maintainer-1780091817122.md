# docs_maintainer digest — 2026-05-29

**Run:** `docs_maintainer-1780091817122` · **Heap:** `coord_ecosystem:docs_maintainer:9d7cbf2140c1bb621962` · **north_star_fit:** ecosystem / Doc-a (easy pillar — honest handbook paths)

## Executive summary

- Latest `ecosystem-audit.json` (2026-05-29T21:58Z): **`repos_without_live_docs: []`** — all eight package handbook URLs are registered in `LIVE_DOCS`.
- **`live_docs_down: 8`** — lip, lit, lis, li-net, li-httpd, li-std-core, li-std-math, li-demo handbook paths still return **404** until **lic#421** merges and **lic** [docs CI](https://github.com/li-langverse/lic/blob/main/.github/workflows/docs.yml) deploys to the legacy `li-language` Pages URL.
- Primary deliverable remains **[lic PR #421](https://github.com/li-langverse/lic/pull/421)** (eight MkDocs handbook pages, `live-documentation.md`, `official-packages.md`, phase-plan ↔ provability-gaps headers).
- This run pushed **`fb0f04ad`** on branch `chore/agent-docs_maintainer-live-ecosystem-docs`: corrects handbook **source = lic** (not archived `li-language`); adds explicit **G-*** HTML anchors for phase-plan Doc-c cross-links.
- Cross-links master plan ↔ provability-gaps: phase plans 00–07 + benchmarks plan link to gaps register; **G-*** status not inflated (Partial/Missing only with evidence).
- Ready mirror README/handbook PRs exist (li-net#13, li-httpd#15, li-std-*#9–#10) — merge after Pages deploy clears audit.
- **Human merge** required for **lic#421** — no self-merge on roadmap; no GitHub Actions cron added.
- Deferred: batch `docs/handbook.md` from package-mirror template; fix CI-red duplicate agent-kit PR stacks on lip/lit/lis.

## Deliverable / findings

| Area | Finding | Action taken |
|------|---------|--------------|
| Missing `LIVE_DOCS` registration | Cleared (`repos_without_live_docs: []`) | No new audit keys |
| Broken handbook URLs (404) | Content on **lic#421** branch; Pages not deployed | HEAD verified 404 for all eight `/ecosystem/<pkg>/` paths |
| Handbook source confusion | Docs said `li-language` repo; it is **archived** | Updated `live-documentation.md`, `overview.md`, `provability-gaps.md` alignment table |
| Phase-plan ↔ provability-gaps anchors | Strict mkdocs flagged `#g-vc` etc. missing | Added explicit `<span id="g-*">` anchors in `provability-gaps.md` |
| `official-packages.md` | Handbook column on #421 branch | Awaiting merge |
| Agent deliverable | lic branch pushed | Commit `fb0f04ad` on `chore/agent-docs_maintainer-live-ecosystem-docs` |

**Evidence (HEAD, 2026-05-29):** `https://li-langverse.github.io/li-language/ecosystem/{lip,lit,lis,li-net,li-httpd,li-std-core,li-std-math,li-demo}/` → **404**. Root handbook **200**.

## Recommended issues/PRs

| Title | Repo | Labels | Notes |
|-------|------|--------|-------|
| docs(ecosystem): live handbook pages for eight org packages | **lic** | `li-swarm`, `agent:docs_maintainer`, `docs` | [PR #421](https://github.com/li-langverse/lic/pull/421) — merge-approved after review; includes this run's commit |
| docs: live documentation map and phase-plan cross-links | **lic** | `docs` | [PR #400](https://github.com/li-langverse/lic/pull/400) — close as superseded by #421 |
| docs(lip/lit/lis): handbook link to li-language Pages | **lip**, **lit**, **lis** | `docs` | PRs #27, #15, #16 — CI fail; rebase after #421 |
| docs(li-net/li-httpd/li-std-*): handbook link | **li-net**, **li-httpd**, **li-std-*** | `docs` | Ready PRs #13–#15, #9–#10 — merge after Pages live |
| docs(li-demo): handbook traceability | **li-demo** | `docs` | Replace failed #16/#17 after #421 |
| docs(swarm): docs_maintainer digest 1780091817122 | **benchmarks** | `docs`, `li-swarm` | This digest |

## Deferred

- **roadmap** governance doc edits (human merge only).
- Mirror-repo `docs/handbook.md` sweep from `lic/scripts/templates/package-mirror/docs/handbook.md.template` (batch after Pages deploy).
- MkDocs strict-mode remaining warnings (master-plan heading anchors — pre-existing, not blocking CI).
- **research-findings** / org agent-kit drift (other agent lanes).
