# Release notes: 2026-05-25 — SOTA / validity / OS dashboard honesty

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** `feat/sota-validity-os-reporting`  
**PH / REQ:** PH-DB-5, benchmark honesty policy  
**Author:** agent

---

## Summary (one sentence)

Makes **validity gate**, **ratio vs best competitor (`sota_lang`)**, and **host OS** visible on **dashboard-next** with an honesty strip that Li is never labeled best-in-series and green perf requires validity pass.

## Agent continuation (required)

1. **Read:** `dashboard-next/app/page.tsx`, `dashboard-next/app/bench/[id]/page.tsx`, `scripts/ingest/build_summary.py`, `docs/honesty/benchmark-dashboard.md`
2. **Run:** `cd dashboard-next && npm ci && npm run build`; `LIC_ROOT=../lic LIS_ROOT=../lis python3 scripts/ingest/build_summary.py ../lic ../lis` — confirm `data/latest/summary.json` rows include `validity_status`, `ratio_vs_sota`, `sota_lang`, `os`
3. **Then:** merge PR; verify Pages deploy shows honesty strip + bench drill-down panels
4. **Blocked on:** Human merge (PR-only); full CSV ingest with `passed`/`os` columns for non-unknown validity

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Ingest | `build_summary.py` validity gate, `compute_sota`, `reporting.os_values`, row fields | `python3 scripts/ingest/build_summary.py` → 39 rows |
| Schema | `schema/bench-result.json` `validity_status`, `ratio_vs_sota`, `sota_lang`, `os` | JSON schema |
| Catalog | Oracle / validity policy comments + `validity_required` default | `catalog.toml` header |
| Types | `dashboard-next/lib/summary.ts`, `lib/validity.ts` | `npm run build` green |
| Overview | Honesty strip, release-index freshness banner, pillar claimable/invalid/unknown counts | `app/page.tsx` |
| Bench drill-down | Validity panel, perf-not-claimable alert, OS table, best-competitor ratio | `app/bench/[id]/page.tsx` |
| Data | Regenerated `data/latest/summary.json` | committed |

## Not changed (scope fence)

- **li-cursor-agents** supervisor UI — separate repo
- **Proof-posture ingest** (`proof-posture.json`) — not required for this PR
- **Tier-6 database harness execution** — rows may stay `unknown` until lidb CSV lands
- **Legacy Vite** `dashboard/` — unchanged

## Breaking changes

None.

## Security

N/A — static dashboard; ingest reads existing CSV/TOML only.

## Performance

N/A — static export; ingest O(catalog rows).

## Downstream

| Repo | Action |
|------|--------|
| lic / lis | Export `passed` and `os` on bench CSV rows for validity pass + OS table |
| li-cursor-agents | Briefing deep links already on `/bench/{id}/` |

## CHANGELOG entry (paste into Unreleased)

- **Dashboard honesty:** validity gate, best-competitor ratio (`sota_lang`), OS table on bench pages; overview honesty strip — [2026-05-25-sota-validity-os-dashboard.md](docs/release-notes/2026-05-25-sota-validity-os-dashboard.md).
