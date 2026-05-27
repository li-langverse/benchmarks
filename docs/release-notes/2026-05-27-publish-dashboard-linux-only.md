# Release notes: 2026-05-27 — publish-dashboard-linux-only

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (branch `cursor/publish-dashboard-linux-ce9b`)  
**PH / REQ:** PH-5b (benchmark dashboard ops)  
**Author:** agent

---

## Summary (one sentence)

`publish-dashboard` in benchmark nightly runs when Linux succeeds, without waiting for macOS/Windows bench jobs.

## Agent continuation (required)

1. Read: `.github/workflows/benchmark-nightly.yml` `publish-dashboard` job.
2. Run: merge PR; trigger `workflow_dispatch` or wait for cron; confirm `publish-dashboard` runs after green `bench-linux`.
3. Then: merge bot PR `bot/nightly-summary-*` when created; verify https://li-langverse.github.io/benchmarks/ `/matrix` updated.
4. Blocked on: **lic** PR for tier-1 validity reds (`cursor/bench-validity-scorecard-ce9b`) before dashboard shows green for `horner_pure_li` / `reduce_sum`.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| GHA | `publish-dashboard.needs: [bench-linux]` only | `.github/workflows/benchmark-nightly.yml` |

## Not changed (scope fence)

- macOS/Windows bench jobs still run (artifacts optional for publish)
- Harness / ingest logic — **not** in this PR
- Ecosystem quality scorecard weights — **not** changed

## Breaking changes

None.

## Security

N/A.

## Performance

N/A — CI orchestration only; restores nightly dashboard data refresh on Linux-only green.

## Downstream

| Repo | Action |
|------|--------|
| lic | Merge bench validity PR; nightly ingest uses new CSV `passed` semantics |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Fixed
- **Nightly publish:** dashboard publish no longer blocked by failed macOS/Windows bench jobs ([#NNN](URL)).
```
