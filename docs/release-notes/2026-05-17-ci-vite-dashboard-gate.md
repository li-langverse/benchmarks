# CI — Vite dashboard gate until lic PH-IO-5

## Summary

Benchmarks CI builds `dashboard/dist` with Node/Vite (matching `pages.yml`) instead of failing on `render-static.sh` while `lic` `main` lacks `std/plot`.

## Agent continuation

1. **Read:** `.github/workflows/ci.yml`, `.github/workflows/pages.yml`, `scripts/dashboard/render-static.sh`.
2. **Run:** `cd dashboard && npm ci && npm run build`; on PRs confirm **Benchmarks CI** `dashboard-build` is green.
3. **Then:** merge open benchmarks PRs (#13, #12, #15); re-enable `dashboard-static` + `render-static.sh` hard gate after **lic** PH-IO-5 (`std/plot`, `plot_render_dashboard`) lands on `main`.
4. **Blocked on:** `li-langverse/lic` PH-IO-5 — no `std/plot` module on `main` yet.

## Changed

| Area | Path | Evidence |
|------|------|----------|
| CI job | `.github/workflows/ci.yml` | `dashboard-build` replaces `dashboard-static` |
| Local render | `scripts/dashboard/render-static.sh` | skip when `std/plot` missing (not in CI path) |
| Changelog | `CHANGELOG.md` | Unreleased Fixed row |

## Not changed

- `pages.yml` (already Vite).
- `render_dashboard.li` or `static-dashboard/` layout.
- Ingest / `summary-compare-gate` in `ingest-smoke`.
- `lic` compiler or runtime.

## Breaking

N/A — CI artifact check only; public Pages URL unchanged.

## Security

N/A — no new trust surface.

## Performance

N/A — CI adds npm build (~same as pre–PH-IO-5 Vite path).

## Downstream

Merge this PR to `main` first, then rebase/merge catalog and agent PRs.
