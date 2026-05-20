# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- **Tier-5 HTTP exploits:** `exploit_http.py` + `harness/drivers/http_attacks.py` (6 PR attacks vs nginx + li-httpd); `nginx_mitigations.toml` li_done rows; `suite_exploits.toml`; `tier5_exploits_pr` catalog row; `lb_least_conn` / `lb_peer_down` scenarios — see [2026-05-21-tier5-http-exploits.md](docs/release-notes/2026-05-21-tier5-http-exploits.md).

### Added

- **nginx compare pipeline:** vendored `vendor/lis-tier5/` harness (sync via `scripts/sync-lis-tier5-vendor.sh`), `scripts/ingest/merge_lis_http_into_summary.py` (HTTP-only ingest without lic CSV), [http-nginx-compare.md](docs/ecosystem/http-nginx-compare.md).
- **HTTP tier-5 plots:** `scripts/plot_http_benchmarks.py` renders `http_*_rps.png` and `http_tier5_overview.png` from `lis/results/latest.csv` or `summary.json` http category; `scripts/run-http-benchmark-report.sh` runs bench + plots without rewriting `summary.json` (avoids ingest races with other agents).
- **`render-benchmark-visuals.sh`:** optional lis HTTP plots; lic shareables failure no longer aborts when lis CSV is present.

### Fixed

- **Ingest workflows:** `ingest.yml` no longer passes a CSV path as the second argument to `build_summary.py` (that was interpreted as `lis` root and dropped HTTP merge). Workflows now check out **lis**, merge dispatch artifacts into `lic/benchmarks/results/latest.csv`, and run `./scripts/ingest/ingest-lic.sh` with `LIC_ROOT` / `LIS_ROOT`. **Benchmarks CI** and **ecosystem-audit** check out **lis** and set `LIS_ROOT` for the same reason.
- **CI `dashboard-static`:** `ci.yml` gates the Vite `dashboard/dist` build (same as `pages.yml`) instead of `render-static.sh` until `lic` `main` ships `std/plot` (PH-IO-5). Restores green Benchmarks CI on open PRs.
- **Pages 404:** `pages.yml` deploys the Vite `dashboard/dist` again; PH-IO-5 static render was uploading an empty `static-dashboard/` when `lic` lacks `std/plot`.

### Added

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
