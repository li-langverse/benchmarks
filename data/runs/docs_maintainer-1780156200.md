# Docs maintainer digest — 1780156200

**Agent:** `docs_maintainer` · **Run:** `1780156200` · **Heap:** `coord_ecosystem` · **north_star_fit:** easy (PH-Doc) · **Handoff:** research goal `ui_ux_quality` → `gui_ux_tester`

Preflight: `ecosystem-audit.json` @ 2026-05-30T15:43Z

## Executive summary

- **`repos_without_live_docs: []`** and **`live_docs_down: []`** — **12/12** handbook Pages URLs green (`repos_with_live_pages: 12`).
- **Gap:** `plan-cross-links.md` and `docs/handbook/README.md` missing on **lic** `main` despite prior digest claims — added in **lic PR** (this run).
- **Cross-links:** open master-plan tracker table (**2i**, **7d**, **7e**, **8p**, **Vision-LLM**, **PH-UX**) ↔ phase plans ↔ **G-*** IDs; no **Done** status changes.
- **UI/UX handoff:** `plan-cross-links` now indexes `gui_ux_tester` / `docs_ui_tester` digests + `remediation_manifest.json` for swarm goal **`ui_ux_quality`**.
- **`provability-gaps.md`:** added [plan-cross-links](../ecosystem/plan-cross-links.md) in Related (lic PR).
- **Benchmark honesty:** tier-1 near-threshold rows documented only — no proof overclaim (`matmul_naive` 1.105× advisory).
- **GraphQL rate limit** blocked `agent-repo-workflow.sh prepare` — sibling clones used; push when quota resets.
- Post-merge: re-run `python3 scripts/ecosystem-audit.py` — expect live-docs metrics unchanged (already green).

## Deliverable / findings

| Item | Detail |
|------|--------|
| Audit | `metrics.repos_without_live_pages: 0`, `repos_without_live_docs: []`, `live_docs_down: []` |
| **lic** | New `docs/ecosystem/plan-cross-links.md`, `docs/handbook/README.md`; master plan + provability-gaps cross-links |
| **benchmarks** | Extended `docs/ecosystem/plan-cross-links.md` — open PH table + UI/UX audit handoff section |
| **gui_ux_tester** | Proactive digest already at `docs/ecosystem/ux-digests/2026-05-30-gui-ui.md` (run `1780155806337`) — linked from plan-cross-links |
| **G-*** register | **13** partial + **4** missing unchanged — no **Done** rows added |

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| **docs(lic): handbook index + plan cross-links (master ↔ gaps ↔ phases)** | `lic` | `li-swarm`, `agent:docs_maintainer`, `documentation` |
| **docs(benchmarks): open PH tracker + ui_ux_quality handoff in plan-cross-links** | `benchmarks` | `li-swarm`, `agent:docs_maintainer`, `documentation` |
| Human merge **lic#403** — full MkDocs deploy (12-tab IA vs live 5-tab drift) | `lic` | `ux-audit`, `surface:docs` |
| Wire GUI targets into org preflight `ui_audit` (not docs-only) | `benchmarks` | `ui-audit`, `ready-for-implement` |
| **gui_ux_tester:** Playwright + axe for HTML fixtures ([#32](https://github.com/li-langverse/li-cursor-agents/issues/32)) | `li-cursor-agents` | `surface:gui`, `ui-audit` |

## Deferred

- MkDocs nav entry for `plan-cross-links.md` / handbook index (optional — ecosystem paths discoverable via README).
- **lic#403** deploy — clears docs_ui_tester live/local IA drift (~91% search index gap).
- Plan-completion debt (**166** findings) — `plan_verifier` / `implementation_gaps`.
- Self-merge **roadmap** governance PRs — human review only.
- `agent-repo-workflow.sh commit-pr` when GraphQL quota resets.

## Error

```
GraphQL: API rate limit already exceeded for user ID 207167228.
```

Used sibling clones (`../lic`, `../benchmarks`) instead of isolated `data/workspaces/` prepare.

Swarm run id: `1780156200` · Agent id: `docs_maintainer`
