# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed

- **Tier-1 matmul workloads:** sync Li `matmul_naive` / `matmul_blocked` drivers with lic IKJ / blocked IKJ (pending CSV re-ingest) — [2026-05-29-tier1-matmul-dashboard-sprint.md](docs/release-notes/2026-05-29-tier1-matmul-dashboard-sprint.md).
- **Nightly publish:** `publish-dashboard` depends on Linux bench success only (not macOS/Windows) — [2026-05-27-publish-dashboard-linux-only.md](docs/release-notes/2026-05-27-publish-dashboard-linux-only.md).

### Changed

- **Dashboard timing:** mean ± σ and `sample_runs` in langs table and bench pages (`value_stat: mean`) — [2026-05-28-bench-mean-std-dashboard.md](docs/release-notes/2026-05-28-bench-mean-std-dashboard.md).
- **Full suite:** parallel tier 1+2 via `run-lic-tier-benches.py` (`BENCH_JOBS`); tier 3 `--jobs`; defaults `BENCH_RUNS=6`, `BENCH_SUBSEC_MIN_RUNS=20`; supplemental HTTP bench mean ± σ.
- **Multi-OS ingest + dashboard:** `build_summary.py` emits one chart/row per `(benchmark, os)`; matrix `?os=` filter; nightly macOS/Windows CSV merge via `merge_bench_csv_artifacts.py`.
- **Full suite defaults:** `BENCH_RUNS=6`, `BENCH_MIN_RUNS=6`, `BENCH_SUBSEC_MIN_RUNS=20` in `run-full-benchmark-suite.sh`.
- **Dashboard ingest:** refreshed `summary.json` / matrix after `lic` harness merges — [2026-05-27-ingest-post-lic-harness.md](docs/release-notes/2026-05-27-ingest-post-lic-harness.md).

- **Nightly GHA:** full suite on Linux (tier 0–5 + exploits, no `SKIP_*` workarounds); requires `lic` httpd E0303 whitelist + Lean on runner.

### Added

- **Dashboard completeness sprint (Phase A):** catalog `[reporting].platforms`, ingest macOS/Windows skip charts, audit gap script — [2026-05-29-dashboard-completeness-sprint.md](docs/release-notes/2026-05-29-dashboard-completeness-sprint.md).
- **`refresh-dashboard-completeness.py`:** offline summary refresh for multi-OS skip charts; committed `summary.json` P0=0; CI runs `audit-dashboard-gaps.py` on PRs.


### Changed

- **Bench suite / ingest:** export `BENCH_MIN_RUNS=20` for full suite; relative paths in `summary.json` sources; refresh `ecosystem-audit.json` — [2026-05-27-bench-ingest-audit-refresh.md](docs/release-notes/2026-05-27-bench-ingest-audit-refresh.md).

### Changed

- **CI (WP-E1):** Run `dashboard-build` on pull requests only; `pages.yml` builds `dashboard-next` on `main` — [2026-05-25-wp-e1-ci-dedupe.md](docs/release-notes/2026-05-25-wp-e1-ci-dedupe.md).

- **Wave2 ingest:** Refresh `summary.json` after local tier 1+2 harness + partial tier-5 nginx/li — ingest unknown 39→34; tier-2 unknown 5→0 — [2026-05-25-wave2-ingest-unknowns.md](docs/release-notes/2026-05-25-wave2-ingest-unknowns.md).

### Fixed

- **Cloud VM update script:** `scripts/update-cloud-agent-env.sh` — LLVM **22**, all org repos via `gh`, `dashboard-next`, safe git pull — [2026-05-27-fix-cloud-update-script.md](docs/release-notes/2026-05-27-fix-cloud-update-script.md).

- **Overview tier cards:** Measured ok/warn/fail derived from `summary.rows`; pending rows labeled **pending** instead of ingest `tier_counts.unknown` gray **?** — [2026-05-25-fix-overview-tier-cards.md](docs/release-notes/2026-05-25-fix-overview-tier-cards.md).

- **Tier-5 HTTP ingest:** macOS `no_li_httpd_bin` / oracle-only rows → yellow + explicit validity (WP-T5); merge `lis` `benchmarks/results/latest.csv` — [2026-05-25-fix-tier5-summary-unknowns.md](docs/release-notes/2026-05-25-fix-tier5-summary-unknowns.md).

### Fixed

- **Overview tier cards:** Measured ok/warn/fail derived from `summary.rows`; pending rows labeled **pending** instead of ingest `tier_counts.unknown` gray **?** — [2026-05-25-fix-overview-tier-cards.md](docs/release-notes/2026-05-25-fix-overview-tier-cards.md).

- **tier0_stability ingest:** Map lic `stability.csv` strict tests (`harmonic_energy`, `momentum_drift`) to validity pass; refresh `summary.json` / benchmark matrix — [2026-05-25-fix-tier0-stability-ingest.md](docs/release-notes/2026-05-25-fix-tier0-stability-ingest.md).

- **Dashboard SOTA charts:** Relative perf bars on `/bench/[id]` (best competitor = 1.0, higher is better); ingest `ratio_vs_sota` + `series[].relative_perf` — [2026-05-25-sota-relative-charts.md](docs/release-notes/2026-05-25-sota-relative-charts.md).

### Fixed

- **Dashboard bench refresh:** Local tier 1+2 harness (LLVM clang) + tier5 HTTP CSV ingest — 140/179 colored rows — [2026-05-25-refresh-full-bench-run.md](docs/release-notes/2026-05-25-refresh-full-bench-run.md).

- **Dashboard measured coverage:** Ingest expanded lic CSV + catalog path wire + tier-7 registry clone — 142/179 colored rows (79.3%) — [2026-05-25-bench-fill-all-measured.md](docs/release-notes/2026-05-25-bench-fill-all-measured.md).

### Added

- **Dashboard pillar/drilldown charts:** Aggregate SOTA-relative bars on `/pillar/[id]`; five-facet bench composition + facet matrix snippet on `/bench/[id]` — [2026-05-25-pillar-drilldown-charts.md](docs/release-notes/2026-05-25-pillar-drilldown-charts.md).

- **WP5 catalog path sync:** `scripts/catalog/sync-paths-from-lic-tree.py` wires 83 `catalog.toml` paths from the **lic** benchmarks tree; refreshes `summary.json` when CSV exists — [2026-05-25-catalog-sync-paths-lic-tree.md](docs/release-notes/2026-05-25-catalog-sync-paths-lic-tree.md).

### Added

- **tier_db_memory / tier_db_parallel harness wire:** `run-db-*-bench.sh` invoke `lidb/scripts/bench/{memory_footprint,parallel_load}.sh` when `BENCH_DB_*_RUN_HARNESS=1`, with `scripts/lidb-bench-stub/` fallback — [2026-05-25-bench-memory-parallel-wire.md](docs/release-notes/2026-05-25-bench-memory-parallel-wire.md).

### Fixed

- **Harness-backed dashboard rows:** Refresh `data/latest/summary.json` from **lic** tier 1+2 CSV + ingest validity; 16 measured green/yellow/red rows — [2026-05-25-refresh-bench-csv.md](docs/release-notes/2026-05-25-refresh-bench-csv.md).

### Added

- **tier_db_token_efficiency:** Agent query-surface token audit (18 scenarios, SQL vs liq vs ORM/BaaS/GraphQL), `run-db-token-efficiency-bench.sh`, manifest `data/latest/tier-db-token-efficiency.json` — [2026-05-25-tier-db-token-efficiency.md](docs/release-notes/2026-05-25-tier-db-token-efficiency.md).

### Added

- **WP-N4 lidb full-spectrum audit tiers:** `tier_db_security`, `tier_db_memory`, `tier_db_parallel`, `tier_db_audit`, `tier_db_realtime` — docs, suite stubs, catalog rows, CI manifests under `data/latest/` — [2026-05-25-tier-db-full-spectrum.md](docs/release-notes/2026-05-25-tier-db-full-spectrum.md).

### Added

- **Dashboard ship regression gates:** `docs/dashboard/ARCHITECTURE.md`, `INVARIANTS.md`, `check-dashboard-invariants.py`, `check-dashboard-static-routes.sh`; CI steps on Benchmarks CI — [2026-05-26-benchmark-ship-integration.md](docs/release-notes/2026-05-26-benchmark-ship-integration.md).

### Fixed

- **LIC_ROOT / catalog alignment:** `tier0_stability` → `li-tests/benchmarks/tier0_correctness`; `rate_limit_429` vendor path; plan-audit skips `unknown`/`planned` paths; CI checks out `lic@dev` with absolute `LIC_ROOT` — [2026-05-25-lic-root-catalog-alignment.md](docs/release-notes/2026-05-25-lic-root-catalog-alignment.md). Closes benchmarks **#17, #19, #20**; documents **#38** agent-kit sync.

### Added

- **FFT catalog (planned):** `fft_1d_fixed` row (`catalog_lifecycle=planned`) for benchmarks **#18** (harness in **lic**).

- **Benchmark size variants:** `problem_size` / `size_label` / `base_id` in `catalog.toml` and `summary.json`; dashboard size filters; survey doc — [2026-05-26-benchmark-size-variants.md](docs/release-notes/2026-05-26-benchmark-size-variants.md).

- **Catalog expansion (algo_registry):** `scripts/catalog/sync-from-algo-registry.py`; catalog **45 → 169** rows; `summary.json` **35 → 169** rows; tier-2 harness gaps + dashboard tier **6** strip — [2026-05-26-expand-catalog-algorithms.md](docs/release-notes/2026-05-26-expand-catalog-algorithms.md).

- **Dashboard diagram layout:** Algorithm×Facet IA doc, design-system link, `algorithm-facet-grid.tsx` types stub — [2026-05-25-dashboard-diagram-layout.md](docs/release-notes/2026-05-25-dashboard-diagram-layout.md).

### Fixed

- **Dashboard matrix tier filter:** `/matrix/?tier=N` from overview tier strip filters catalog rows; mobile header/main padding — [2026-05-25-dashboard-matrix-tier-filter.md](docs/release-notes/2026-05-25-dashboard-matrix-tier-filter.md).

### Added

- **SOTA / validity / OS reporting:** `summary.json` adds `sota_lang`, `ratio_vs_sota`, validity gate, `os`; ingest never labels Li as SOTA; dashboard-next honesty strip + bench drill-down — [2026-05-26-sota-validity-os-reporting.md](docs/release-notes/2026-05-26-sota-validity-os-reporting.md).

- **Benchmark board ship:** dashboard-next nine-pillar bento, proof-posture ingest, release freshness banner, Pages copies `proof-posture.json` — [2026-05-25-benchmark-board-ship.md](docs/release-notes/2026-05-25-benchmark-board-ship.md).
- **Demo video package:** `docs/dashboard/demo-video-script.md`, `demo-storyboard.html`, `scripts/record-dashboard-demo.sh` for recording the benchmarks portal walkthrough — [2026-05-25-demo-video-package.md](docs/release-notes/2026-05-25-demo-video-package.md).
- **WP9 briefing deep links:** `agent-briefing.py` adds `benchmark_dashboard_base` and `/bench/{id}/` URLs for red rows — [2026-05-25-benchmark-deep-links-briefing.md](docs/release-notes/2026-05-25-benchmark-deep-links-briefing.md).

- **Dashboard Next wave 1:** `dashboard-next/` static export (overview, pillar/bench routes); `catalog.toml` `pillar`/`package`; `ecosystem-packages.toml`; `summary.json` `pillars`; history hash gate — [2026-05-25-dashboard-next-wave1.md](docs/release-notes/2026-05-25-dashboard-next-wave1.md).
- **WP3 release manifests:** `schema/release-manifest.json`, `scripts/ingest/ingest-release-manifests.py`, `data/incoming/manifests/`, `data/latest/release-index.json` ingest; `package-release` `repository_dispatch` on [ingest workflow](.github/workflows/ingest.yml); [docs/dashboard/release-manifest.md](docs/dashboard/release-manifest.md).

### Fixed

- **CI `ingest-smoke`:** Install LLVM **22** via **lic** `ci-install-llvm.sh` (apt.llvm.org on Noble GHA); align `setup-lic-for-bench.sh` — fixes lic CMake pin vs LLVM 18.
- **`plan-completion-audit.py`:** Parse only the master-plan phase tracker; suppress sub-plan `- [ ]` when tracker phases are `[x]`; dedupe master-plan rows from `plan_files_open`; tag phase-02 implementation task lists as `stale_spec_checklists` (exit gates stay actionable) — [2026-05-25-plan-completion-audit-filters.md](docs/release-notes/2026-05-25-plan-completion-audit-filters.md).

### Added

- **lic merged (#153 proxy epoll + seam, #156 E0360 ptr ABI):** tier5 `proxy_loopback,li` ~9.1k req/s (quick wrk); matrix refreshed — [2026-05-21-bench-matrix-post-lic-merge.md](docs/release-notes/2026-05-21-bench-matrix-post-lic-merge.md).

- **HTTP RPS matrix:** `docs/ecosystem/http-server-rps-matrix.md` + `benchmark-matrix-report.py` full scenario grid (`li` on every row); rule `.cursor/rules/li-httpd-bench-matrix.mdc` — [2026-05-22-http-server-rps-matrix.md](docs/release-notes/2026-05-22-http-server-rps-matrix.md).
- **HTTP https_static:** tier5 nightly stub (`verify_skip` until `li-tls` ships) + `catalog.toml` row — [2026-05-22-httpd-https-static-tier5.md](docs/release-notes/2026-05-22-httpd-https-static-tier5.md).
- **HTTP rate_limit_429:** tier5 verify scenario + `catalog.toml` row; harness `bench_rate_limit_scenario` in `vendor/lis-tier5` — [2026-05-22-httpd-rate-limit-tier5.md](docs/release-notes/2026-05-22-httpd-rate-limit-tier5.md).
- **Master-plan progress:** `scripts/httpd-masterplan-step.sh` → `data/latest/httpd-masterplan-progress.md`.
- **Full benchmark matrix:** `benchmark-matrix-report.py` → `data/latest/benchmark-matrix.md` + `.json` (perf catalog + HTTP RPS grid + exploit matrix); always run at end of full suite.
- **Tier-5 HTTP exploits:** `run-tier5-http-exploits.sh` in full suite (`SKIP_EXPLOITS=1` for fast iter only); [http-server-benchmark-growth.md](docs/ecosystem/http-server-benchmark-growth.md).
- **Full benchmark suite:** `scripts/run-full-benchmark-suite.sh`, `setup-lic-for-bench.sh`, `tier5-http-bench.py`; [full-benchmark-suite.md](docs/ecosystem/full-benchmark-suite.md); **AGENTS.md** mandates run after perf/httpd/compiler/physics work.
- **Tier-5 multi-oracle HTTP:** `vendor/lis-tier5/` harness + `run-tier5-http-bench.sh` — **nginx**, **apache**, **lighttpd**, **node**, **bun**, **li** on `static_small` / `keepalive_pipelining`; dashboard shows all oracles.
- **Catalog:** tier-5 HTTP rows for `static_large`, `proxy_loopback`, `lb_round_robin`, `lb_least_conn`, `lb_peer_down` (dashboard was missing proxy/LB dimensions).

### Fixed

- **Tier-5 proxy oracles:** Apache `BalancerMember` syntax (drop `status+H`; `ProxySet lbmethod=byrequests`); lighttpd proxy `document-root` + per-backend host tuples — [2026-05-22-httpd-proxy-oracles.md](docs/release-notes/2026-05-22-httpd-proxy-oracles.md).
- **Tier-5 HTTP benches:** nginx `client_body_temp_path` under `/tmp/nginx-bench`; wrk pipelining via Lua (Debian wrk lacks `--pipeline`).
- **Ingest:** `build_summary.py` honors catalog `variant` when multiple `li` rows exist (e.g. `proxy_loopback` / `li_epoll`).
- **Ingest workflows:** `ingest.yml` no longer passes a CSV path as the second argument to `build_summary.py` (that was interpreted as `lis` root and dropped HTTP merge). Workflows now check out **lis**, merge dispatch artifacts into `lic/benchmarks/results/latest.csv`, and run `./scripts/ingest/ingest-lic.sh` with `LIC_ROOT` / `LIS_ROOT`. **Benchmarks CI** and **ecosystem-audit** check out **lis** and set `LIS_ROOT` for the same reason.
- **CI `dashboard-static`:** `ci.yml` gates the Vite `dashboard/dist` build (same as `pages.yml`) instead of `render-static.sh` until `lic` `main` ships `std/plot` (PH-IO-5). Restores green Benchmarks CI on open PRs.
- **Pages 404:** `pages.yml` deploys the Vite `dashboard/dist` again; PH-IO-5 static render was uploading an empty `static-dashboard/` when `lic` lacks `std/plot`.

### Added

- **Issue hygiene agent:** `scripts/issue-backlog-hygiene.py`, `.cursor/automations/issue-hygiene-agent.md`, briefing recommendation for duplicate/stale/explorer-finding backlog (`docs/release-notes/2026-05-20-issue-hygiene-agent.md`)
- **Docs maintainer:** [handbook](docs/handbook/README.md), [plan cross-links](docs/ecosystem/plan-cross-links.md), [benchmark honesty labels](docs/honesty/benchmark-dashboard.md); Pages 404 runbook in [SETUP_GITHUB.md](SETUP_GITHUB.md)
- **Agent-first architecture:** [cursor-agent-architecture.md](docs/ecosystem/cursor-agent-architecture.md) — Cursor Automations for explorer, PR alignment/review, implementation gaps, numerics SOTA; `agent-preflight.sh` / `agent-briefing.py` for preflight JSON only
- **Ecosystem explorer:** `ecosystem-explorer.py`, skill `explore-li-ecosystem`, automation [ecosystem-explorer.md](.cursor/automations/ecosystem-explorer.md), `/explore-ecosystem`, label `explorer-finding`; HPC rubric (Eigen/Kokkos/PETSc/…) + Reddit/web search queries ([ecosystem-explorer.md](docs/ecosystem/ecosystem-explorer.md))
- **Ecosystem-first** philosophy: [ecosystem-first.md](docs/ecosystem/ecosystem-first.md), [tooling-catalog.md](docs/ecosystem/tooling-catalog.md), rule `li-ecosystem-first`, skill `ecosystem-first`, `file-ecosystem-gap-issue.py`, issue template `ecosystem_gap`
- **Git workflow:** [git-workflow.md](docs/ecosystem/git-workflow.md), rule `li-git-hygiene`; hooks block force push (prefer rebase + normal push)
- **Merge queue plan:** `pr-merge-queue-plan.py`, skill `plan-merge-queue`; `pr-auto-merge-sweep --use-plan` for ordered merge + redundancy skip
- Physics benchmark catalog rows for new `lic` Tier-2 kernels (`docs/release-notes/2026-05-16-physics-catalog-expansion.md`)
- **Numerics research:** [research-methodology.md](docs/numerics/research-methodology.md), skills `research-li-numerics` + `numerics-autoresearch`, `numerics-evidence-checklist.py`, automation `numerics-research-cycle`
- **PR program:** `run-pr-program.py` → `data/latest/pr-program-run.json` (org-wide open PR triage + recommended merge order)
- **Merge conflicts:** skill `resolve-merge-conflicts`, [merge-conflict-resolution.md](docs/ecosystem/merge-conflict-resolution.md), `/resolve-conflicts`
- Feature planner + plan completion audit automations, skills, and scripts (`docs/release-notes/2026-05-16-agent-automations-planning.md`)
- **PH-IO-7:** Li `summary.json` ingest (`build-summary-li.sh`) with Python fallback; CI builds `lic` and runs `summary-compare-gate.sh` on fixtures.
- **PH-IO-5:** Static Pages dashboard via `lic` `std/plot` (`scripts/dashboard/render-static.sh`); Node/Vite removed from `pages.yml` critical path.
- **PH-IO-4:** Li CSV ingest smoke (`scripts/ingest/csv_ingest_smoke.li`) before `build_summary.py`.
- Ecosystem audit (`scripts/ecosystem-audit.py`) + Cursor Automation prompts (`.cursor/automations/`): failed benchmarks, **visual validation** (`render-benchmark-visuals.sh`, manifest + zip); Actions workflow **manual dispatch only** (no cron).
- Actions budget doc (`docs/ecosystem/actions-budget.md`).
- Benchmark history snapshots (`data/history/`, `scripts/record-benchmark-history.py`) with ratio deltas between ingests.
- Agent-kit sync and release-notes policy (roadmap v1.1.0).
- **Li language guides (shareable):** [docs/language/README.md](docs/language/README.md) — real `lic` examples + `scripts/render-li-code-image.py` for **local** editor-style PNGs (`docs/language/assets/*.png` gitignored); handbook link from [docs/handbook/README.md](docs/handbook/README.md).
