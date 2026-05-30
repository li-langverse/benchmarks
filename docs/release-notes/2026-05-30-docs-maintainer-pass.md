# Docs maintainer pass — live handbook URLs + audit HEAD checks

**Repo:** benchmarks (orchestration) + cross-repo Pages scaffolds  
**Audience:** agents, maintainers

## Summary

- `scripts/ecosystem-audit.py` now HEAD-checks per-repo handbook URLs (`REPO_LIVE_DOC_URLS`) instead of a static missing list; **lic** canonical site is **li-language** mkdocs.
- Added `scripts/bootstrap-minimal-handbook-pages.sh` and `scripts/templates/minimal-handbook-pages/` for package/tooling repos.
- Opened companion PRs: **lip**, **lit**, **lis**, **li-net**, **li-httpd**, **li-std-core**, **li-std-math**, **li-demo**, **roadmap** (site root redirect), **lic** (in-repo handbook index).

## Preflight (before merge)

| Check | Expected after Pages deploy |
|-------|----------------------------|
| `python3 scripts/ecosystem-audit.py` | `repos_without_live_docs` shrinks as each `https://li-langverse.github.io/<repo>/` returns 200 |
| `live_docs_down` | empty for benchmarks + li-language |
| roadmap root | `https://li-langverse.github.io/roadmap/` → redirect or 200 |

## Cross-links

- [plan-cross-links.md](../ecosystem/plan-cross-links.md)
- [handbook/README.md](../handbook/README.md)

## Deferred

- Human enable **Settings → Pages → GitHub Actions** on each new site repo.
- **roadmap** governance paths: human merge only.
- Full mkdocs for **lip** / **lis** (static landing pages only in this pass).
