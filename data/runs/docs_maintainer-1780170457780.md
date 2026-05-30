# Docs maintainer digest — 2026-05-30 (run 1780170457780)

**Agent:** `docs_maintainer` · **Heap:** `coord_ecosystem` · **north_star_fit:** easy (PH-Doc) · **Handoff:** research goal `ui_ux_quality` → `gui_ux_tester`

## Executive summary

- Preflight **`repos_without_live_docs: []`** and **`live_docs_down: []`** — all 12 org repos report live handbook/Pages URLs (audit green).
- No broken live doc URLs to fix this pass; priority shifted to **cross-links** and **ui_ux_quality** handoff.
- Extended **lic** [plan-cross-links](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/plan-cross-links.md) with open master-plan tracker table (5 PH rows) ↔ provability-gaps ↔ phase plans.
- Refreshed **gui-ux-quality-handoff** with proactive GUI audit snapshot (`data/latest-gui-ui-run/ui-audit.json`, 2026-05-30T15:47Z).
- Linked **Vision-LLM** spec to plan map; **provability-gaps** alignment table now references GUI UX handoff (surface-only, not proof).
- **No G-*** status changes — benchmark honesty preserved (`matmul_blocked` yellow advisory unchanged).
- PR opened on **lic**; benchmarks digest path only (no code change required).

## Deliverable / findings

| Repo | Change | Notes |
|------|--------|-------|
| **lic** | `plan-cross-links.md`, `gui-ux-quality-handoff.md`, `provability-gaps.md`, `li-llm-first-design.md`, release notes | Open PH tracker + ui_ux handoff refresh |
| **benchmarks** | This digest at `data/runs/docs_maintainer-1780170457780.md` | Existing ux digests + remediation manifest already current |

**Cross-links verified:** master plan § Doc → provability-gaps → plan-cross-links open tracker → phase plans (2i/7d/7e/8p/Vision-LLM).

**UI/UX handoff:** `gui_ux_tester` should read proactive `ui-audit.json` (not briefing docs-only `ux-audit.json` alone); P1 items in `remediation_manifest.json` ([#32](https://github.com/li-langverse/li-cursor-agents/issues/32), [#38](https://github.com/li-langverse/li-cursor-agents/issues/38), [#46](https://github.com/li-langverse/li-cursor-agents/issues/46)).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| docs: open PH tracker + ui_ux_quality handoff refresh | `lic` | `li-swarm`, `agent:docs_maintainer`, `documentation` |
| [ui-audit] Wire Playwright snapshots + axe for dashboard | `li-cursor-agents` | `ui-audit`, `surface:gui` ([#32](https://github.com/li-langverse/li-cursor-agents/issues/32)) |
| [ui-audit] Align harness probe URL to Playwright webServer port | `li-cursor-agents` | `ui-audit`, `surface:gui` ([#38](https://github.com/li-langverse/li-cursor-agents/issues/38)) |
| [ui-audit] lic-tetris must not reuse studio SDL stub | `li-cursor-agents` / `lic` | `surface:gui` ([#46](https://github.com/li-langverse/li-cursor-agents/issues/46)) |
| docs: roadmap development-overview live-docs table sync | `roadmap` | `documentation` (human merge) |

## Deferred

- Full mkdocs handbooks for lip/lis beyond static Pages landing (separate pass).
- Close master-plan tracker rows 2i/7d/7e/8p/Vision-LLM — requires implementation evidence, not docs-only PRs.
- 117 catalog path gaps — implementation or catalog lifecycle `planned` cleanup (gap_explorer / code_implementer).
- `agent-repo-workflow.sh prepare` for **benchmarks** digest-only commit if org policy requires PR for `data/runs/` paths.
