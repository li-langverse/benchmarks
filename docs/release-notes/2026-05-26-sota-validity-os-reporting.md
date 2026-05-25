# SOTA / validity / OS reporting in summary ingest and dashboard

## Summary

`summary.json` ingest adds best-competitor SOTA fields (Li never SOTA), a correctness validity gate before perf colors, and host `os` tags; dashboard-next surfaces them on overview, search, and bench drilldown.

## Agent continuation

1. **Read:** `docs/honesty/benchmark-dashboard.md`, `scripts/ingest/build_summary.py`, `schema/bench-result.json`, `dashboard-next/lib/validity.ts`.
2. **Run:** `python3 scripts/ingest/build_summary_fixture.py`; `python3 -m py_compile scripts/ingest/build_summary.py`; `cd dashboard-next && npm run build`.
3. **Then:** Extend **lic** / **lis** CSV writers with `os` + `passed` on all tier exports; re-run `ingest-lic.sh` so `data/latest/summary.json` picks up production rows.
4. **Blocked on:** Full **lis** tier-5 RPS CSV with `os`/`passed` — HTTP rows may stay unknown until harness ships.

## Changed

| Area | Paths / ids |
|------|-------------|
| Ingest | `scripts/ingest/build_summary.py` — `is_sota_candidate`, `compute_sota`, `validity_for_benchmark`, `apply_validity_gate`, `make_summary_row`, `reporting.os_values` |
| Fixture gate | `scripts/ingest/build_summary_fixture.py`, `scripts/ingest/fixtures/summary/lic.csv`, `stability.csv` |
| Schema | `schema/bench-result.json` — `os`, `passed`, `ratio_vs_sota`, `sota_lang`, `validity_*` |
| Catalog | `catalog.toml` — `validity_required` default + oracle policy comments |
| Dashboard | `dashboard-next/lib/validity.ts`, `lib/summary.ts`, `lib/overview.ts`, `components/bench/validity-*.tsx`, `perf-not-claimable.tsx`, `os-table.tsx`, `benchmark-search.tsx`, `app/page.tsx`, `app/bench/[id]/page.tsx`, `globals.css` |
| Docs | `docs/honesty/benchmark-dashboard.md`, `CHANGELOG.md` |

## Not changed

- Bench **threshold_ratio_cpp** values and harness measurement code in **lic** / **lis**.
- GitHub Pages cutover (still **dashboard-next** build artifact path).
- Agent control plane (**li-cursor-agents**).
- Proof closure in **lic** Lean (`provability-gaps.md`).

## Breaking

N/A — additive JSON fields; consumers ignoring new keys behave as before.

## Security

N/A — static ingest and dashboard; no new secrets or trusted surface.

## Performance

N/A — ingest CPU only; no harness runs in this PR.

## Downstream

- **lic** / **lis:** export `os` and `passed` on `latest.csv` and stability exports.
- **agent-briefing.py:** may cite `validity_status` and `sota_lang` in red-row deep links (follow-up).
