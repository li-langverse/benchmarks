# Agent instructions (`benchmarks`)

1. Read [roadmap: release-notes](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/release-notes.md) — **write before PR**.
2. **PR-only** — branch + PR; CI green; reviewer merges; do not self-merge.
3. Do **not** copy `lic/benchmarks/harness` into this repo (ingest only).
4. Update `catalog.toml` when adding benchmarks; run `./scripts/ingest/ingest-lic.sh` locally.
5. Dashboard: https://li-langverse.github.io/benchmarks/
6. `./scripts/sync-agent-kit.sh` after roadmap `agent-kit/` changes.

## Standing ops (every session)

1. Run `python3 scripts/ecosystem-audit.py` — failed PRs, missing `ci.yml` on `main`, missing live docs, benchmark reds vs [master plan PH-5b/PH-7e](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md).
2. Read `data/latest/ecosystem-audit.json` and `data/history/index.json` (`latest_deltas`) for time-resolved benchmark changes.
3. Align fixes to vision: P0 package CI → merge queue → lic compiler perf (pure-Li tier-1), not dashboard-only threshold tweaks.
4. If queue is healthy and benches are green, improve **lic** harness kernels (goal: Li ≤1.2× cpp everywhere; beat HPC SOTAs on tier-2 physics).

**Cursor Automations** (not Actions cron): see `.cursor/automations/` — **failed benchmarks** (`failed-benchmarks-maintainer.md`), ecosystem health, merge-queue digest. Report: `./scripts/benchmark-failures-report.sh`. Actions budget: `docs/ecosystem/actions-budget.md`.

Skills: `write-li-release-notes`, `li-ecosystem-discipline`.
