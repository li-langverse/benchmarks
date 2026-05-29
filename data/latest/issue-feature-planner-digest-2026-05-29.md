# Issue feature planner digest — 2026-05-29

**Agent:** `issue_planner` · **Repo focus:** `li-langverse/benchmarks` (org sweep: 6 repos)  
**Pass:** 2026-05-29T15:39Z · **Skill:** `plan-feature-from-issue`  
**north_star_fit:** Scientific/HPC benchmark honesty · PH-IO, PH-5b · proof → easy → fast (harness in **lic**, catalog/ingest in **benchmarks**)

---

## Executive summary

- Scanned **6** repos via `issue-feature-triage.py`: **24** `needs_plan`, **3** candidates (all on **lic**).
- **benchmarks:** **10** `needs_plan`, **0** candidates — **3** feature plans already drafted today (draft PRs **#135–#137**); no new implementation (no `plan-approved`).
- Confirmed **LIC_ROOT** cluster (#20, #25, #28, #29, #54) → single plan + PR **#135**; issue comments already posted.
- **#18** tier-1 FFT → plan + PR **#136**; **#53** PH-IO-7 summary parity → plan + PR **#137**.
- **Deferred #19** — tier-2 gaming rows (`euler_fluid_2d`, `combustion_passive`, `wind_field_bc`) now exist under `lic/benchmarks/tier2_physics/`; real debt is **catalog path migration** (117 gaps), not re-filed harness stubs.
- Linked explorer rubrics **#51**, **#52** to **#18** / PR **#136** (no separate plan PR).
- **proof_gap_researcher** handoff: prioritize **G-par**, **G-dec**, **G-vc** (`sqrt_open_bound`) aligned with **lic#387**, **lic#386**, master-plan phases **7d** / **2i**.
- **Blocked:** maintainer must add `plan-approved` on parent issues before `code_implementer`; do not self-merge planning PRs.
- Org **gh** rate limit hit during `ensure-org-repo-ci.py` (403) — does not block benchmarks planning.

---

## Deliverable / findings

### Issues scanned

| Repo | Open feature/plan issues | Action this pass |
|------|--------------------------|------------------|
| **benchmarks** | 10 `needs_plan` | 3 plans (existing PRs); 1 defer (#19); 2 link-only (#51, #52) |
| **lic** | 14 `needs_plan` + 3 candidates | Out of repo scope — **lic** planner pass / **lic#387–385** |
| lip, lit | 0 | — |
| lis, roadmap | gh empty/error | — |

Triage artifact: `data/latest/issue-feature-triage.json` (`generated_at` 2026-05-29T15:29Z).

### Plans drafted (benchmarks)

| Issue(s) | Plan path | Draft PR |
|----------|-----------|----------|
| #20, #25, #28, #29, #54 | `docs/ecosystem/plans/2026-05-29-lic-root-agent-preflight.md` | https://github.com/li-langverse/benchmarks/pull/135 |
| #18 (+ rubric #51, #52) | `docs/ecosystem/plans/2026-05-29-tier1-fft-microbench-ph5b.md` | https://github.com/li-langverse/benchmarks/pull/136 |
| #53 | `docs/ecosystem/plans/2026-05-29-ph-io-7-summary-parity-gate.md` | https://github.com/li-langverse/benchmarks/pull/137 |

**Traceability:** REQ-BENCH-AUDIT-1 (LIC_ROOT honesty) · PH-IO / PH-IO-7 · PH-5b (FFT tier-1) · G-math (vendor crossover rubric, catalog-only).

**Harness rule:** FFT and tier-2 physics kernels stay in **lic**; **benchmarks** owns `catalog.toml`, ingest, dashboard, audit scripts.

### Issues blocked / deferred

| Issue | Disposition | Reason |
|-------|-------------|--------|
| **#19** | **Defer / close** | Harness dirs present on `lic@dev`; original audit stale |
| **#51**, **#52** | **Linked** to #18 | Explorer SOTA refs; single implementation plan |
| **lic** needs_plan (14+) | **Other repo** | Language/compiler plans belong in **lic** (`docs/superpowers/plans/`) |
| All draft plans | **Human-only** | Add `plan-approved`; remove `plan-needed` after PR merge |

### proof_gap_researcher handoff (provability_holes · priority 9)

Research goal: close honest **G-*** holes without weakening benches or claiming **Done** without Lean evidence.

| Priority | G-* / PH | lic issue | Research angle |
|----------|----------|-----------|----------------|
| P0 | **G-par**, **G-dec** | [#387](https://github.com/li-langverse/lic/issues/387) | MIR proc tags; `@parallel` on plain `for` policy bypass (`parallel_decorator_policy_capture_gap.sh`) |
| P1 | **G-vc** / P-float | master plan **2f** | `sqrt_open_bound` — `Float.abs` Prop, `sqrt_open_bound_contract_tier.sh` |
| P1 | **G-math** | [#386](https://github.com/li-langverse/lic/issues/386) | PH-2i tracker vs shipped length-1 broadcast + reductions |
| P2 | **G-meta** | — | Compiler ↔ Lean equivalence (document limits only in benchmarks agents) |

**Sources:** [provability-gaps.md](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) · `data/latest/plan-completion-audit.json` (13 partial, 4 missing G-*) · [implementation-gaps digest](./explorer-digests/2026-05-29-gaps.md) (sibling pass).

**Do not:** lower `threshold_ratio_cpp`; copy harness into **benchmarks**; edit `trusted.lean` without human-approved issue.

---

## Recommended issues/PRs

| Item | Repo | Labels / notes |
|------|------|----------------|
| **Merge review:** LIC_ROOT agent preflight plan | benchmarks | PR **#135** · `plan-needed` on #20,#25,#28,#29,#54 |
| **Merge review:** tier-1 FFT PH-5b plan | benchmarks | PR **#136** · `feature`, `plan-needed` on **#18** |
| **Merge review:** PH-IO-7 summary parity plan | benchmarks | PR **#137** · `explorer-finding`, `plan-needed` on **#53** |
| PH-7d / G-par MIR + Lean disjoint proofs | lic | **#387** · `master-plan-gap`, `plan-needed` |
| PH-2i tracker reconciliation | lic | **#386** · `master-plan-gap`, `plan-needed` |
| Catalog harness migration | lic | **#378** PR (CI red) — 117 catalog path gaps |
| std.summary / PH-IO | lic | **#13** (ingest native path) |

---

## Deferred

- **#19** — tier-2 gaming catalog ahead of **lic** tree (**resolved** on disk; close after maintainer ack).
- **Explorer-only** benchmarks issues without new capability (#51, #52) — wait on **#18** `plan-approved`.
- **lic** explorer-finding backlog (Kokkos, OpenMP, PETSc rubrics) — **lic** issue_planner pass; not benchmarks-owned.
- **Roadmap / lis** — no issues returned (gh empty or auth).
- **Implementation** — blocked until `plan-approved` + merged plan doc on each parent issue.

---

## Errors

None fatal. Preflight noted **org-ci-audit** `gh` API rate limit (HTTP 403) during `ensure-org-repo-ci.py`; triage and plan-completion-audit succeeded with local `LIC_ROOT=../lic`.
