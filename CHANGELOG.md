# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Physics benchmark catalog rows for new `lic` Tier-2 kernels (`docs/release-notes/2026-05-16-physics-catalog-expansion.md`)
- Agent skill `research-li-numerics` (pointer to `lic`)
- Feature planner + plan completion audit automations, skills, and scripts (`docs/release-notes/2026-05-16-agent-automations-planning.md`)
- Ecosystem audit (`scripts/ecosystem-audit.py`) + Cursor Automation prompts (`.cursor/automations/`): failed benchmarks, **visual validation** (`render-benchmark-visuals.sh`, manifest + zip); Actions workflow **manual dispatch only** (no cron).
- Actions budget doc (`docs/ecosystem/actions-budget.md`).
- Benchmark history snapshots (`data/history/`, `scripts/record-benchmark-history.py`) with ratio deltas between ingests.
- Agent-kit sync and release-notes policy (roadmap v1.1.0).
