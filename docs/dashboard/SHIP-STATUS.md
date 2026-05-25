# Benchmark dashboard ship status

**Updated:** 2026-05-26 (post conflict resolution)  
**Integration PR:** [#85](https://github.com/li-langverse/benchmarks/pull/85) — **merged** to `main` (`185e8e7` after [#87](https://github.com/li-langverse/benchmarks/pull/87) SHIP-STATUS doc)  
**Live:** https://li-langverse.github.io/benchmarks/

## Merge status

| PR | Role | Status |
|----|------|--------|
| [#85](https://github.com/li-langverse/benchmarks/pull/85) | Integration (catalog 169, dashboard-next, summary.json, CI gates) | **Merged** |
| [#83](https://github.com/li-langverse/benchmarks/pull/83)–[#84](https://github.com/li-langverse/benchmarks/pull/84), [#81](https://github.com/li-langverse/benchmarks/pull/81), [#79](https://github.com/li-langverse/benchmarks/pull/79)–[#82](https://github.com/li-langverse/benchmarks/pull/82) | Catalog expand, size variants, SOTA, board stack | **Merged** (absorbed into #85 / main) |
| [#86](https://github.com/li-langverse/benchmarks/pull/86) | LIC_ROOT + `fft_1d_fixed` planned row (WP-G) | **Open** — conflicts resolved 2026-05-26; CI pending |
| [#78](https://github.com/li-langverse/benchmarks/pull/78) | Demo video (docs + `record-dashboard-demo.sh`) | **Open** — conflicts resolved 2026-05-26; CI pending |

**li-cursor-agents [#18](https://github.com/li-langverse/li-cursor-agents/pull/18):** CLEAN (no merge conflicts).

## Conflicts resolved (2026-05-26)

| PR | Branch | Files | Resolution |
|----|--------|-------|------------|
| [#86](https://github.com/li-langverse/benchmarks/pull/86) | `chore/benchmarks-lic-root-catalog` | `catalog.toml`, `data/latest/plan-completion-audit.json`, `data/latest/summary.json` | **Union:** main’s 169-row ship catalog + size/SOTA fields; branch-only `fft_1d_fixed` (`catalog_lifecycle=planned`); regenerated `summary.json` (**170** rows) and plan audit |
| [#78](https://github.com/li-langverse/benchmarks/pull/78) | `feat/demo-video` | `CHANGELOG.md` | **Union:** main CHANGELOG (already lists demo package); branch keeps demo docs/scripts |

Pushed with `--force-with-lease` after `git merge origin/main` (not rebase — preserves branch commits).

## CI checks

| Check | Command |
|-------|---------|
| Dashboard invariants | `python3 scripts/check-dashboard-invariants.py` |
| Dashboard static routes | `./scripts/check-dashboard-static-routes.sh` |
| Dashboard build | `cd dashboard-next && npm ci && npm run build` |
| Ingest smoke | Benchmarks CI `ingest-smoke` (lic build + ingest) |

## Live URL audit (post-#85)

| Check | Result |
|-------|--------|
| `latest/summary.json` row count | **169** on Pages until #86 merges (**170** with `fft_1d_fixed` in repo) |
| Overview “benchmarks” count | Matches committed `summary.json` |
| `/matrix/` size filter | Size pills from `problem_size` / `size_label` / `base_id` |
| `/bench/matmul_naive/` | Validity gate, facets, lic path when known |

## Remaining gaps

1. **~109 `path=unknown` rows** — algo_registry stubs; need **lic** harness + CSV before perf colors.
2. **CI ingest vs dashboard artifact** — `ingest-smoke` may emit fewer measured rows; gates use **committed** `summary.json` ([INVARIANTS.md](./INVARIANTS.md)).
3. **Memory facet** — RSS ingest not wired; dashboard UI stub only.
4. **`fft_1d_fixed` harness** — catalog row planned in #86; implementation in **lic** (benchmarks #18).
5. **PR #78** — docs/recording helper; merge after green CI (not ship-blocking).
6. **PR #86** — merge after green CI; adds 170th catalog row + LIC_ROOT audit already on main.

## Verify locally

```bash
python3 scripts/check-dashboard-invariants.py
LIC_ROOT=../lic python3 scripts/plan-completion-audit.py
cd dashboard-next && npm ci && npm run build
```

## Docs index

- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [INVARIANTS.md](./INVARIANTS.md)
- [coverage-gap-analysis.md](./coverage-gap-analysis.md)
