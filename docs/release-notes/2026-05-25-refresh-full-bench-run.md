# Release notes: 2026-05-25 — refresh-full-bench-run

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** feat/refresh-full-bench-run  
**PH / REQ:** PH-5b / dashboard ship  
**Author:** agent

---

## Summary (one sentence)

Refreshes `data/latest/summary.json` from a local fair-release **lic** tier 1+2 harness run (LLVM clang) plus **lis** tier-5 HTTP CSV merge, raising colored dashboard rows from 16 to **140** (37 still `unknown`).

## Agent continuation (required)

1. **Read:** `scripts/run-full-benchmark-suite.sh`; `docs/honesty/benchmark-dashboard.md`; **lic** `benchmarks/results/latest.csv` (sibling checkout, not committed here).
2. **Run:** `CC=/opt/homebrew/opt/llvm/bin/clang CXX=... SKIP_TIER0=1 LIC_ROOT=../lic ./scripts/run-full-benchmark-suite.sh` (fix tier3 `await_codegen_ok.li` or skip); `./scripts/ingest/ingest-lic.sh`; `python3 scripts/check-dashboard-invariants.py`.
3. **Then:** Commit refreshed **lic** `latest.csv` on **lic** `main` when CI green; close 37 unknown (tier0, tier6 DB, HTTP proxy_loopback without li-httpd, 5 Li build failures).
4. **Blocked on:** **lic** tier3 compile bench (`await_codegen_ok.li`); **lic** Li builds for `cloth_swing`, `euler_fluid_2d`, `combustion_passive`, `wind_field_bc`, `rigid_body_stack`; **lidb** tier_db harness for tier6.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Data | `data/latest/summary.json` — 130 green, 4 yellow, 6 red, 39 unknown (179 rows) | Ingest `2026-05-25T17:28:15Z` |
| Vendor | `vendor/lis-tier5/results/latest.csv` — 45 HTTP rows (profile=nightly) | `run-tier5-http-bench.sh` |
| Machine | arm64 MacBookAir; tier12 ~8.4 min (`BENCH_RUNS=1`, LLVM clang) | Local log `/tmp/bench-full-run2.log` |
| Gates | `check-dashboard-invariants.py`, `check-summary-measurement-coverage.py` PASS | 140 colored rows |

## Not changed (scope fence)

- **lic** `benchmarks/results/latest.csv` — updated locally (~705 rows post tier5 merge), not in this PR.
- **dashboard-next** UI / histogram memory facet.
- **lidb** tier_db real execution (tier6 rows stay unknown).
- Tier-7 registry clone (not implemented on this **lic** ref — `tier 7 benchmarks: not implemented`).

## Breaking changes

None.

## Security

N/A — reads local harness CSV only.

## Performance

| Bench families (native harness, green) | Notes |
|--------------------------------------|-------|
| `simd_dot`, `matmul_naive`, `matmul_blocked`, `reduce_sum`, `horner_pure_li` | tier1 micro |
| `num_*` (cg, cholesky, fft, integrators, opt, …) | tier1 numerics |
| `md_*`, `three_body`, `nbody_gravity`, `heat_equation_2d`, … | tier2 physics (5 Li builds skipped) |
| HTTP oracles | partial — tier5 catalog rows mostly unknown without `li-httpd` |

Registry-alias rows (e.g. `cfd_*`, `fea_*`, `am_*`) colored via prior catalog path wiring + CSV template propagation from harness families — not independent kernels.

## Downstream

| Repo | Action |
|------|--------|
| **lic** | Optional: commit `benchmarks/results/latest.csv` after review |
| Pages | Redeploy on merge to `main` |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Fixed
- **Dashboard bench refresh:** Local tier 1+2 + tier5 ingest — 140/179 colored rows — [2026-05-25-refresh-full-bench-run.md](docs/release-notes/2026-05-25-refresh-full-bench-run.md).
```
