# Numerics researcher digest — 2026-05-17

**Agent:** `numerics_researcher`  
**Skill:** `research-li-numerics`  
**Preflight:** ecosystem-audit + benchmark-failures-report (2026-05-17)  
**Dashboard:** https://li-langverse.github.io/benchmarks/

---

## Executive summary

- **One red row:** `horner_pure_li` at **88.82×** cpp — pure-Li float `while` loop; oracle C is ~100× faster at same `-O3`/fast-math semantics.
- **Root cause (SOTA):** not wrong Horner math — **PH-7e / release codegen** gap (interpreter or immature LLVM lowering vs `horner_core.c` FMA loop).
- **Mode A verdict:** adopt standard Horner + FMA + light unroll per NR / LLVM practice; **no novel algorithm** (autoresearch not required).
- **Seven near-threshold rows** (1.003–1.035× cpp) use **shared C kernels** via `LI_EXTRA_C`; fix path is PH-5b link/LTO/FFI parity, not new integrators.
- **Studies written:** `docs/numerics/studies/2026-05-17-horner-pure-li-ph7e.md`, `docs/numerics/studies/2026-05-17-near-threshold-tier12.md`.
- **G-math / G-par:** horner → **G-math** float pipeline + phase **7e**; near-threshold → **PH-5b** until pure-Li physics kernels ship.
- **Do not:** weaken `threshold_ratio_cpp`, ship `sorry`/`unsafe`, or tune catalog to greenwash.
- **gh blocked:** not logged in — issue bodies below for manual `gh issue create` or CI bot.

---

## Mode & targets

| Mode | Targets |
|------|---------|
| **A — SOTA survey** | `horner_pure_li` (red); near-threshold cluster |
| **B — Autoresearch** | Deferred — no SOTA gap for red row |

---

## Recommended issues / PRs

### Issues (file on **lic** with label `numerics-research`)

1. **lic:** `[numerics-research] PH-7e: horner_pure_li pure-Li loop → FMA LLVM (88× → ≤1.2× cpp)`  
   - Body: link study `benchmarks/docs/numerics/studies/2026-05-17-horner-pure-li-ph7e.md` (after benchmarks PR lands) or paste Learned from table  
   - Labels: `numerics-research`, `PH-7e`, `G-math`

2. **lic:** `[numerics-research] PH-5b: near-threshold LI_EXTRA_C link parity (7 benches >1.0× cpp)`  
   - Body: link `2026-05-17-near-threshold-tier12.md`  
   - Labels: `numerics-research`, `PH-5b`

### PRs (coordinate with bench_improver — do not open until codegen path confirmed)

| Repo | Title | Owner |
|------|-------|-------|
| **lic** | `perf(codegen): PH-7e — lower horner_pure_li float loop to FMA LLVM` | bench_improver + compiler |
| **lic** | `perf(bench): PH-5b — align LI_EXTRA_C release/LTO with cpp oracle` | bench_improver |
| **benchmarks** | `docs(numerics): studies for horner PH-7e + near-threshold cluster` | this pass |

**No lic implementation PR** from numerics_researcher until PH-7e lowering is scoped in compiler (proof path documented in study).

---

## Learned from (horner — quick reference)

1. Numerical Recipes Ch. 5 — Horner recurrence semantics  
2. Golub & Van Loan + LLVM `fmuladd` — FMA-shaped inner loop  
3. [Breese 2022](https://breese.github.io/2022/08/21/evaluating-polynomials.html) / [Herumi FMA](https://zenn.dev/herumi/articles/poly-evaluation-by-fma?locale=en) — latency-bound scalar Horner; FMA + unroll  
4. Eigen / BLIS micro-kernel isolation — hot loop must compile to native code, not dispatch

---

## Evidence commands

```bash
cd benchmarks && ./scripts/benchmark-failures-report.sh

cd lic/benchmarks/harness
python3 bench.py --tier 1 --bench horner_pure_li --runs 5

cd benchmarks
LIC_ROOT=../li ./scripts/ingest/ingest-lic.sh
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/2026-05-17-horner-pure-li-ph7e.md
```

---

## Deferred items

| Item | Reason |
|------|--------|
| **autoresearch** on horner | SOTA FMA lowering sufficient |
| **lic PR** | Await compiler 7e scoping; coordinate bench_improver |
| **GitHub issue create** | `gh` not authenticated in agent env |
| **37 catalog path gaps** | lic checkout path / implementation_gaps — separate agent |
| **Agent-kit sync** | platform coordinator, not numerics |
| **FFT micro-bench** | explorer P2 — no red row yet |
| **Threshold / catalog edits** | explicitly forbidden |

---

## Issue template (copy for `gh issue create -R li-langverse/lic`)

```markdown
## Summary
[numerics-research] PH-7e: Close `horner_pure_li` red row (88.82× cpp → ≤1.2×).

## Evidence
- Dashboard: https://li-langverse.github.io/benchmarks/
- Study: li-langverse/benchmarks `docs/numerics/studies/2026-05-17-horner-pure-li-ph7e.md`
- Pure-Li source: `benchmarks/tier1_micro/horner_pure_li/li/main.li`
- Oracle: `common/horner_core.c`

## SOTA (Learned from)
1. NR Ch.5 Horner — same recurrence as oracle
2. GVL + LLVM fmuladd — FMA inner loop
3. Breese/Herumi — FMA latency + modest unroll (not Estrin for scalar bench)
4. Eigen/BLIS — compile hot loop to native LLVM, not interpreter

## Implementation (lic)
- [ ] Release `lic build` for `li_pure` harness path
- [ ] Lower `while` + float `*`/`+` to FMA LLVM with fast-math parity
- [ ] `--verify` checksum vs cpp
- [ ] `bench.py --bench horner_pure_li`; ingest; ratio ≤ 1.2

## Tracks
PH-7e, G-math, PH-5b (harness)

## Do not
- Weaken `threshold_ratio_cpp`
- `sorry` / `unsafe` for speed
```

Labels: `numerics-research`
