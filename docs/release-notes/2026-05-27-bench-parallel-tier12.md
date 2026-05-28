# Release notes: 2026-05-27 — parallel tier-1/2 benches

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (branch `cursor/bench-parallel-tier12-5599`)  
**PH / REQ:** PH-5b / PH-7e (perf harness throughput)  
**Author:** agent

---

## Summary (one sentence)

Tier-1 and tier-2 lic harness benchmarks run in parallel when `BENCH_JOBS>1`, using spare CPU during full-suite runs instead of one benchmark at a time.

## Agent continuation (required)

1. Read: `scripts/run-lic-tier-benches.py`, `scripts/run-full-benchmark-suite.sh`.
2. Run: `LIC_ROOT=../lic BENCH_JOBS=4 SKIP_BUILD=1 SKIP_TIER0=1 ./scripts/run-full-benchmark-suite.sh`.
3. Then: ingest PR with measured `latest.csv` via `ingest-lic.sh`; verify `python3 scripts/check-summary-measurement-coverage.py`.
4. Blocked on: none for harness; full HTTP tier-5 still serial per oracle.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Runner | `scripts/run-lic-tier-benches.py` — `ProcessPoolExecutor`, resume skip | `BENCH_JOBS=4` on 4-core VM |
| Suite | `run-full-benchmark-suite.sh` calls runner instead of inline serial Python | tier 1+2 log shows `parallel: jobs=N` |
| Env | `BENCH_JOBS` (default: `os.cpu_count()`), `BENCH_RESUME=0` to force re-run | documented below |

## Not changed (scope fence)

- `lic/benchmarks/harness/bench.py` — no change; per-benchmark isolation unchanged (`build/bench/<name>/`).
- Tier 0, 3, 5 HTTP multi-oracle, exploits — still serial orchestration.
- Dashboard thresholds / catalog — not in this PR.

## Breaking changes

None.

## Security

N/A — local perf harness only.

## Performance

| Setting | Effect |
|---------|--------|
| `BENCH_JOBS=4` | Up to 4 tier-1/2 benchmarks at once on a 4-core host |
| `BENCH_JOBS=1` | Previous serial behavior |
| `BENCH_RESUME=0` | Re-times all tier-1/2 rows |

## Downstream

| Repo | Action |
|------|--------|
| lic | N/A |
| GHA nightly | Set `BENCH_JOBS` in workflow env if runner has >2 cores |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Added
- Parallel tier-1/2 lic harness runs via `BENCH_JOBS` and `scripts/run-lic-tier-benches.py` — [2026-05-27-bench-parallel-tier12.md](docs/release-notes/2026-05-27-bench-parallel-tier12.md).
```
