# Plan-completion-audit LIC_ROOT CI honesty (#20)

> **Issue:** [benchmarks#20](https://github.com/li-langverse/benchmarks/issues/20)  
> **Related:** [#25](https://github.com/li-langverse/benchmarks/issues/25), [#28](https://github.com/li-langverse/benchmarks/issues/28), [#54](https://github.com/li-langverse/benchmarks/issues/54), [#266](https://github.com/li-langverse/benchmarks/issues/266)  
> **Repo:** li-langverse/benchmarks  
> **Vision:** **Provable** (honest audit signals), **AI-first** (agents trust preflight JSON)  
> **North star fit:** Ecosystem agent infrastructure — **PH-IO** (accurate ingest/explorer signals), not compiler proof surface  
> **Learned from:** [engineering-standards](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md), [2026-05-18-lic-root-audit-layout.md](./2026-05-18-lic-root-audit-layout.md), [2026-05-25-lic-root-catalog-alignment.md](../release-notes/2026-05-25-lic-root-catalog-alignment.md), merged PR [#86](https://github.com/li-langverse/benchmarks/pull/86)

## Goal

Ensure `plan-completion-audit.py`, `ecosystem-explorer.py`, and `agent-briefing.py` never report phantom master-plan or catalog debt when the **lic** checkout is missing. GitHub Actions must checkout `li-langverse/lic@dev` and export `LIC_ROOT` deterministically; local and cloud agents must surface **`scan_degraded`** instead of empty or inflated gap counts.

## Non-goals

- Weakening `threshold_ratio_cpp` or bench pass criteria.
- Copying harness into **benchmarks** (workloads live under `benchmarks/workloads/`; execution stays lic-driven).
- Adding `schedule:` cron to workflows ([actions-budget](../actions-budget.md)).
- Resolving catalog migration drift (#266) — tracked separately; this plan enables honest counts once paths are fixed.

## Current state (2026-06-07)

| Acceptance criterion (#20) | Status |
|----------------------------|--------|
| GHA checks out `lic@dev` beside benchmarks | **Done** — `plan-completion-audit.yml`, `ecosystem-audit.yml`, `ci.yml`, `ecosystem-explorer.yml`, `benchmark-nightly.yml`, `ingest.yml` |
| Export `LIC_ROOT` before audit scripts | **Done** in CI (`${{ github.workspace }}/lic`) |
| Document in workflow comment / briefing preflight | **Partial** — `agent-briefing.py` note exists; explorer lacks `scan_degraded`; cloud script omits `LIC_ROOT` export |

**Evidence (issue body):** Without sibling `../lic`, audit reported 21 false `catalog_gaps` + missing master plan file; with shallow `lic@dev` clone, counts drop to 7 open tracker items, 6 real catalog gaps, 12+4 G-* partial/missing.

**Remaining gaps:**

- **Gap A:** `ecosystem-explorer.py` sets `lic_present: false` but does not emit `scan_degraded` — agents interpret empty `std_modules_on_disk` as real debt (#54).
- **Gap B:** `scripts/update-cloud-agent-env.sh` clones/builds **lic** but never exports `LIC_ROOT` for subsequent agent sessions.
- **Gap C:** `agent-briefing.py` does not propagate degraded scan into `recommended_agents` — phantom P1 “implement 21 benches” actions persist locally.

## Dependencies

| ID | Owner | Notes |
|----|-------|-------|
| **PH-IO** | lic + benchmarks | Accurate ingest/explorer/agent signals |
| **REQ-BENCH-AUDIT-1** | benchmarks | Catalog audit honesty (no phantom gaps) |
| **PH-5b** | lic | Harness paths; catalog migration (#266) is follow-on |
| CI checkout | benchmarks | **Complete** on `main` since PR #86 |

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | Confirm all GHA jobs running audit/explorer/ingest checkout `lic@dev` + `LIC_ROOT` | `rg 'LIC_ROOT\|checkout.*lic' .github/workflows` — zero audit jobs without lic (**done**) |
| B | `ecosystem-explorer.py`: add `scan_degraded: true` + `degraded_reason` when `lic_present` is false; digest banner | Explorer JSON shows degraded, not “all std missing” |
| C | `scripts/update-cloud-agent-env.sh`: export `LIC_ROOT=$REPOS_ROOT/lic`; optional `~/.profile.d/li-langverse.sh` snippet | Cloud preflight `lic_present: true` after install |
| D | `scripts/agent-briefing.py`: propagate `scan_degraded`; suppress false P1 catalog-gap recommendations when degraded | Briefing JSON lists degraded scan with explicit skip reason |
| E | Workflow header comments on `plan-completion-audit.yml` + `ecosystem-audit.yml`: note `LIC_ROOT` requirement for local runs | Maintainer-visible; matches `agent-briefing.py` note |
| F | Close #20, #25, #28 when B–E land; umbrella #54 closes when cloud + explorer honest | Maintainer adds **`plan-approved`**, removes **`plan-needed`** |

## Tests / benches

- `LIC_ROOT=../lic python3 scripts/plan-completion-audit.py` → honest `catalog_gaps` (not inflated by missing tree).
- `LIC_ROOT=../lic python3 scripts/ecosystem-explorer.py` → `lic_present: true`, `scan_degraded: false`.
- `LIC_ROOT=/nonexistent python3 scripts/ecosystem-explorer.py` → `scan_degraded: true`, `degraded_reason` set; no false `missing_std_modules` in recommended actions.
- `python3 scripts/agent-briefing.py --skip-slow` with and without sibling lic — degraded path documented in JSON.
- No new tier-1 bench rows; no gate weakening.

## Provability / G-* mapping

| Gap | Impact |
|-----|--------|
| **G-meta** | Unchanged — audit remains filesystem read-only |
| **G-math** / **G-lean** | Unchanged — no compiler or proof edits |
| Honesty | Agent digests must not claim “implement N benches” when `LIC_ROOT` is unresolvable |

## Rollout

1. **This PR:** plan doc only (planning lane).
2. **Implementation PR** (after maintainer **`plan-approved`**): sub-phases B–E in one focused benchmarks PR.
3. Issue comments linking plan; close #20 when exit gates met.
4. Optional: `workflow_dispatch` plan-audit artifact commit on `main` (no new cron).

## Human-only

- Maintainer must add label **`plan-approved`** before `code_implementer` agents run.
- Do not self-merge governance or roadmap PRs.
