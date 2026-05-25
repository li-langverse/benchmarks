# Benchmark dashboard ship status

**Updated:** 2026-05-26  
**Integration PR:** [#85](https://github.com/li-langverse/benchmarks/pull/85) — **merged** to `main` (`b87e6b3`)  
**Live:** https://li-langverse.github.io/benchmarks/

## Merge status

| PR | Role | Status |
|----|------|--------|
| [#85](https://github.com/li-langverse/benchmarks/pull/85) | Integration (catalog 169, dashboard-next, summary.json, CI gates) | **Merged** |
| [#79](https://github.com/li-langverse/benchmarks/pull/79)–[#82](https://github.com/li-langverse/benchmarks/pull/82) | Stack PRs (absorbed into #85) | Already merged individually before integration merge |
| [#78](https://github.com/li-langverse/benchmarks/pull/78) | Demo video (docs) | Open — out of ship scope |

**Final CI on #85:** `ingest-smoke` ✅ · `dashboard-build` ✅ (includes invariants + static routes)

## CI checks added

| Check name | Job | Command |
|------------|-----|---------|
| **Dashboard invariants** | `dashboard-build` | `python3 scripts/check-dashboard-invariants.py` |
| **Dashboard static routes** | `dashboard-build` | `./scripts/check-dashboard-static-routes.sh` |

Existing: `summary-compare-gate.sh`, tier-db stub manifests, `ingest-smoke` lic build + ingest.

## Live URL audit (post-merge)

| Check | Result |
|-------|--------|
| `latest/summary.json` row count | **PASS** — **169** rows (after Pages deploy) |
| Overview “benchmarks” count | **PASS** — “169 of 169 benchmarks” |
| `/matrix/` catalog table + Size filter | **PASS** — size pills + “159 of 159” filtered view (full catalog 169) |
| `/bench/matmul_naive/` drill-down | **PASS** — validity gate, facet regions, lic path link |
| Nav links (Overview, Matrix, Proofs, pillars) | **PASS** — sampled via browser |

**Note:** Immediately after merge, CDN could still serve stale `summary.json` (35 rows); after **Deploy dashboard** workflow on `main`, live JSON matches repo.

## Merged deliverables

- `dashboard-next/` — facet matrix, SOTA/validity/OS honesty, nine pillars, proof posture
- `data/latest/summary.json` — **169** rows committed
- `catalog.toml` — **169** benchmarks (no `*_stub` package ids)
- Docs: `ARCHITECTURE.md`, `INVARIANTS.md`, `coverage-gap-analysis.md`
- Release notes: `2026-05-26-benchmark-ship-integration.md`

## Open problems (human)

1. **~109 `path=unknown` rows** — harness + CSV in **lic** before meaningful perf colors.
2. **CI ingest vs dashboard artifact** — `ingest-smoke` may emit fewer measured rows; dashboard gates use **committed** `summary.json` (see `INVARIANTS.md`).
3. **Memory facet** — RSS ingest not wired; UI stub only.
4. **Demo video PR #78** — merge separately when ready.

## Verify locally

```bash
python3 scripts/check-dashboard-invariants.py
cd dashboard-next && npm ci && npm run build
mkdir -p out/latest && cp ../data/latest/{summary,release-index,benchmark-matrix,proof-posture}.json out/latest/ 2>/dev/null || true
bash ../scripts/check-dashboard-static-routes.sh
curl -sS https://li-langverse.github.io/benchmarks/latest/summary.json | python3 -c "import sys,json; print(len(json.load(sys.stdin)['rows']), 'rows')"
```

## Docs index

- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [INVARIANTS.md](./INVARIANTS.md)
- [coverage-gap-analysis.md](./coverage-gap-analysis.md)
- [2026-05-26-benchmark-ship-integration.md](../release-notes/2026-05-26-benchmark-ship-integration.md)
