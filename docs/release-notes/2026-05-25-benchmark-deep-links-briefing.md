# Release notes: 2026-05-25 — benchmark-deep-links-briefing

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** (branch `feat/wp3-release-manifest` or follow-up)  
**PH / REQ:** WP9  
**Author:** agent

---

## Summary (one sentence)

`agent-briefing.py` now emits `benchmark_dashboard_base` and per-red-bench `/bench/{id}/` deep links for dashboard-next and li-cursor-agents interventions.

## Agent continuation (required)

1. Read: `scripts/agent-briefing.py` (`enrich_benchmark_deep_links`), `docs/dashboard/sitemap.md`
2. Run: `python3 scripts/agent-briefing.py --skip-slow` and confirm `data/latest/agent-briefing.json` has `benchmark_dashboard_base` and `benchmarks.deep_links`
3. Then: merge with li-cursor-agents `feat/benchmark-deep-links` PR so control-plane links use first red bench URL
4. Blocked on: none

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Briefing | `benchmark_dashboard_base`, `benchmarks.deep_links`, `ecosystem_audit.benchmarks.deep_links` | `python3 -c` enrich smoke on red row |
| Automation doc | `dashboard-next` routes in `.cursor/automations/repos/benchmarks.md` | path updated |

## Not changed (scope fence)

- `ecosystem-audit.py` red row detection — unchanged
- Dashboard-next UI — no route changes
- Ingest / `summary.json` generation — unchanged

## Breaking changes

None.

## Security

N/A — briefing JSON only; no new trust surface.

## Performance

N/A — O(n) over red rows at briefing time.

## Downstream

| Repo | Action |
|------|--------|
| li-cursor-agents | consume `deep_links` / `benchmark_dashboard_base` in `interventions.ts` |

## CHANGELOG entry (paste into Unreleased)

- **WP9 briefing deep links:** `agent-briefing.py` adds `benchmark_dashboard_base` and `/bench/{id}/` URLs for red rows — [2026-05-25-benchmark-deep-links-briefing.md](docs/release-notes/2026-05-25-benchmark-deep-links-briefing.md).
