# Release notes: 2026-05-25 — wave2-ingest-unknowns

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** feat/wave2-ingest-unknowns  
**PH / REQ:** PH-IO (dashboard ingest honesty)  
**Author:** agent (wave2 sequential)

---

## Summary (one sentence)

Refreshed `data/latest/summary.json` after local tier 1+2 harness (Apple clang) and partial tier-5 nginx/li HTTP run, lowering ingest `unknown` from 39→34 while overview tier cards continue to show catalog **pending** separately from measured gray **?**.

## Agent continuation (required)

1. Read: `docs/honesty/benchmark-dashboard.md`, `data/latest/summary.json` `tier_counts`, overview `splitTierCounts` in `dashboard-next/lib/coverage.ts`.
2. Run: `LIC_ROOT=../lic LIS_ROOT=../lis ./scripts/run-full-benchmark-suite.sh` on Linux CI (clang-18, full tier3+tier5 oracles) → `python3 scripts/ingest/build_summary.py` → invariant scripts → `cd dashboard-next && npm run build`.
3. Then: merge green WP branches (`feat/fix-overview-tier-cards`, tier0/tier2/tier5/tier_db, pillar charts) when PRs exist; re-ingest to clear tier 5/6 catalog pending.
4. Blocked on: `gh pr merge` for #102 (branch protection); tier3 `await_codegen_ok.li` compile on current lic; tier_db harness rows (19 pending).

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Ingest | `build_summary.py` from updated `lic/benchmarks/results/latest.csv` (707 rows post tier5 merge) | `unknown` 34/179 rows; tier2 `unknown` 0 |
| Checks | Dashboard invariants + measurement coverage | `check-dashboard-invariants.py` PASS; `check-summary-measurement-coverage.py` PASS (145 colored) |
| Branch | Includes fast-forward of `feat/sota-relative-charts` (PR #102 CI green, merge blocked) | `relative_perf` on bench drill-down |

- `data/latest/summary.json` — regenerated `generated_at`, tier_counts, row statuses from local harness.
- Local bench: tier0 li-tests 18 fail (verify); tier12 11 Li pure builds skipped (contracts); tier3 ecosystem aborted; tier5 `BENCH_HTTP_QUICK_SEC=3` nginx+li wrk only.

## Not changed (scope fence)

- `feat/fix-overview-tier-cards` / tier0 / tier2 / tier5 / tier_db / pillar chart PRs — not merged to `main` (no remote branches or policy block).
- Full tier-5 scenario matrix (`https_static`, LB, etc.) — still catalog pending; vendor CSV uses `proxy_loopback` ids.
- Tier 6 lidb measured harness — **not** run (`BENCH_DB_*_RUN_HARNESS` unset).
- `lic` / `lis` source — benchmark CSVs updated locally only, not committed in those repos.

## Breaking changes

None.

## Security

N/A — ingest-only; no CVE catalog or exploit profile changes in this PR.

## Performance

N/A for merge gate — local tier1+2 wall times refreshed; no dashboard ratio threshold changes. Reproduce: `SKIP_BUILD=1 LIC_ROOT=../lic LIS_ROOT=../lis ./scripts/run-full-benchmark-suite.sh` (macOS clang).

## Downstream

| Repo | Action |
|------|--------|
| benchmarks Pages | Deploy after merge; ingest timestamp updates on live site |
| lic / lis | Optional: commit `benchmarks/results/latest.csv` from CI full suite |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Changed
- **Wave2 ingest:** Refresh `summary.json` after local tier 1+2 + partial tier-5 — unknown 39→34, tier-2 fully colored — [2026-05-25-wave2-ingest-unknowns.md](docs/release-notes/2026-05-25-wave2-ingest-unknowns.md).
```
