# Release notes: 2026-05-28 — dashboard multi-OS fresh tiers

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** branch `cursor/dashboard-multi-os-fresh-5599`

---

## Summary

Dashboard ingest and UI surface **per-OS** measurements (linux, darwin, windows) for every tier present in `latest.csv`, with matrix `?os=` filtering after nightly multi-OS merge.

## Agent continuation

1. Merge **lic** PR #358 (mean ± σ + `os` column on all harnesses).
2. Merge **benchmarks** #126 (parallel full suite) then this PR (or squash dashboard + multi-OS).
3. Run nightly or `LIC_ROOT=../lic ./scripts/run-full-benchmark-suite.sh` then `./scripts/ingest/ingest-lic.sh`.
4. Verify live site: overview OS links, `/matrix/?os=linux`, bench pages show OS when multi-host.

## Changed

| Path | What |
|------|------|
| `scripts/ingest/build_summary.py` | `os_tags_for_bench`, per-OS charts (`id@os`), `reporting.os_values` |
| `scripts/run-benchmark-ci-nightly.sh` | parallel tier 1+2/3 on macOS/Windows core profile |
| `dashboard-next/lib/summary.ts` | `buildSummaryById`, `rowsForBenchmark` |
| `dashboard-next/components/matrix-catalog-table.tsx` | OS column + `?os=` filter |
| `data/latest/summary.json` | refreshed from lic `latest.csv` (linux) |

## Not changed

- Catalog row count vs measured gap (~167/187) — registry stubs still `unknown` until harness fills CSV.
- Live Pages deploy — requires merge to `main` (or nightly bot PR).

## Breaking

N/A

## Performance

N/A — ingest/dashboard only.

## Downstream

Nightly `publish-dashboard` job already merges linux + macOS + Windows artifacts; this ingest reads `os` from CSV so all three appear after green nightly.
