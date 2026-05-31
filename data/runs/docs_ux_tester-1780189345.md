# Docs UX tester run log — `docs_ux_tester-1780189345`

**Date:** 2026-05-31T01:02Z  
**Agent:** docs_ux_tester (proactive ecosystem sweep)  
**Briefing:** `data/latest/agent-briefing.json` (2026-05-30T21:55Z)  
**Skills:** explore-li-ecosystem, ui-ux-tester-shared  
**north_star_fit:** provable · easy · ecosystem docs (PH-Pkg governance, Vision-LLM handover)

---

## Executive summary

- Refreshed `ux_audit` + `ui_audit` preflight for `lic-docs`: **pass** locally (377 HTML, 0 broken links, rubric min 0.70).
- **P0 unchanged:** Live GitHub Pages stale (5 tabs vs 12 local) — public reading path 404 for new IA; blocked by [lic#403](https://github.com/li-langverse/lic/issues/403).
- **Search index:** live 248 vs local 2801 entries (~91% missing on published site).
- Diátaxis IA friction: 11 language reference pages under Game development tab ([#422](https://github.com/li-langverse/lic/issues/422)); Project tab cognitive load (10+ phase plans).
- SOTA gap vs MkDocs Material: missing `navigation.instant.progress` / `prefetch`; competitor Rust docs model clearer Learning/Mastering split with keyboard search.
- Seven prior control-plane runs today ended **`error`**; this run completes the digest with refreshed harness output.

---

## Deliverable / findings

See full digest: [`docs/ecosystem/ux-digests/2026-05-31-docs-ux.md`](../docs/ecosystem/ux-digests/2026-05-31-docs-ux.md)

Preflight command:

```bash
LIC_ROOT=/home/s4il0r/Documents/Cursor/li-langverse/lic \
  python3 ../li-cursor-agents/ux-harness/run_audit.py \
  --target lic-docs --mode both \
  --out-dir data/latest-docs-ux-run
```

Live verification:

```bash
curl -sI https://li-langverse.github.io/li-language/guide/hello-world/  # 404
curl -sI https://li-langverse.github.io/li-language/search/search_index.json | grep Last-Modified
# last-modified: Sat, 30 May 2026 12:17:17 GMT — 248 docs entries vs 2801 local
```

---

## Recommended issues/PRs

| Priority | Title | Repo | Labels |
|----------|-------|------|--------|
| P0 | [ux-audit] Docs CI strict build failing — GitHub Pages stale | `lic` | existing [#403](https://github.com/li-langverse/lic/issues/403) |
| P0 | Ship satellite handbook Pages (10 repos) | org sweep | `ux-audit`, `surface:docs`, `ready-for-implement` |
| P1 | docs(IA): move language reference out of Game development nav | `lic` | existing [#422](https://github.com/li-langverse/lic/issues/422) |

---

## Deferred

- Playwright mobile_nav capture; axe/contrast ([#426](https://github.com/li-langverse/lic/issues/426)); Diátaxis-hard restructure until #403 lands.
