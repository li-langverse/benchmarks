# Docs maintainer digest — 1780150168103

**Generated:** 2026-05-30 · **Agent:** `docs_maintainer` · **north_star_fit:** easy (coord_ecosystem · PH-Doc · **ui_ux_quality** handoff)

Preflight: `ecosystem-audit.json` @ 2026-05-30T14:11Z

## Executive summary

- **Live handbook:** `repos_without_live_docs: []`, `live_docs_down: []` — **12/12** Pages green; `https://li-langverse.github.io/lic/` returns **200**.
- **Priority 1–2 (missing/broken Pages):** no action required this pass.
- **Priority 3 (cross-links):** extended [plan-cross-links](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/plan-cross-links.md) + **Doc-c** proof-gap lines on math-linalg, httpd, governance, package-scaffold, 8p, studio-ui-ux.
- **Proactive `ui_ux_quality`:** added [gui-ux-quality-handoff.md](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/gui-ux-quality-handoff.md) for `gui_ux_tester`; supplementary [gui-ux digest](../docs/ecosystem/ux-digests/2026-05-30-gui-ux.md) in benchmarks.
- **lic PR** opened from isolated workspace `chore/agent-docs_maintainer-1780150168103`.
- No **G-*** proof status changes.
- Plan-completion debt (166 findings) remains — stale spec checklists deferred to `plan_verifier`.

## Deliverable / findings

| Item | Detail |
|------|--------|
| Audit | `metrics.repos_without_live_pages: 0`, `repos_with_live_pages: 12` |
| lic PR | GUI UX handoff + plan cross-links (this run) |
| benchmarks | `docs/ecosystem/ux-digests/2026-05-30-gui-ux.md` (handoff support; commit with lic PR or follow-up) |
| Preflight UX | `ux-audit.json` docs-only — GUI journeys need proactive `gui_ux_tester` |

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| **docs: GUI UX handoff + plan cross-links** | `lic` | `docs`, `li-swarm`, `agent:docs_maintainer` |
| Expand preflight `ux-audit` to GUI targets | `li-cursor-agents` | `ux-audit`, `automation` |
| Human merge lic PR + verify handbook links | `lic` | `merge-approved` (human) |

## Deferred

- **lis** satellite handbook (404 if still down — not in `repos_without_live_docs` static set).
- MkDocs strict deploy ([#403](https://github.com/li-langverse/lic/issues/403)) — stale live nav vs local 12-tab build.
- Stale spec checklists (9) in plan-completion-audit — `plan_verifier` domain.
- Self-merge **roadmap** governance PRs.
