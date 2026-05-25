# Release notes: 2026-05-25 — SOTA relative perf charts

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** `feat/sota-relative-charts`  
**PH / REQ:** PH-DB-5, benchmark dashboard honesty  
**Author:** agent

---

## Summary (one sentence)

Fixes **SOTA semantics** so `ratio_vs_sota` and bench diagrams use **relative speed** (best competitor = 1.0, higher is better) with **absolute units only in the table below** the bar chart on `/bench/[id]`.

## Agent continuation (required)

1. **Read:** `docs/dashboard/diagram-layout.md`, `docs/honesty/benchmark-dashboard.md`, `dashboard-next/components/bench/perf-relative-bars.tsx`, `scripts/ingest/build_summary.py` (`relative_perf_vs_sota`)
2. **Run:** `python3 scripts/ingest/build_summary.py ../lic ../lis`; `python3 scripts/check-dashboard-invariants.py`; `cd dashboard-next && npm run build`
3. **Next:** WP2 virtualized facet matrix on `/matrix`; optional history sparklines in perf column
4. **Blocked:** Human merge (PR-only); do not label Li SOTA or weaken `check-dashboard-invariants.py`

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Ingest | `relative_perf_vs_sota`, `enrich_series_relative_perf`; `ratio_vs_sota` = Li relative speed; `reporting.relative_perf_higher_is_better` | `build_summary.py` |
| Data | Regenerated `data/latest/summary.json` (179 rows) | `check-dashboard-invariants.py` PASS |
| Types | `LangPoint.relative_perf`, `SummaryReporting`, `SummaryRow.pending` | `dashboard-next/lib/summary.ts` |
| UI | `PerfRelativeBars` on bench drill-down; absolute `LangsTable` below | `app/bench/[id]/page.tsx`, `perf-relative-bars.tsx` |
| Docs | Honesty ratio semantics | `docs/honesty/benchmark-dashboard.md` |

## Not changed (scope fence)

- **Threshold oracle** (`ratio_vs_cpp` / `compare_oracle`) and validity gate — unchanged
- **Legacy Vite** `dashboard/` — unchanged
- **li-cursor-agents** supervisor UI — separate repo
- **Matrix facet virtualization** — still WP2 (`algorithm-facet-grid` stub)

## Breaking changes

None for API consumers; **`ratio_vs_sota` meaning changes** from Li/oracle time ratio to relative speed (1.0 = SOTA). Update prose that cited old `1.18×` style ratios.

## Security

N/A — static dashboard; ingest reads existing CSV/TOML only.

## Performance

N/A — static export; ingest O(catalog rows).

## Downstream

| Repo | Action |
|------|--------|
| Agents / briefing | Cite relative speed (`0.85` = 85% of `{sota_lang}`), not “Li is SOTA” |
| lic / lis | No CSV schema change; optional future export of precomputed `relative_perf` |

## CHANGELOG entry (paste into Unreleased)

- **Dashboard SOTA charts:** Relative perf bars on `/bench/[id]` (SOTA = 1.0); `ratio_vs_sota` and `series[].relative_perf` in ingest — [2026-05-25-sota-relative-charts.md](docs/release-notes/2026-05-25-sota-relative-charts.md).
