# Release notes: 2026-05-25 — bench-fill-all-measured

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** feat/bench-fill-all  
**PH / REQ:** dashboard ship / PH-5b  
**Author:** agent

---

## Summary (one sentence)

Raises dashboard measured coverage from ~9% to **79.3%** (142/179 colored rows) by ingesting expanded **lic** `latest.csv`, wiring all catalog `path=` fields, and adding tier-7 registry family CSV clone in the full-suite script.

## Agent continuation (required)

1. **Read:** `scripts/run-full-benchmark-suite.sh` (tier 7 + CC fallback); `scripts/catalog/wire-registry-paths.py`; **lic** `benchmarks/harness/bench_registry.py`.
2. **Run:** `LIC_ROOT=../lic ./scripts/run-full-benchmark-suite.sh` then `./scripts/ingest/ingest-lic.sh`; `python3 scripts/check-summary-measurement-coverage.py`.
3. **Then:** Merge **lic** PR `feat/bench-harness-fill-all-registry` first; re-run suite on CI macOS with `clang-18` or host `clang`; close remaining 37 unknown rows (tier0, DB tier6, HTTP-only, Li build failures on cloth/euler/rigid/wind).
4. **Blocked on:** **lidb** tier_db harness CSV for 18 DB rows; **lis** static_large wrk parse; **lic** Li builds for `cloth_swing`, `euler_fluid_2d`, `combustion_passive`, `wind_field_bc`, `rigid_body_stack`.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Data | `data/latest/summary.json` — 132 green, 4 yellow, 6 red, 37 unknown | Local ingest after lic CSV refresh |
| Suite | `scripts/run-full-benchmark-suite.sh` — tier 7 registry clone; CC fallback | — |
| Catalog | `catalog.toml` — 0 rows with `path=unknown` (109→0) | `wire-registry-paths.py` + prior sync |
| Scripts | `scripts/catalog/wire-registry-paths.py` | New |
| Coverage | `check-summary-measurement-coverage.py` PASS (142 colored) | Local |

## Not changed (scope fence)

- **dashboard-next** UI measured/pending strip.
- **lidb** real Postgres benchmark execution (stubs/manifests only).
- **lic** compiler fixes for failed tier-2 Li builds (separate PR).
- Histogram memory facet (RSS ingest).

## Breaking changes

None.

## Security

N/A — ingest reads local CSV only.

## Performance

N/A — reporting only; tier-7 clone duplicates template timings (no new kernel work).

## Downstream

| Repo | Action |
|------|--------|
| **lic** | Merge `feat/bench-harness-fill-all-registry`; refresh CSV on `main` |
| Pages | Redeploy after `summary.json` on `main` |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Fixed
- **Dashboard measured coverage:** Ingest expanded lic CSV + catalog path wire + tier-7 registry clone — 142/179 colored rows (79.3%) — [2026-05-25-bench-fill-all-measured.md](docs/release-notes/2026-05-25-bench-fill-all-measured.md).
```
