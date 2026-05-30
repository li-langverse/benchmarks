# Proof gap researcher — cycle 27 (prelude scale/axpy/norm manifest tier overclaim)

**Run:** 2026-05-30 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-2i · G-test-verify, G-math, G-vc  
**Focus:** PH-2i prelude `scale` / `axpy` / `norm` — codegen present, manifest `verify_ok`, AutoVC trivial  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** Prelude linalg smoke tests (`scale_float4`, `axpy_float4`, `norm_float4`) are tiered **`verify_ok`** in `manifest.toml` but carry **no proc-level contracts** and **no Lean Discharge specs** — only trivial `main` `Prop := True` AutoVC.
- **HYPOTHESIS: verified** — MIR lowers scalar×array to `ArrayScaleF64`, `axpy` to `ArrayAxpyF64`, `norm` to dot-of-self + `li_rt_sqrt` (`lower.cpp:271-337`, `1272-1289`).
- **HYPOTHESIS: verified** — Codegen emits scalar multiply loops (`emit.cpp:1211-1233`); objdump shows `mulsd` in `scale_float4` binary.
- **HYPOTHESIS: verified** — `Discharge.lean` and `vc_witness.cpp` have no `scale_spec` / `axpy_spec` / `norm_spec` wiring.
- **HYPOTHESIS: verified** — AutoVC for all three specimens is `vc_main_ensures_0 (result : Int) : Prop := True` only (no prelude predicates).
- **HYPOTHESIS: verified** — **G-test-verify gap:** manifest overclaims vs `broadcast_len1_*` correctly at `compile_ok` (cycle 26).
- **Evidence test added:** `li-tests/tooling/prelude_linalg_manifest_tier_gap.sh` (wired into `contracts_discharge_corpus.sh`).
- **`lic check`:** all three specimens — exit 0; gap script — PASS.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| Prelude `2.0 * array` | **Codegen** — `ArrayScaleF64` | `lower.cpp:271-292`, `1645-1655` |
| Prelude `axpy(α,x,y)` | **Codegen** — in-place `ArrayAxpyF64` | `lower.cpp:316-337`, `1245-1260` |
| Prelude `norm(a)` float | **Codegen** — `dot(a,a)` + `li_rt_sqrt` | `lower.cpp:1272-1289` |
| Lean eval for prelude ops | **Missing** | no symbols in `Discharge.lean` |

### 2. Contract gaps

- Smoke tests use **`ensures result == 0` on `main` only** — no postconditions on scaled arrays, axpy side effects, or `norm(a)` value.
- **Contrast (closed slice):** `linalg_axpy4_int_closed.li` proves scalar `alpha*x+y` with real `axpy4_int` VCs in AutoVC — not array-level prelude semantics.

### 3. Trusted surface

- `norm` float path calls **`li_rt_sqrt`** (runtime/trusted FP); no `sqrt_open_bound`-style VC on prelude call sites.
- No `trusted.lean` edits (policy).

### 4. External trust boundaries

- **Deferred:** Downgrade manifest tier to `compile_ok` until array-level P-linalg witnesses land (human review of manifest policy).
- **Deferred:** Float `norm` ↔ `sqrt` contract linkage (**P-float** / **G-vc**).

### 5. Evidence pack

| Item | Location |
|------|----------|
| Scale MIR | `compiler/mir/lower.cpp:271-292` |
| Axpy MIR | `compiler/mir/lower.cpp:316-337` |
| Norm MIR (dot+sqrt) | `compiler/mir/lower.cpp:1272-1289` |
| Scale codegen | `compiler/codegen/emit.cpp:1211-1233` |
| Manifest overclaim | `li-tests/manifest.toml:868-894` (`verify_ok`) |
| Contrast compile_ok | `li-tests/manifest.toml:825-831` (`broadcast_len1_*`) |
| Gap repro script | `li-tests/tooling/prelude_linalg_manifest_tier_gap.sh` |
| Specimens | `li-tests/math_linalg/scale_float4.li`, `axpy_float4.li`, `norm_float4.li` |
| Closed control | `li-tests/contracts_verify/linalg_axpy4_int_closed.li` |
| G-* register | `docs/verification/provability-gaps.md` — **G-test-verify** Partial; **G-math** PH-2i prelude slice |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/math_linalg/scale_float4.li
./build/compiler/lic/lic check li-tests/math_linalg/axpy_float4.li
./build/compiler/lic/lic check li-tests/math_linalg/norm_float4.li
./li-tests/tooling/prelude_linalg_manifest_tier_gap.sh
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | `scale_float4` lowers to `ArrayScaleF64` with FMul codegen | `lower.cpp:279`, objdump `mulsd` |
| **verified** | `axpy_float4` lowers to `ArrayAxpyF64` | `lower.cpp:325` |
| **verified** | `norm_float4` lowers via self-dot + extern sqrt | `lower.cpp:1277-1287` |
| **verified** | No Lean prelude scale/axpy/norm specs or witnesses | gap script grep on `Discharge.lean`, `vc_witness.cpp` |
| **verified** | AutoVC is trivial main-only for all three smoke tests | build → `vc_main_ensures_0 : Prop := True` |
| **verified** | Manifest marks them `verify_ok` (G-test-verify overclaim) | `manifest.toml:868-894` vs broadcast `compile_ok` |
| **falsified** | “Prelude smoke tests emit Discharge-linked VCs like mat2 closed” | AutoVC has no `Discharge.*` refs |
| **deferred** | Array-level `axpy_spec` / `scale_spec` / `norm_spec` + manifest promotion | Needs P-linalg design (lic **#472** family) |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| G-test-verify: downgrade `scale_float4` / `axpy_float4` / `norm_float4` to `compile_ok` until witnesses | **lic** | `provability`, `G-test-verify`, `PH-2i`, `li-tests` |
| P-linalg: prelude `ArrayScaleF64` / `ArrayAxpyF64` / float `norm` specs in Discharge + VC witness | **lic** | `provability`, `PH-2i`, `G-math`, `G-vc` |
| Link float `norm` prelude to `sqrt_open_bound` or closed sqrt VC | **lic** | `provability`, `P-float`, `G-vc` |
| Extend `provability-gaps.md` G-test-verify row: manifest tier vs trivial AutoVC | **lic** | `documentation`, `provability` |

**Existing (no duplicate):** lic **#472** (P-linalg loop ≡ ensures), lic **#461** (provability-gaps doc hygiene).

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper this run.
- Horner FMA / `--numerically-stable` asymmetry (cycle 18 branch; harness not on `dev`).
- Broadcast len-1 Lean witness (cycle 26).
- `trusted.lean` — human gate only.
