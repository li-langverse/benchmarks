# Issue feature planner digest — 2026-05-29 (pass 2)

**Agent:** `issue_planner` · **Repo focus:** `li-langverse/benchmarks` (org sweep: 6 repos)  
**Pass:** 2026-05-29T22:39Z · **Skill:** `plan-feature-from-issue`  
**north_star_fit:** Scientific/HPC benchmark honesty · PH-IO, PH-5b · proof → easy → fast (harness in **lic**, catalog/ingest in **benchmarks**)

---

## Executive summary

- Scanned **6** repos via `issue-feature-triage.py`: **30** `needs_plan`, **3** candidates (all on **lic**).
- **benchmarks:** **10** `needs_plan`, **0** candidates — **3** draft plan PRs open (**#135–#137**); no new implementation (no `plan-approved`).
- Refreshed **PR #135** plan for post-**#130** reality: **117** `catalog_gaps` are catalog `repo=lic` drift, not missing harness on disk.
- **LIC_ROOT** cluster (#20, #25, #28, #29, #54) → umbrella plan PR **#135**; sub-phase **F** added for catalog path migration (#29).
- **#18** tier-1 FFT → plan PR **#136**; **#53** PH-IO-7 summary parity → plan PR **#137** — issue comments already posted.
- **Deferred #19** — harness dirs exist on **lic**; debt is catalog lifecycle / path sync, not greenfield stubs.
- **proof_gap_researcher** handoff: **G-par** / **G-dec** decorator-for policy bypass (cycles 7–8) aligns with **lic#387** / PH-7d.
- **Blocked:** maintainer must add `plan-approved` before `code_implementer`; do not self-merge planning PRs.

---

## Deliverable / findings

### Issues scanned

| Repo | Open feature/plan issues | Action this pass |
|------|--------------------------|------------------|
| **benchmarks** | 10 `needs_plan` | 3 plans (PRs #135–137); plan refresh on #135; defer #19; link #51/#52 → #18 |
| **lic** | 20 `needs_plan` + 3 candidates | Out of repo scope — **lic** planner pass (**#387**, **#386**, **#424**, …) |
| lip, lit | 0 | — |
| lis, roadmap | gh empty/error | — |

Triage artifact: `data/latest/issue-feature-triage.json` (`generated_at` 2026-05-29T22:39Z).

### Plans drafted (benchmarks)

| Issue(s) | Plan path | Draft PR |
|----------|-----------|----------|
| #20, #25, #28, #29, #54 | `docs/ecosystem/plans/2026-05-29-lic-root-agent-preflight.md` | https://github.com/li-langverse/benchmarks/pull/135 |
| #18 (+ rubric #51, #52) | `docs/ecosystem/plans/2026-05-29-tier1-fft-microbench-ph5b.md` | https://github.com/li-langverse/benchmarks/pull/136 |
| #53 | `docs/ecosystem/plans/2026-05-29-ph-io-7-summary-parity-gate.md` | https://github.com/li-langverse/benchmarks/pull/137 |

**Traceability:** REQ-BENCH-AUDIT-1 · PH-IO / PH-IO-7 · PH-5b (FFT tier-1) · G-math (vendor crossover rubric, catalog-only).

**Plan refresh (this pass):** PR **#135** “Current state” corrected — after merged **#130**, workloads live at `benchmarks/workloads/` but catalog still points at `lic/benchmarks/tier*`. Sub-phase **F/G** covers #29 migration.

### Issues blocked / deferred

| Issue | Disposition | Reason |
|-------|-------------|--------|
| **#19** | **Defer** | Harness present on **lic**; catalog sync / `planned` lifecycle only |
| **#51**, **#52** | **Linked** to #18 | Explorer SOTA refs; numerics research after CPU FFTW row |
| **lic** needs_plan (20+) | **Other repo** | Language/compiler plans → **lic** `docs/superpowers/plans/` |
| All draft plans | **Human-only** | Add `plan-approved`; remove `plan-needed` after PR merge |

### proof_gap_researcher handoff (provability_holes · priority 9)

| Priority | G-* / PH | lic issue | Research angle |
|----------|----------|-----------|----------------|
| P0 | **G-par**, **G-dec** | [#387](https://github.com/li-langverse/lic/issues/387) | `@parallel` / `@vectorized` on plain `for`; decorator-for policy bypass (research cycles 7–8) |
| P1 | **G-vc** / P-float | master plan **2f** | `sqrt_open_bound` — contract tier vs Lean |
| P1 | **G-math** | [#386](https://github.com/li-langverse/lic/issues/386) | PH-2i tracker vs shipped length-1 broadcast |
| P2 | **G-meta** | — | Compiler ↔ Lean equivalence limits (document only in benchmarks agents) |

**Sources:** [provability-gaps.md](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) · `data/latest/plan-completion-audit.json` (13 partial, 4 missing G-*) · [implementation-gaps digest](../docs/ecosystem/explorer-digests/2026-05-29-gaps.md).

**Do not:** lower `threshold_ratio_cpp`; copy harness into **benchmarks**; edit `trusted.lean` without human-approved issue.

---

## Recommended issues/PRs

| Item | Repo | Labels / notes |
|------|------|----------------|
| **Review:** LIC_ROOT + catalog migration plan | benchmarks | PR **#135** · #20,#25,#28,#29,#54 |
| **Review:** tier-1 FFT PH-5b plan | benchmarks | PR **#136** · `feature`, `plan-needed` on **#18** |
| **Review:** PH-IO-7 summary parity plan | benchmarks | PR **#137** · `explorer-finding`, `plan-needed` on **#53** |
| PH-7d / G-par MIR + Lean disjoint proofs | lic | **#387** · `master-plan-gap`, `plan-needed` |
| PH-2i tracker reconciliation | lic | **#386** · `master-plan-gap`, `plan-needed` |
| Catalog `repo`/`path` migration | benchmarks | **#29** · sub-phase F of PR **#135** plan |
| std.summary / PH-IO | lic | **#13** (ingest native path) |

---

## Deferred

- **#19** — tier-2 gaming catalog sync; harness on disk, catalog lifecycle debt only.
- **Explorer rubrics** (#51, #52, tier-5 HTTP unknowns) — wait on parent `plan-approved` / numerics_researcher.
- **lic** explorer-finding backlog (Kokkos, OpenMP, PETSc) — **lic** issue_planner pass.
- **Roadmap / lis** — no issues returned (gh empty or auth).
- **Implementation** — blocked until `plan-approved` + merged plan doc on each parent issue.

---

## Errors

None fatal this pass. Triage and plan-completion-audit succeeded with local `LIC_ROOT=../lic`.
