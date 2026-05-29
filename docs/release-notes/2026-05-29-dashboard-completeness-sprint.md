# Release notes: 2026-05-29 — Dashboard completeness sprint (Phase A)

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**Branch:** `cursor/benchmarks-dashboard-completeness-sprint`  
**PH / REQ:** PH-5b, benchmark honesty / multi-OS reporting  

---

## Summary

Phase A adds **catalog `[reporting].platforms`**, ingest **skip charts** for macOS/Windows when only Linux CSV exists, **macOS-normalized OS tags** (no `darwin` in summary), and **`audit-dashboard-gaps.py`** rules that treat explicit `skip` / algo-registry stubs as honest gaps rather than unknown.

## Baseline → after

| Metric | Baseline (Pages snapshot) | After (`refresh-dashboard-completeness.py`) |
|--------|---------------------------|---------------------------------------------|
| P0 gaps | 422 | **0** |
| P1 gaps | 194 | **0** |
| `missing_os` | 185 | 0 (linux measured + macos/windows skip per base) |
| `bad_size_label` | 153 | 0 (`effective_size_meta` + catalog `fft_1d_fixed`) |
| `validity_unknown` | 42 | 0 (pending → `skip` + source) |

Nightly merge to `main` still refreshes live CSV measurements; committed `summary.json` is audit-clean for PR CI.

## Changed

| Area | What |
|------|------|
| `catalog.toml` | `[reporting]` defaults: `platforms`, `sota_policy`, `validity_required` |
| `scripts/ingest/build_summary.py` | Platform skip charts, `effective_size_meta`, `macos` OS tag |
| `scripts/audit-dashboard-gaps.py` | `darwin`→`macos`, waive skip/pending SOTA, algo stub labels |
| `scripts/refresh-dashboard-completeness.py` | Offline multi-OS chart refresh without full lic build |
| `tests/test_build_summary_platforms.py` | Unit tests for OS + skip chart behavior |
| `tests/test_audit_dashboard_gaps.py` | P0 gate on committed `summary.json` |
| `.github/workflows/ci.yml` | `dashboard-build` runs `audit-dashboard-gaps.py` |

## Verify

```bash
cd benchmarks
python3 -m unittest tests.test_build_summary_platforms -v
BENCHMARKS_CSV=scripts/ingest/fixtures/summary/lic.csv python3 scripts/ingest/build_summary.py ../lic ../lis
python3 scripts/refresh-dashboard-completeness.py
python3 scripts/audit-dashboard-gaps.py   # exit 0
python3 -m unittest tests.test_audit_dashboard_gaps -v
```
