# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed

- **`tier0_stability` catalog path:** `catalog.toml` now points to **`li-tests/benchmarks/tier0_correctness`** on **lic** (matches harness layout); `plan-completion-audit` **catalog_gaps** clear when `LIC_ROOT` is current. See `docs/release-notes/2026-05-20-catalog-tier0-lic-path.md`.
- **CI `dashboard-static`:** `ci.yml` gates the Vite `dashboard/dist` build (same as `pages.yml`) instead of `render-static.sh` until `lic` `main` ships `std/plot` (PH-IO-5). Restores green Benchmarks CI on open PRs.
- **Pages 404:** `pages.yml` deploys the Vite `dashboard/dist` again; PH-IO-5 static render was uploading an empty `static-dashboard/` when `lic` lacks `std/plot`.

### Added

- **Cursor rule:** `.cursor/rules/lic-benchmark-catalog-parity.mdc` — `catalog.toml` `repo=lic` paths must exist under `LIC_ROOT`; run `plan-completion-audit.py` before merge; ingest honesty.
- **GEMM multi-size catalog + doc:** `matmul_blocked_n128`, `matmul_blocked_n1024`, `matmul_naive_n128` in `catalog.toml`; [matmul scaling & huge GEMM](docs/numerics/matmul-scaling-and-huge-gemm.md) (BLIS blocking, Strassen, SUMMA, OOC); links from SOTA matrix + studies README; snapshot [benchmark-reports/2026-05-20-tier1-matmul-scaling.md](docs/benchmark-reports/2026-05-20-tier1-matmul-scaling.md).
- **SOTA / simulation rubric:** [docs/numerics/sota-comparison-matrix.md](docs/numerics/sota-comparison-matrix.md) — stability, wall time at small/large scale, memory, long horizons; maps tiers to comparators; honest gap list vs dashboard-only claims (cross-linked from handbook, methodology, honesty labels, game-dev map, plan cross-links, AGENTS).
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
