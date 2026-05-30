# Docs maintainer digest — 2026-05-30 (run 1780177405649)

**Agent:** `docs_maintainer` · **Heap:** `coord_ecosystem` · **north_star_fit:** easy (PH-Doc) · **Handoff:** research goal `ui_ux_quality` → `gui_ux_tester`

## Executive summary

- Preflight **`repos_without_live_docs: []`** and **`live_docs_down: []`** — 12/12 handbook URL roots respond (audit green).
- **Reachability ≠ freshness:** [li-language Pages](https://li-langverse.github.io/li-language/) still stale (5-tab nav, hero 404s) until [lic#403](https://github.com/li-langverse/lic/issues/403); documented in lic plan-cross-links + handbook index.
- **lic** PR: audit HEAD vs content honesty + refreshed `gui-ux-quality-handoff` (full GUI sweep vs native-only briefing run).
- Latest `data/latest-gui-ui-run/ui-audit.json` (20:26Z): **1 target**, `world-studio-native` **skip** (SDL/Xvfb) — not a substitute for 15:47Z five-target proactive sweep.
- Cross-links intact: master plan § Doc → provability-gaps → plan-cross-links open PH tracker (2i, 7d, 7e, 8p, Vision-LLM).
- No **G-*** status changes; `matmul_blocked` yellow advisory unchanged.
- `plan_completion_audit`: 5 open tracker rows, 16 partial / 3 missing provability gaps (docs-only alignment, no closure claims).

## Deliverable / findings

| Repo | Change | Notes |
|------|--------|-------|
| **lic** | `plan-cross-links.md`, `gui-ux-quality-handoff.md`, `provability-gaps.md`, `handbook/README.md`, release note | PR on `chore/agent-docs_maintainer-1780177405649` |
| **benchmarks** | This digest | Run artifact only |

**gui_ux_tester:** Use [2026-05-30-gui-ui.md](https://github.com/li-langverse/benchmarks/blob/main/docs/ecosystem/ux-digests/2026-05-30-gui-ui.md) + full-target `run_audit.py` per handoff; read `remediation_manifest.json` `surface` field (GUI vs TUI vs docs).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| docs: audit HEAD vs stale Pages + GUI handoff native-rerun caveat | `lic` | `li-swarm`, `agent:docs_maintainer`, `documentation` |
| [ux-audit] Docs CI strict build failing — GitHub Pages stale | `lic` | `ux-audit`, `surface:docs` — **[#403](https://github.com/li-langverse/lic/issues/403)** |
| [ui-audit] Wire Playwright + axe for dashboard | `li-cursor-agents` | `surface:gui` — **[#32](https://github.com/li-langverse/li-cursor-agents/issues/32)** |
| [ui-audit] Harness probe URL / dev server port | `li-cursor-agents` | `surface:gui` — **[#38](https://github.com/li-langverse/li-cursor-agents/issues/38)** |
| [ui-audit] lic-tetris must not reuse studio SDL stub | `li-cursor-agents` / `lic` | `surface:gui` — **[#46](https://github.com/li-langverse/li-cursor-agents/issues/46)** |
| chore(benchmarks): ecosystem-audit flag stale Pages content (not just HEAD) | `benchmarks` | `ux-audit`, `ready-for-implement` |

## Deferred

- Close master-plan PH rows 2i/7d/7e/8p/Vision-LLM — requires implementation evidence.
- MkDocs Diátaxis restructure ([#422](https://github.com/li-langverse/lic/issues/422)) — after #403 deploy.
- Full satellite handbook content beyond static Pages landing (lip/lis/…).
- TUI harness fixes ([#30](https://github.com/li-langverse/li-cursor-agents/issues/30), [#33](https://github.com/li-langverse/li-cursor-agents/issues/33)) — `tui_ux_tester` / `code_implementer`, not docs_maintainer.
