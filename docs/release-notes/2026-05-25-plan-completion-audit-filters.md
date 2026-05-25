# Release notes: Plan completion audit false-positive filters

## Summary

`plan-completion-audit.py` now reads only the master-plan phase tracker for `master_plan_open`, suppresses stale sub-plan checkboxes when tracker phases are `[x]`, and tags phase-02 implementation task bullets separately from exit gates.

## Agent continuation

1. **Read** `data/latest/plan-completion-audit.json` — use `summary.open_plan_checkboxes` + `master_plan_open` for P1 work; `stale_spec_checklists` is P3 hygiene only.
2. **Run** `python3 scripts/plan-completion-audit.py` with `LIC_ROOT=../lic` after plan edits.
3. **Then** close or check off sub-plan exit gates in **lic** when tracker phase is `[x]` but exit-gate boxes remain (e.g. `phase-02-typechecker.md`).
4. **Blocked on** editing lic master-plan tracker rows from benchmarks agents (human/lic PR only).

## Changed

- `.github/workflows/ci.yml`, `scripts/setup-lic-for-bench.sh` — LLVM **22** (align with lic `scripts/ci-install-llvm.sh` pin; fixes `ingest-smoke` lic build on PR CI)
- `scripts/plan-completion-audit.py` — tracker section parse, `PLAN_FILE_COVERED_PHASES`, dedupe, `stale_spec_checklists`, `plan_files_suppressed`
- `data/latest/plan-completion-audit.json` — additive `summary` keys (`plan_checkboxes_suppressed`, `stale_spec_checklists`, `tracker_phases_complete`)
- `.cursor/skills/audit-plan-completion/SKILL.md` — interpret new fields

## Not changed

- `lic` master plan or sub-plan markdown (no checkbox edits in this PR)
- `provability-gaps.md` scanning logic
- `catalog.toml` rows or ingest pipelines
- li-cursor-agents supervisor heap

## Breaking

N/A — existing JSON keys unchanged; new arrays/fields are additive. Automations that assumed `open_plan_checkboxes` included all `- [ ]` in `docs/superpowers/plans/` should read `stale_spec_checklists` for hygiene-only rows.

## Security

N/A — read-only filesystem scan under `LIC_ROOT`.

## Performance

N/A — same single-pass markdown scan; capped list sizes preserved.

## Downstream

- **lic (optional):** check off phase-00/03/04 exit gates or archive task lists in a docs-only PR.
- **agent-briefing:** consumes updated JSON on next preflight; no code change required.
