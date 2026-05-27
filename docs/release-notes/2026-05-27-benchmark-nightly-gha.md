# Release notes: 2026-05-27 — benchmark-nightly-gha

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (branch `cursor/benchmark-nightly-gha-ce9b`)  

---

## Summary

Adds daily GitHub Actions `benchmark-nightly.yml` (Linux full suite + macOS/Windows core tiers) that merges CSVs, ingests every catalog row, commits `data/latest/summary.json`, and refreshes the dashboard via Pages.

## Agent continuation

1. Read: `.github/workflows/benchmark-nightly.yml`, `docs/ecosystem/actions-budget.md`.
2. Run: `gh workflow run benchmark-nightly.yml --repo li-langverse/benchmarks` after merge.
3. Then: Verify https://li-langverse.github.io/benchmarks/ `generated_at` updates daily.
4. Blocked on: Linux job wall time (~2h); set org secret only if ingest bot push fails (default `GITHUB_TOKEN` should suffice).

## Changed

| Area | What | Evidence |
|------|------|----------|
| Workflow | Daily 04:00 UTC cron + matrix OS | `.github/workflows/benchmark-nightly.yml` |
| Scripts | `run-benchmark-ci-nightly.sh`, `merge_bench_csv_artifacts.py` | `scripts/` |
| Suite | `SKIP_TIER5_HTTP`, LLVM 22 CC default | `scripts/run-full-benchmark-suite.sh` |

## Not changed

- lic tier-1 push CI (`ci-bench.sh`) — still fast smoke on `benchmarks/**` pushes  
- Cursor automations for audits  

## Breaking changes

None.

## Security

Tier-5 exploits run on Linux nightly unless `skip_exploits` on manual dispatch.

## Performance

Product path: fresh multi-OS CSV → ingest → dashboard. Replaces stale committed `summary.json` (last manual ingest 2026-05-26).

## Downstream

| Repo | Action |
|------|--------|
| lic | Removed weekly bench cron (nightly owned by benchmarks) — companion PR |

## CHANGELOG entry

### Added

- **Benchmark nightly GHA:** daily multi-OS run + dashboard ingest — `docs/release-notes/2026-05-27-benchmark-nightly-gha.md`.
