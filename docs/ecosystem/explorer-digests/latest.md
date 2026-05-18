# Implementation gaps digest — 2026-05-19

**Agent:** `implementation_gaps` · **Heap:** `coord_governance`  
**Full digest:** [2026-05-19-gaps.md](./2026-05-19-gaps.md)

---

## Executive summary

- **127** plan-audit findings (`LIC_ROOT=../lic`): 8 partial master-plan rows, 96 open sub-plan checkboxes, 12+4 **G-*** gaps, 1 catalog gap (`tier0_stability`).
- **P0:** lic#47 / #40 duplicate horner PRs (CI red); lic#48 bench improver failing.
- **P1:** `horner_pure_li` **~88.8×** cpp (PH-5b, PH-7e) — numerics + codegen, not catalog.
- **P1:** PH-IO std modules missing — lic#13.
- **P1:** Physics scaffolds + 12 packages without org mirrors — lic#14, **lic#50** (new).
- **Next week:** numerics_research → pr_alignment → issue_planner (PH-IO).

See [2026-05-19-gaps.md](./2026-05-19-gaps.md) for plan debt table, web spot-check, and PR queue.
