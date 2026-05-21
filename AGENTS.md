# Agent instructions (`benchmarks`)

**Philosophy:** [ecosystem-first](docs/ecosystem/ecosystem-first.md) — use [tooling-catalog](docs/ecosystem/tooling-catalog.md) before inventing tooling. If blocked, `python3 scripts/file-ecosystem-gap-issue.py` → labels `ecosystem-gap` + `plan-needed` for planner automations.

1. Read [handbook](docs/handbook/README.md) and [plan cross-links](docs/ecosystem/plan-cross-links.md); [provability gaps](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) before proof/perf claims.
2. Read [roadmap: release-notes](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/release-notes.md) — **write before PR**.
3. **PR-only** — branch + PR; **normal push only** ([git-workflow](docs/ecosystem/git-workflow.md)); CI green; **`merge-approved`** + gate for automated merge (see **merge-approved-pr** skill).
4. Do **not** copy `lic/benchmarks/harness` into this repo (ingest only).
5. Update `catalog.toml` when adding benchmarks; run `./scripts/ingest/ingest-lic.sh` locally.
6. Dashboard: https://li-langverse.github.io/benchmarks/ — perf labels: [benchmark-dashboard.md](docs/honesty/benchmark-dashboard.md)
7. `./scripts/sync-agent-kit.sh` after roadmap `agent-kit/` changes.

## Standing ops (every session)

1. After **any implementation** that touches perf, httpd, compiler, or physics kernels: run **`./scripts/run-full-benchmark-suite.sh`** (or `SKIP_BUILD=1` if already built); read **`data/latest/benchmark-matrix.md`** (full matrix), **`./scripts/benchmark-failures-report.sh`**, and `data/latest/summary.json`. For **httpd** changes: do **not** set `SKIP_EXPLOITS=1` on merge-worthy work — see [http-server-benchmark-growth.md](docs/ecosystem/http-server-benchmark-growth.md).
2. Run `python3 scripts/ecosystem-audit.py` — failed PRs, missing `ci.yml` on `main`, missing live docs, benchmark reds vs [master plan PH-5b/PH-7e](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md).
3. Read `data/latest/ecosystem-audit.json` and `data/history/index.json` (`latest_deltas`) for time-resolved benchmark changes.
4. Align fixes to vision: P0 package CI → merge queue → lic compiler perf (pure-Li tier-1), not dashboard-only threshold tweaks.
5. If queue is healthy and benches are green, improve **lic** harness kernels (goal: Li ≤1.2× cpp everywhere; beat HPC SOTAs on tier-2 physics).
6. On catalog miss or script failure → **file ecosystem-gap issue** (do not only patch locally).

**Full suite** (`LIC_ROOT=../lic`): tier-0 → tier-1/2 → tier-3 → tier-5 HTTP multi-oracle + supplemental proxy → **tier-5 exploits** → ingest → failures report → **`benchmark-matrix-report.py`** (always).

**Agent-first:** Intelligence (explorer, PR review/alignment, numerics SOTA, plan gaps) = **[Cursor Automations](https://cursor.com/automations)** + web search. Scripts only **preflight** JSON: `./scripts/agent-preflight.sh` → [cursor-agent-architecture.md](docs/ecosystem/cursor-agent-architecture.md).

**Cursor Automations** (not Actions cron): see `.cursor/automations/` and [docs/ecosystem/agent-automations.md](docs/ecosystem/agent-automations.md):

- **Issue feature planner** — vision-aligned plans from new issues (`plan-feature-from-issue` skill); includes **`ecosystem-gap`**
- **Plan completion audit** — stale PH phases, plan checkboxes, G-* gaps (`audit-plan-completion` skill)
- **PR auto-merge** — after `merge-approved` + `pr-merge-gate.py`
- Visual validation, failed benchmarks, ecosystem health, merge digest

Scripts (preflight for agents): `./scripts/agent-preflight.sh`, `./scripts/cursor-agent-run.sh` (→ **li-cursor-agents** + `@cursor/sdk`, `--mock` in CI), `./scripts/ecosystem-explorer.py`, `./scripts/plan-completion-audit.py`, `./scripts/run-pr-program.py`, `./scripts/pr-merge-gate.py`, … Actions budget: `docs/ecosystem/actions-budget.md` (CI/Pages only).

Skills: **`ecosystem-first`**, `plan-feature-from-issue`, `audit-plan-completion`, **`plan-merge-queue`**, **`resolve-merge-conflicts`**, `merge-approved-pr`, `write-li-release-notes`, `li-ecosystem-discipline`, **`research-li-numerics`**, **`numerics-autoresearch`** (novel algorithms). Methodology: [docs/numerics/research-methodology.md](docs/numerics/research-methodology.md).
