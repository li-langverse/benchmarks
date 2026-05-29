# Release notes: 2026-05-29 — Dashboard completeness sprint (Phase A)

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**Branch:** `cursor/benchmarks-dashboard-completeness-sprint`  
**PH / REQ:** PH-5b, benchmark honesty / multi-OS reporting  

---

## Summary

Phase A adds **catalog `[reporting].platforms`**, ingest **skip charts** for macOS/Windows when only Linux CSV exists, **macOS-normalized OS tags** (no `darwin` in summary), and **`audit-dashboard-gaps.py`** rules that treat explicit `skip` / algo-registry stubs as honest gaps rather than unknown.

## Baseline → after (ingest re-run required for live summary)

| Metric | Baseline (Pages snapshot) | After code (fixture slice) |
|--------|---------------------------|----------------------------|
| P0 gaps | 422 | drops `missing_os` per base when ingest runs |
| `missing_os` | 185 | 0 (3 charts/base: linux measured + macos/windows skip) |
| `bad_size_label` (`harness pending`) | 153 | algo_registry → `algo registry stub` |
| `validity_unknown` | 42 | pending rows → `skip` + source |

Full `data/latest/summary.json` refresh happens on **benchmark-nightly** merge to `main` (multi-OS CSV merge unchanged).

## Changed

| Area | What |
|------|------|
| `catalog.toml` | `[reporting]` defaults: `platforms`, `sota_policy`, `validity_required` |
| `scripts/ingest/build_summary.py` | Platform skip charts, `effective_size_meta`, `macos` OS tag |
| `scripts/audit-dashboard-gaps.py` | `darwin`→`macos`, waive skip/pending SOTA, algo stub labels |
| `tests/test_build_summary_platforms.py` | Unit tests for OS + skip chart behavior |

## Verify

```bash
cd benchmarks
python3 -m unittest tests.test_build_summary_platforms -v
BENCHMARKS_CSV=scripts/ingest/fixtures/summary/lic.csv python3 scripts/ingest/build_summary.py ../lic ../lis
python3 scripts/audit-dashboard-gaps.py
```
