# Proof gap researcher — cycle 27 (Horner FMA vs `--numerically-stable`)

**Run:** 2026-05-30 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-7e · G-hw, G-meta, G-math  
**Focus:** Horner `FmaFloatF64` / `HornerStepPow4` codegen ignores `--numerically-stable` (matmul parity gap)  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** PH-7e Horner FMA lowering — MIR emits `llvm.fmuladd` on **both** default and `--numerically-stable` release builds; matmul loop path gates FMA on `fp_numerically_stable` (`emit.cpp:232-247`).
- **HYPOTHESIS: verified** — `HornerStepPow4` / `HornerFmaUnroll` / `FmaFloatF64` never consult `fp_numerically_stable` (`emit.cpp:764-800`).
- **HYPOTHESIS: verified** — objdump: probe emits 128× `vfmadd213sd` with and without `--numerically-stable`.
- **HYPOTHESIS: verified** — no horner/fma symbols in `Discharge.lean` or `vc_witness.cpp`.
- **HYPOTHESIS: falsified** — “trip=64 probe suffices for FMA repro” — LLVM constant-folds small loops; **65536** trip required.
- **Evidence test added:** `li-tests/tooling/horner_fma_numerically_stable_gap.sh` (wired into `contracts_discharge_corpus.sh`).
- **`lic check`:** `horner_fma_codegen_probe.li` — exit 0.
- **Gap script:** `./li-tests/tooling/horner_fma_numerically_stable_gap.sh` → PASS.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| Horner FMA ignores `--numerically-stable` | **Open** | `emit.cpp:764-800` vs matmul `232-247` |
| Horner MIR lowering (PH-7e) | **Codegen only** | `lower.cpp:2091-2159` (`HornerStepPow4`, `HornerFmaUnroll`) |
| Lean horner/fma eval | **Missing** | `Discharge.lean` grep empty |

**Soundness note (G-hw):** FMA is not bit-identical to separate `fmul`+`fadd`; `--numerically-stable` is documented as cancellation-safe FP but does not apply to Horner today.

### 2. Contract gaps

- Horner probe uses **`ensures result == 0` on `main` only** — no proc-level float `ensures` linking loop acc to closed form; **G-vc** / **P-float** have nothing to discharge for Horner semantics (contrast `sqrt_open_bound.li`).

### 3. Trusted surface

- No `trusted.lean` edits (policy). Horner is pure user/MIR lowering.

### 4. External trust boundaries

- **G-hw axiomatic:** IEEE FMA vs mul+add rounding differences — human acceptance for tier-1 perf vs proof mode split.
- **Deferred:** Whether Lean float model should distinguish FMA (`P-float` design).

### 5. Evidence pack

| Item | Location |
|------|----------|
| Horner MIR pattern match | `compiler/mir/lower.cpp:2091-2159` |
| FMA emit (no stable gate) | `compiler/codegen/emit.cpp:764-800` |
| Matmul FMA stable gate (contrast) | `compiler/codegen/emit.cpp:232-247` |
| Gap repro script | `li-tests/tooling/horner_fma_numerically_stable_gap.sh` |
| Specimen | `li-tests/math_linalg/horner_fma_codegen_probe.li` |
| Tier-1 bench reference | `benchmarks/tier1_micro/horner_pure_li/li/main.li` |
| G-* register | `docs/verification/provability-gaps.md` — **G-hw** axiomatic; **G-math** Partial (FMA horner tier-1) |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/math_linalg/horner_fma_codegen_probe.li
./li-tests/tooling/horner_fma_numerically_stable_gap.sh
objdump -d /tmp/h_horner | grep -c vfmadd          # 160 (5M trip bench)
objdump -d /tmp/h_horner_stable | grep -c vfmadd   # 160 — gap confirmed
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | Horner MIR ops always emit `llvm.fmuladd` | `emit.cpp:764-800`; objdump 128× vfmadd |
| **verified** | Matmul loop path gates FMA on `fp_numerically_stable` | `emit.cpp:232-247` |
| **verified** | `--numerically-stable` does not disable Horner FMA | gap script; bench objdump 160/160 |
| **verified** | No Lean horner/fma semantics or witness | `Discharge.lean`, `vc_witness.cpp` grep |
| **falsified** | trip=64 probe reproduces FMA in release IR | LLVM folds; 65536 trip needed |
| **deferred** | `horner_fma_eval_spec` + witness in Discharge | Needs P-float / G-meta design |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| PH-7e: gate Horner FMA on `fp_numerically_stable` (parity with matmul) | **lic** | `provability`, `PH-7e`, `G-hw`, `numerics` |
| P-float: `horner_fma_eval_spec` in Discharge + VC witness (FMA vs mul+add) | **lic** | `provability`, `G-vc`, `G-meta` |
| Extend `provability-gaps.md` G-math row: Horner FMA ignores `--numerically-stable` | **lic** | `documentation`, `provability` |

**Existing (no duplicate):** lic **#472** (P-linalg loop ≡ ensures), lic **#461** (provability-gaps doc hygiene), lic **#387** (G-par Lean).

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper this run (`provability_holes` is auxiliary, no vertical slug per `researcher-factory.ts`).
- Full compiler↔Lean equivalence for FMA (`G-meta` research).
- `@vectorized` + Horner interaction (7d / G-dec) — separate focus.
- `trusted.lean` — human gate only.
