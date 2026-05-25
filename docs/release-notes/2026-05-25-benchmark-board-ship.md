# Release notes: 2026-05-25 — benchmark-board-ship

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** `feat/benchmark-board-ship`  
**PH / REQ:** WP5, WP4, PH-DB-5, PH-DB-G0  
**Author:** agent

---

## Summary (one sentence)

Ships production-quality **dashboard-next** on GitHub Pages: all nine pillar cards with honest row counts, tier-6 database ingest rows, WP4 proof-posture JSON + `/proofs/`, release-index freshness banner, and Pages CI copying `latest/*.json` artifacts.

## Agent continuation (required)

1. **Read:** `dashboard-next/app/page.tsx`, `scripts/ingest/build_summary.py`, `scripts/build-proof-posture.py`, `.github/workflows/pages.yml`, `docs/dashboard/sitemap.md`
2. **Run:** `cd dashboard-next && npm ci && npm run build`; `LIC_ROOT=../lic LIS_ROOT=../lis ./scripts/ingest/ingest-lic.sh`; confirm `data/latest/summary.json` has nine `pillars` keys and `proof-posture.json` has G-* rows
3. **Then:** merge PR; wait for **Deploy dashboard** on `main`; verify https://li-langverse.github.io/benchmarks/ shows database + proofs pillars; close superseded PRs #75 #77 with pointer to this PR
4. **Blocked on:** Human merge (PR-only); `package-release` dispatches for lip/lit/lidb tags if release-index stays empty in prod ingest

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Dashboard home | `PILLAR_IDS` bento (9 pillars), release freshness banner, `regressionRows(summary.rows)` | `npm run build` green |
| Proof posture | `scripts/build-proof-posture.py`, `dashboard-next/lib/proof-posture.ts`, `data/latest/proof-posture.json` | 23 G-* rows from lic `provability-gaps.md` |
| Ingest / summary | `build_pillars` emits all pillars; `proofs` pillar mapping; `lic_compile_smoke` catalog stub | `build_summary.py` → 9 pillars |
| Catalog | `tier0_stability` → `pillar = proofs`; `lic_compile_smoke`; tier-6 database rows (existing) | `catalog.toml` |
| Pages / CI | Copy `proof-posture.json` into `out/latest/` | `pages.yml`, `ci.yml` dashboard-build |
| Data | Regenerated `summary.json`, `proof-posture.json` | committed under `data/latest/` |

## Not changed (scope fence)

- **li-cursor-agents** deep-link UI (separate PR #18) — briefing already has `benchmark_dashboard_base` on main
- **lic** package-release workflow (PR #272) — docs-only cross-link remains PR #76
- **Tier-6 bench harness execution** in GHA — still stub manifests + `unknown` rows until lidb CSV merge
- **Legacy Vite** `dashboard/` — not removed; Pages uses `dashboard-next` only

## Breaking changes

None.

## Security

N/A — static dashboard + parsed markdown; no new trusted inputs.

## Performance

N/A — static export; ingest unchanged except proof-posture parse (O(rows) on gaps table).

## Downstream

| Repo | Action |
|------|--------|
| li-cursor-agents | use `/bench/{id}/` URLs from briefing after deploy |
| lic | optional: wire compile smoke CSV into `latest.csv` |

## CHANGELOG entry (paste into Unreleased)

- **Benchmark board ship:** dashboard-next nine-pillar bento, proof-posture ingest, release freshness banner, Pages `proof-posture.json` — [2026-05-25-benchmark-board-ship.md](docs/release-notes/2026-05-25-benchmark-board-ship.md).
