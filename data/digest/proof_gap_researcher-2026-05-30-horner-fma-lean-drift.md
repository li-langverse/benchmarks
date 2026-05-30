# Proof gap researcher — cycle 21 (Horner FMA codegen↔Lean drift; G-hw / G-meta)

**Run:** `proof_gap_researcher-2026-05-30-horner-fma-lean-drift` · **Date:** 2026-05-30  
**Goal:** `provability_holes` · **Focus:** **G-hw**, **G-meta**, **G-vc**, **G-math** · **PH-7e, PH-2f**  
**north_star_fit:** provable pillar — tier-1 `horner_pure_li` FMA lowering is perf-advisory only; no Lean loop≡ensures witness; `--numerically-stable` asymmetry vs matmul

## Executive summary

- **Focus:** Tier-1 Horner (`acc = acc * x + 1.0`, trip multiple of 64) lowers via `HornerStepPow4` + LLVM `fmuladd`; **no** `witness_horner*` in `vc_witness.cpp` and **no** horner eval lemma in `Discharge.lean`.
- **New harness:** `horner_fma_codegen_lean_drift.sh` + probe `horner_5m_fma_codegen_probe.li` — gates Lean witness absence and `--numerically-stable` FMA policy asymmetry vs IKJ matmul.
- **HYPOTHESIS verified:** Default release horner retains FMA chain (80 `vfmadd` in `main`, 98 insns) when trip = 5_000_000 (matches `horner_pure_li` bench).
- **HYPOTHESIS verified:** `--numerically-stable` still emits horner `fmuladd` (80 hits); matmul IKJ disables FMA under same flag (`emit.cpp:231-234` vs `HornerStepPow4` unconditional FMA at `:657-672`).
- **HYPOTHESIS falsified:** Short-trip probe (`i < 64`) with only `volatile_sink` on `acc` retains codegen — LLVM const-folds entire loop (~11 insns, 0 FMA).
- **Contrast:** Dot4 loop closed via `witness_dot4_int_loop` + `dot4_int_loop_eval_spec`; Horner has no analogous P-loop slice.
- **No `trusted.lean` edits.**
- **`publish_subdir`** not injected (`provability_holes` auxiliary goal).

## Deliverable / findings

### 1. Compiler / semantics gaps

- **G-math / G-meta:** `lower.cpp:2106-2165` recognizes Horner while (`trip ≥ 64`, `% 64 == 0`) and emits `HornerStepPow4` (const `x`) or `HornerFmaUnroll`; algebraically rewrites 64 scalar steps per iteration.
- **G-hw:** `HornerStepPow4` / `FmaFloatF64` always call `llvm.fmuladd` (`emit.cpp:632-672`) — hardware FMA semantics, not sequential `mul`+`add` in Lean `Float`.
- **G-meta:** Default release enables fast-math contract/reassoc on builder (`emit.cpp:1435-1442`); tier-1 horner certificate is codegen-bound, not Lean-equivalence (**G-meta Missing**).

### 2. Contract gaps

- Tier-1 `horner_pure_li` ≤1.2× C++ proves **FMA Horner codegen** performance, not `ensures` tying loop to closed-form polynomial spec.
- **Open:** `witness_horner_fma_loop` + `horner_loop_eval_spec` (P-loop / P-float) — no AutoVC linkage today.
- `@` matmul respects `--numerically-stable` FMA disable; Horner path does not — documented asymmetry for physics-grade builds.

### 3. Trusted surface

- No new axioms; gap is witness + semantic lemma backlog plus FP/fast-math policy honesty (**G-hw Axiomatic** row applies to FMA vs IEEE sequential).

### 4. External trust boundaries

- Human: decide whether `--numerically-stable` should disable Horner `fmuladd` (parity with matmul IKJ).
- Human: design horner loop witness predicate matching `HornerStepPow4` / scalar `acc = acc*x+c` steps before P-float closure.
- Human: tier-1 horner advisory certificate remains valid only while codegen path is unchanged.

### 5. Evidence pack

| Command | Outcome |
|---------|---------|
| `bash li-tests/tooling/horner_fma_codegen_lean_drift.sh` | exit 0 — horner fma=80/80; matmul_stable fma=0; main=98ins |
| `lic check li-tests/codegen/horner_5m_fma_codegen_probe.li` | exit 0 |
| Short-trip probe (`i < 64`, pre-fix) | main ~11 insns, 0 FMA (LLVM const-fold) |

**Key file:line:**

- `compiler/mir/lower.cpp:2106-2165` — Horner while recognition + `HornerStepPow4`
- `compiler/codegen/emit.cpp:657-672` — unconditional horner `fmuladd`
- `compiler/codegen/emit.cpp:231-234` — matmul IKJ FMA gated on `!fp_numerically_stable`
- `compiler/codegen/emit.cpp:1435-1442` — fast-math flags (default release)
- `compiler/verify/vc_witness.cpp` — no `witness_horner*` (contrast `witness_dot4_int_loop`)
- `docs/semantics/Discharge.lean:27-32` — `dot4_int_loop_eval_spec` (contrast; no horner lemma)
- `benchmarks/tier1_micro/horner_pure_li/li/main.li:15-17` — tier-1 bench source pattern
- `li-tests/codegen/horner_5m_fma_codegen_probe.li` — codegen probe
- `li-tests/tooling/horner_fma_codegen_lean_drift.sh` — gap gate

## Hypothesis outcomes

- **HYPOTHESIS: verified** — No `witness_horner*` in `vc_witness.cpp` | evidence: harness grep
- **HYPOTHESIS: verified** — No horner loop lemma in `Discharge.lean` | evidence: harness grep; only `dot4_*` / `mat2_*`
- **HYPOTHESIS: verified** — 5M-trip horner probe retains FMA codegen | evidence: harness main=98ins, fma=80
- **HYPOTHESIS: verified** — `--numerically-stable` horner still uses `fmuladd`; matmul IKJ does not | evidence: harness fma=80/80 vs 0
- **HYPOTHESIS: falsified** — Short-trip (`i < 64`) probe with `volatile_sink` on `acc` retains FMA | evidence: pre-fix main ~11 insns, 0 FMA (const-fold)
- **HYPOTHESIS: deferred** — Horner loop ≡ ensures in AutoVC | evidence: needs witness design + P-float lemma

## Recommended issues/PRs

1. **lic:** Merge horner FMA drift harness + 5M probe; wire into `contracts_discharge_corpus.sh` — labels: `provability`, `G-hw`, `testing`
2. **lic:** `[P-float] witness_horner_fma_loop + Discharge horner_loop_eval (64-step pilot)` — labels: `provability`, `G-vc`, `PH-7e`
3. **lic:** Align `--numerically-stable` with Horner FMA disable (parity with matmul IKJ) — labels: `provability`, `G-hw`, `numerics`
4. **lic:** Update `provability-gaps.md` G-math row — horner tier-1 = FMA codegen advisory, not Lean-closed — labels: `provability`, `G-lean`
5. **lic:** Remove duplicate Proof-db appendix blocks (`provability-gaps.md`, lic#461) — labels: `provability`
6. **benchmarks:** Link cycle 21 digest in ecosystem grader provability row — labels: `provability`

## Deferred

- matmul IKJ / blocked loop witness (cycles 19–20 / lic#472)
- mat2 FMA codegen vs Lean eval (cycles 16–17)
- `sqrt_open_bound` P-float intentional open
- Vec3 / CallProc opaque ensures (cycles 13–15)
- `publish_subdir` whitepaper — not injected this run
