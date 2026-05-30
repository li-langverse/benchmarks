# docs_maintainer digest — 2026-05-30

**Agent:** `docs_maintainer` · **Run:** `1780144600799` · **Heap:** `coord_ecosystem` (`repos_without_live_docs`: 1)  
**north_star_fit:** Easy pillar — live handbook hub for compiler monorepo; proof status unchanged (**G-*** not edited).

---

## Executive summary

- Preflight `ecosystem-audit.json` flagged **lic** in `repos_without_live_docs` and `live_docs_down` (HEAD 404 on https://li-langverse.github.io/lic/).
- Root cause: PR **#535** merged `pages.yml` but **omitted** `site/index.html`; **Handbook (Pages)** failed on `test -f site/index.html`.
- Shipped `site/index.html` hub (master plan, provability gaps, plan cross-links, satellite Pages table) on **lic#544**.
- Cross-links (`docs/handbook/README.md`, `docs/ecosystem/plan-cross-links.md`) already on `main` from #535; open **#533** is largely redundant.
- After **#544** merge + deploy, re-run `ecosystem-audit.py` — expect **lic** cleared from `repos_without_live_docs`.
- **lis** may remain 404 until its Pages PR merges — out of scope for this run.
- No **G-*** or roadmap self-merge; no GitHub Actions cron added.

---

## Deliverable / findings

| Item | Detail |
|------|--------|
| **Repo** | `li-langverse/lic` (isolated clone `docs_maintainer-1780144600799`) |
| **PR** | https://github.com/li-langverse/lic/pull/544 |
| **Files** | `site/index.html`, `CHANGELOG.md`, `docs/release-notes/2026-05-30-lic-handbook-pages.md` |
| **Pages workflow** | Run `26683179853` failed post-#535; fix unblocks deploy on next `main` push |
| **Audit probe** | `HANDBOOK_PAGES["lic"]` → `https://li-langverse.github.io/lic/` |

### Cross-links (already on main)

- [Master plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md) ↔ [provability-gaps](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) via [plan-cross-links](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/plan-cross-links.md)
- [Handbook index](https://github.com/li-langverse/lic/blob/main/docs/handbook/README.md) lists satellite package Pages

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| fix(docs): ship site/index.html for lic GitHub Pages | `lic` | `li-swarm`, `agent:docs_maintainer` — **#544** (open) |
| Close or supersede docs(lic): handbook index and plan cross-links | `lic` | — **#533** (duplicate of #535 content) |
| docs(lis): GitHub Pages handbook and plan cross-links | `lis` | `agent:docs_maintainer` — **#23** (CI fail; separate pass) |

---

## Deferred

- **li-language** / **lic-docs** mkdocs publish drift (nav tabs, search index) — `docs_ui_tester` / separate `lic-docs` work ([#403](https://github.com/li-langverse/lic/issues/403)).
- **lis** live Pages until failing handbook PRs land.
- Plan-completion debt (166 findings) — `plan_verifier` / `implementation_gaps`, not docs_maintainer.
- Red tier-1 benchmarks — `bench_improver` / `numerics_researcher`.
