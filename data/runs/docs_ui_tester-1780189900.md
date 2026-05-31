# Docs UI tester run log — `docs_ui_tester-1780189900`

**Date:** 2026-05-31T01:52Z  
**Agent:** docs_ui_tester (proactive ecosystem sweep)  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-31T01:46Z)  
**Skills:** explore-li-ecosystem, ui-ux-tester-shared  
**north_star_fit:** easy · provable — Vision-LLM handbook surfaces (PH-Vision-LLM)

---

## Executive summary

- Rebuilt `lic/site` via `./scripts/build-docs.sh` (242 HTML); preflight `ui_audit` **pass** (static); proactive Playwright pass **fail** (axe unchanged).
- **Axe:** 12 `color-contrast` + 5 `link-in-text-block` on home desktop — [lic#426](https://github.com/li-langverse/lic/issues/426).
- **Live drift:** 5 tabs vs 12 local; key IA paths 404; search index 248 live vs 1956 local (~87% gap).
- **Deep scan:** 21,143 hrefs, 183 broken, 51 raw `.md` hrefs — [lic#404](https://github.com/li-langverse/lic/issues/404).
- **Baselines:** `ux-harness/baselines/docs/` still missing — [li-cursor-agents#37](https://github.com/li-langverse/li-cursor-agents/issues/37).
- Viewport matrix refreshed (6 local + 4 live PNGs).
- Deploy blocked by [lic#403](https://github.com/li-langverse/lic/issues/403).

---

## Deliverable / findings

See full digest: [`docs/ecosystem/ux-digests/2026-05-31-docs-ui.md`](../docs/ecosystem/ux-digests/2026-05-31-docs-ui.md)

Preflight command:

```bash
LIC_ROOT=/home/s4il0r/Documents/Cursor/li-langverse/lic \
  python3 ../li-cursor-agents/ux-harness/run_audit.py \
  --target lic-docs --mode ui \
  --out-dir data/latest
```

Proactive capture (Playwright via dashboard-ui deps):

```bash
cd ../lic && ./scripts/build-docs.sh
cd ../li-cursor-agents/dashboard-ui && npm install playwright
BENCHMARKS_ROOT=/path/to/benchmarks LIC_ROOT=/path/to/lic \
  node scripts/docs-ui-capture.mjs
```

---

## Recommended issues/PRs

| Priority | Title | Repo | Labels |
|----------|-------|------|--------|
| P0 | [ux-audit] Docs CI strict build failing — GitHub Pages stale | `lic` | existing [#403](https://github.com/li-langverse/lic/issues/403) |
| P1 | [ui-audit] lic-docs: axe color-contrast + link-in-text-block | `lic` | existing [#426](https://github.com/li-langverse/lic/issues/426) |
| P1 | Seed baselines/docs + Playwright capture | `li-cursor-agents` | existing [#37](https://github.com/li-langverse/li-cursor-agents/issues/37) |
| P2 | Built docs site contains raw .md hrefs | `lic` | existing [#404](https://github.com/li-langverse/lic/issues/404) |

---

## Deferred

- Wire Playwright + deep link scan into harness preflight (not docs-only static pass).
- Pixel diff after #37 baselines land.
- Axe sweep across all 12 nav tabs post-#403 deploy.
