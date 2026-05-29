# Docs UI tester digest — 2026-05-29

**Agent:** `docs_ui_tester` · **Source:** proactive · **Pass:** 2026-05-29T17:58Z  
**North star:** easy pillar — handbook links and contrast must not block proof-first contributor workflows (PH-2i adjacent)

## Executive summary

- Harness **`lic-docs` pass** but **`links_checked: 0`** — static adapter blind spot ([#36](https://github.com/li-langverse/li-cursor-agents/issues/36)).
- Deep scan: **45 relative raw `.md` hrefs** + **26 GitHub blob links** in built `lic/site/` ([#404](https://github.com/li-langverse/lic/issues/404)).
- Live Pages returns **HTTP 200**; local `site/` is audit source of truth.
- No Playwright baselines under `ux-harness/baselines/docs/` ([#37](https://github.com/li-langverse/li-cursor-agents/issues/37)).
- Manual token contrast: all sampled pairs **WCAG AA pass**.
- `ui_audit` not embedded in briefing JSON — coord gap for heap recommendation.
- **8 repos** without live docs — defer to `docs_maintainer`.
- Existing remediation issues remain open; no duplicate issues filed.

## Deliverable / findings

| Check | Result | Severity |
|-------|--------|----------|
| Preflight `ui-audit.json` | 1 target, 0 failing | Misleading |
| Deep link scan | 45 raw + 26 GitHub `.md` hrefs | **P1** |
| Desktop / mobile screenshots | Not run | **P2** |
| axe violations | Not run | **P2** |
| Baseline drift | No baseline dir | **P2** |
| Contrast tokens | AA pass (17.3:1 – 6.7:1) | OK |

Full tables: [ux-digests/2026-05-29-docs-ui.md](../../docs/ecosystem/ux-digests/2026-05-29-docs-ui.md)

## Recommended issues/PRs

| Priority | Repo | Title |
|----------|------|-------|
| P1 | `lic` | [#404](https://github.com/li-langverse/lic/issues/404) raw `.md` hrefs in built site |
| P1 | `li-cursor-agents` | [#36](https://github.com/li-langverse/li-cursor-agents/issues/36) static_site href parsing |
| P2 | `li-cursor-agents` | [#37](https://github.com/li-langverse/li-cursor-agents/issues/37) baselines + Playwright |
| P2 | `benchmarks` | Embed `ui_audit` in `agent-briefing.json` |

## Deferred

- axe + screenshot capture until #37 lands.
- Per-repo MkDocs targets beyond `lic-docs`.
- 8-repo live Pages onboarding (`docs_maintainer`).
- No merges; no GHA cron added.
