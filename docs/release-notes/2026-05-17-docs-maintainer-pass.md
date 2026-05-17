# Docs maintainer pass — handbook, plan cross-links, Pages runbook

**Repo:** benchmarks  
**Audience:** agents, maintainers

## Summary

- Added [handbook](../handbook/README.md), [plan cross-links](../ecosystem/plan-cross-links.md), and [benchmark honesty labels](../honesty/benchmark-dashboard.md).
- Expanded [SETUP_GITHUB.md](../../SETUP_GITHUB.md) for **live_docs_down** (Pages 404) recovery.
- README points to in-repo handbook when GitHub Pages is not deployed.

## Live docs

Dashboard URL unchanged: https://li-langverse.github.io/benchmarks/ — requires **Pages → GitHub Actions** + successful `pages.yml` on `main` (human/org step if still 404).

## Cross-repo follow-ups (not in this PR)

- **lic / lip / lit / lis / roadmap:** handbook stubs and mkdocs Pages — separate PRs per repo.
- **roadmap:** do not self-merge; human review on `docs/**`.

## Test plan

- [ ] `open static-dashboard/index.html` after `render-static.sh`
- [ ] Links in handbook resolve on GitHub
- [ ] Re-run `python3 scripts/ecosystem-audit.py` after Pages deploy (expect `live_docs_down` empty)
