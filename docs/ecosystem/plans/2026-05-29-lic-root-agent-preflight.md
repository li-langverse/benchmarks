# LIC_ROOT agent preflight honesty (PH-IO / REQ-BENCH-AUDIT-1)

> **Issues:** [#20](https://github.com/li-langverse/benchmarks/issues/20), [#25](https://github.com/li-langverse/benchmarks/issues/25), [#28](https://github.com/li-langverse/benchmarks/issues/28), [#29](https://github.com/li-langverse/benchmarks/issues/29), [#54](https://github.com/li-langverse/benchmarks/issues/54) · **Repo:** li-langverse/benchmarks  
> **Vision:** **easy**, **ai-first** (trustworthy agent signals) · **Learned from:** [engineering-standards](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md), [plan-cross-links](../plan-cross-links.md), [release-notes/2026-05-25-lic-root-catalog-alignment.md](../release-notes/2026-05-25-lic-root-catalog-alignment.md), merged PR [#86](https://github.com/li-langverse/benchmarks/pull/86)

## Goal

Ensure `plan-completion-audit.py`, `ecosystem-explorer.py`, and agent preflight never report phantom catalog or std-module debt when the **lic** sibling checkout is missing. CI and cloud agents must set `LIC_ROOT` deterministically; explorers must surface **`scan_degraded`** instead of empty `std_modules_on_disk`.

## Non-goals

- Changing `threshold_ratio_cpp` or bench pass criteria.
- Copying `lic/benchmarks/harness` into **benchmarks**.
- New org repos or governance policy edits (human merge on **roadmap**).

## Dependencies

| ID | Owner | Notes |
|----|-------|-------|
| **PH-IO** | lic + benchmarks | Accurate ingest/explorer signals |
| **PH-5b** | lic | Harness paths under `LIC_ROOT/benchmarks/` |
| CI checkout | benchmarks | `lic@dev` beside workspace — **done** on `main` (`.github/workflows/ci.yml`, `plan-completion-audit.yml`, `ecosystem-explorer.yml`, `benchmark-nightly.yml`) |

## Current state (2026-05-29)

- With `LIC_ROOT=../lic`: `catalog_gaps = 0` (plan-completion-audit).
- PR **#86** merged: multi-root audit, `catalog_lifecycle=planned` skip, tier-0 path fix.
- **Gap:** `ecosystem-explorer.json` can still show `lic_present: false` in cloud VMs without sibling **lic**; issues #25–#29 duplicate the same CI fix.

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | Confirm all GHA jobs that run audit/explorer/ingest check out `li-langverse/lic@dev` and export `LIC_ROOT=${{ github.workspace }}/lic` | `rg LIC_ROOT .github/workflows` — no job runs audit without lic |
| B | `ecosystem-explorer.py`: add `scan_degraded: true` + `degraded_reason` when `lic_present` is false; digest banner | Explorer JSON + digest show degraded, not “all std missing” |
| C | `scripts/update-cloud-agent-env.sh`: export `LIC_ROOT=$REPOS_ROOT/lic` in completion log / optional `~/.profile.d/li-langverse.sh` snippet for Cloud Agent | Cloud preflight `lic_present: true` after install script |
| D | `scripts/agent-briefing.py`: propagate `scan_degraded` into briefing JSON | Briefing lists degraded scan, suppresses false P1 “21 catalog gaps” |
| E | Close #20, #25, #28, #29 as duplicate of #54 umbrella after B–D land; remove `plan-needed` | Maintainer adds `plan-approved` |

## Tests / benches

- `LIC_ROOT=../lic python3 scripts/plan-completion-audit.py` → `catalog_gaps == 0`
- `LIC_ROOT=../lic python3 scripts/ecosystem-explorer.py` → `lic_present: true`, `scan_degraded: false`
- `LIC_ROOT=/nonexistent python3 scripts/ecosystem-explorer.py` → `scan_degraded: true`, no false `missing_std_modules` count in agent actions
- No new tier-1 bench rows (catalog-only honesty).

## Provability

- **G-meta** — unchanged; audit is filesystem read-only.
- Honesty: agent digests must not claim “implement 21 benches” when paths are unresolvable.

## Rollout

1. Implementation PR (benchmarks): explorer + cloud env + briefing (sub-phases B–D).
2. Issue comments linking this plan; maintainer `plan-approved` + remove `plan-needed`.
3. Optional: `workflow_dispatch` plan-audit artifact commit on `main` (no new `schedule:` cron).

## Human-only

- None for implementation; maintainer label `plan-approved` before `code_implementer` agents run.
