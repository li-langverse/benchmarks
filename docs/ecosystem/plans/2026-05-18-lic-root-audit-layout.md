# LIC_ROOT layout for plan-completion-audit and CI (PH-5b / REQ-bench-audit)

> **Issues:** [benchmarks#20](https://github.com/li-langverse/benchmarks/issues/20), [#25](https://github.com/li-langverse/benchmarks/issues/25), [#28](https://github.com/li-langverse/benchmarks/issues/28), [#29](https://github.com/li-langverse/benchmarks/issues/29)  
> **Repo:** li-langverse/benchmarks  
> **Vision:** **Provable** (honest catalog gaps), **AI-first** (agents get consistent preflight)  
> **Learned from:** [plan-cross-links.md](../plan-cross-links.md), [tooling-catalog.md](../tooling-catalog.md), `scripts/plan-completion-audit.py`, [engineering-standards](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md)

## Goal

Make `plan-completion-audit.py`, `agent-briefing.py`, and GitHub Actions resolve the **same** compiler checkout (`LIC_ROOT`) so `catalog_gaps` and `catalog_without_lic_path` findings are real—not false positives when a sibling `lic` tree is missing or named `li`.

## Non-goals

- Copying benchmark harness into **benchmarks** (harness stays under **lic** per ecosystem-first).
- Weakening `threshold_ratio_cpp` or marking catalog rows green without harness paths.
- Adding `schedule:` cron to workflows.

## Dependencies

- **PH-5b** — benchmark harness ownership in **lic**.
- Human: org clone layout docs (monorepo vs sibling repos) in **roadmap** if policy changes.

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | Document canonical `LIC_ROOT` resolution order in `docs/ecosystem/plan-cross-links.md` + `SETUP_GITHUB.md` | Table: env → `../lic` → `../li` (first existing dir) |
| B | `plan-completion-audit.py`: resolve LIC with shared helper; emit `lic_root_resolved`, `lic_present` in JSON | No `catalog_gaps` when resolved tree has paths |
| C | `agent-briefing.py` / `agent-preflight.sh`: same resolver; skip plan_audit with explicit reason when `lic_present: false` | Briefing shows skip reason, not silent empty audit |
| D | Align workflow env: `ci.yml` uses `${{ github.workspace }}/lic`; dispatch workflows use relative `lic` after checkout | `workflow_dispatch` audit matches PR CI layout |
| E | Optional: `scripts/resolve-lic-root.sh` sourced by ingest + audit scripts | Single source in tooling-catalog |

## Tests / benches

- `python3 scripts/plan-completion-audit.py` with `LIC_ROOT=../li` and `LIC_ROOT=../lic` (whichever exists).
- CI `ingest-smoke` job (existing) — no regression.
- Catalog path check: only rows with `repo = "lic"` validated under resolved root.

## Provability

- **G-math** — unchanged; audit honesty improves (fewer false catalog debt rows).
- Do not mark **G-*** rows Done from this work alone.

## Rollout

1. Implementation PR on **benchmarks** (after `plan-approved`).
2. Close #20–#29 when JSON shows `lic_present: true` on dispatch + local preflight docs updated.
3. Remove `plan-needed` on linked issues; maintainer adds `plan-approved`.

## Human-only

- None for implementation; maintainer must label **`plan-approved`** before code agents run.
