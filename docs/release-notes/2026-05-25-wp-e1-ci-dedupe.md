# Release notes: 2026-05-25 — wp-e1-ci-dedupe

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (open after push)  
**PH / REQ:** org hygiene WP-E1  
**Author:** agent

---

## Summary (one sentence)

Skip `dashboard-build` on push to `main` so `pages.yml` is the only workflow that builds `dashboard-next` on publish paths, removing duplicate npm CI on data merges.

## Agent continuation (required)

1. Read: `.github/workflows/ci.yml`, `.github/workflows/pages.yml`, `docs/ecosystem/actions-budget.md`.
2. Run: open a PR to `main`; confirm PR CI still runs `ingest-smoke` + `dashboard-build`; after merge, push a `data/latest/**` change and confirm only one `dashboard-next` build runs (`pages.yml`, not `ci.yml` `dashboard-build`).
3. Then: none for WP-E1; proceed WP-E2 fuzz cache on `lic` after WP-C2 merges.
4. Blocked on: none.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| CI | `dashboard-build` gated with `if: github.event_name == 'pull_request'` | `.github/workflows/ci.yml` |
| Docs | Actions budget table reflects 1 vs 2 jobs by event | `docs/ecosystem/actions-budget.md` |

## Not changed (scope fence)

- `ingest-smoke` job on push/PR — unchanged (still builds lic + ingest on every PR and `main` push).
- `pages.yml` deploy path filters — unchanged.
- `ingest.yml` repository_dispatch ingest — unchanged.
- Dashboard source or `dashboard-next/package.json` — unchanged.

## Breaking changes

None.

## Security

N/A — workflow condition only; no trust boundary change.

## Performance

N/A for bench rows; saves ~1–2 Actions minutes per `main` push that also triggers Pages (duplicate `npm ci` + `next build` removed).

## Downstream

| Repo | Action |
|------|--------|
| All | N/A |

## CHANGELOG entry (paste into Unreleased)

- **CI (WP-E1):** Gate `dashboard-build` to PRs only; `pages.yml` owns `dashboard-next` build on `main` — [2026-05-25-wp-e1-ci-dedupe.md](docs/release-notes/2026-05-25-wp-e1-ci-dedupe.md).
