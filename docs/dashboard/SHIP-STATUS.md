# Benchmark dashboard ship status

**Updated:** 2026-05-26 (agent run, user on break)  
**Tracking PR:** https://github.com/li-langverse/benchmarks/pull/85  
**Live:** https://li-langverse.github.io/benchmarks/

## Merge status

| PR | Role | Status |
|----|------|--------|
| [#85](https://github.com/li-langverse/benchmarks/pull/85) `feat/benchmark-ship-integration` | Integration (catalog 169, dashboard-next, summary.json) | _pending merge_ |
| [#79](https://github.com/li-langverse/benchmarks/pull/79)–[#82](https://github.com/li-langverse/benchmarks/pull/82) | Superseded stack PRs | _close after #85_ |
| [#78](https://github.com/li-langverse/benchmarks/pull/78) | Demo video (docs) | Open — out of ship scope |

**Pre-merge CI (PR #85):** `ingest-smoke`, `dashboard-build` — green on last push before regression-gate commit.

## CI checks added (this ship)

| Check name | Location | Command |
|------------|----------|---------|
| **Dashboard invariants** | `ingest-smoke` job | `python3 scripts/check-dashboard-invariants.py` |
| **Dashboard static routes** | `dashboard-build` job | `./scripts/check-dashboard-static-routes.sh` |

Existing: `summary-compare-gate.sh`, tier-db stub manifests, `test -f data/latest/summary.json`, `test -s dashboard-next/out/index.html`.

## Live URL audit

| Check | Before merge (`main`) | After merge (target) |
|-------|----------------------|----------------------|
| `summary.json` row count (live fetch) | **35** rows | **≥169** |
| `/matrix/` table rows | ~35 | ≥169 + Size column |
| `/bench/simd_dot/` drill-down | Present | Facet panels + validity |
| `latest/summary.json` on Pages | Stale 35-row artifact | Matches `data/latest/summary.json` on `main` |

_Live audit results filled in post-merge below._

### Post-merge audit

- _Deploy workflow:_ _pending_
- _Row count:_ _pending_
- _Matrix / Size column:_ _pending_
- _Broken links:_ _pending_

## Merged PRs (integration contents)

Consolidated on branch `feat/benchmark-ship-integration` (not individual merges):

- Board ship (#79) — nine pillars, proof posture
- Matrix tier filter (#80)
- SOTA / validity / OS (#81)
- Diagram layout IA (#82)
- Catalog expansion + size variants (commits on integration branch)

## Open problems (human)

1. **~109 `path=unknown` catalog rows** — need **lic** harness dirs + CSV before perf colors are meaningful.
2. **Production ingest on CI** — PR CI uses fixture catalog parity; full `ingest-lic.sh` ratios still need sibling CSV refresh.
3. **Memory facet** — RSS series not in ingest yet (stub UI only).
4. **lic pin** — CI uses `lic@c0977131` until `resource_options_invalid` on lic `main`.

## Verify locally

```bash
python3 scripts/check-dashboard-invariants.py
python3 scripts/ingest/build_summary_fixture.py   # refresh summary after catalog edits
cd dashboard-next && npm ci && npm run build
mkdir -p out/latest && cp ../data/latest/*.json out/latest/ 2>/dev/null || true
bash ../scripts/check-dashboard-static-routes.sh
```

## Docs (regression prevention)

- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [INVARIANTS.md](./INVARIANTS.md)
- [coverage-gap-analysis.md](./coverage-gap-analysis.md)
- Release note: [2026-05-26-benchmark-ship-integration.md](../release-notes/2026-05-26-benchmark-ship-integration.md)
