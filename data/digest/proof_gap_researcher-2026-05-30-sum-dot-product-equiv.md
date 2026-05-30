# Proof gap researcher — cycle 28 (sum(a×b) vs dot — codegen drift, no Lean equiv)

**Run:** 2026-05-30 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-2i · G-math, G-vc, G-test-verify, G-hw  
**Focus:** PH-2i reductions — `sum(a * b)` vs `dot(a, b)` divergent lowering; `--numerically-stable` applies to sum only  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** Prelude `sum(a*b)` and `dot(a,b)` are documented as equivalent math (`linear-algebra.md`) but lower to **different MIR ops** (`ArrayBinOpF64` + `ArraySumF64` vs `ArrayDotF64`) with no Lean equivalence lemma.
- **HYPOTHESIS: verified** — `sum(a*b)` emits elementwise `mulsd` then reduction; `dot(a,b)` uses fused `ArrayDotF64` loop (possibly SIMD-gather).
- **HYPOTHESIS: verified** — `ArraySumF64` gates Kahan summation on `fp_numerically_stable` (`emit.cpp:1086-1093`); `ArrayDotF64` does **not** consult the flag — `--numerically-stable` changes sum path add/sub count (3→12) but not dot-via-sum mul count.
- **HYPOTHESIS: verified** — `dot_via_sum_product.li` computes `s = sum(a*b)` and `d = dot(a,b)` but carries **no proc-level `ensures s == d`**; AutoVC is trivial `main` `Prop := True` only.
- **HYPOTHESIS: verified** — `Discharge.lean` has `dot4_int_loop_eval_spec` for int loops but **no** `sum_dot_float_equiv` / `sum4_float_spec`.
- **Contrast:** `linalg_dot4_int_closed.li` emits real closed-form int VCs; `linalg_dot4_float_closed.li` uses **prelude dot() return witness** stub (`Prop := True`).
- **Evidence test added:** `li-tests/tooling/sum_dot_product_equiv_gap.sh` (wired into `contracts_discharge_corpus.sh`).
- **`lic check`:** `sum_float4.li`, `dot_via_sum_product.li` — exit 0; gap script — PASS.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| `sum(a*b)` lowering | **Codegen** — temp array + `ArraySumF64` | `lower.cpp:1308-1324`, elementwise via `lower_array_elementwise_binop_expr` |
| `dot(a,b)` lowering | **Codegen** — direct `ArrayDotF64` | `lower.cpp:1264-1270`, `emit.cpp:1342-1375` |
| Semantic equivalence | **Missing** | no spec in `Discharge.lean` |
| `--numerically-stable` asymmetry | **Open** | Kahan in `ArraySumF64` only; dot path unchanged (objdump) |

**Soundness note (G-hw):** Under `--numerically-stable`, `sum(a*b)` and `dot(a,b)` may **diverge numerically** even when mathematically equal — proof corpus cannot treat them as interchangeable without float model work (**P-float**).

### 2. Contract gaps

- `dot_via_sum_product.li` — variables `s` and `d` never constrained; manifest **`verify_ok`** overclaims vs absent proc contracts (**G-test-verify**).
- **Contrast (int closed slice):** `linalg_dot4_int_closed.li` proves closed-form dot with real `dot4_int` VCs.
- **Contrast (float partial):** `linalg_dot4_float_closed.li` relies on prelude dot stub witness, not closed-form float formula.

### 3. Trusted surface

- No `trusted.lean` edits (policy). Reductions are user/prelude surface only.

### 4. External trust boundaries

- **Deferred:** Human decision on whether `sum(a*b)` should canonicalize to `ArrayDotF64` in MIR (perf + proof unification).
- **Deferred:** Float associativity / Kahan policy for dot vs sum (**P-float**, **G-hw** axiomatic limit).

### 5. Evidence pack

| Item | Location |
|------|----------|
| `sum()` prelude lowering | `compiler/mir/lower.cpp:1308-1324` |
| `dot()` prelude lowering | `compiler/mir/lower.cpp:1264-1270` |
| `ArraySumF64` Kahan gate | `compiler/codegen/emit.cpp:1070-1096` |
| `ArrayDotF64` (no stable gate) | `compiler/codegen/emit.cpp:1342-1375` |
| Reduction smoke tests | `li-tests/math_linalg/reductions/sum_float4.li`, `dot_via_sum_product.li` |
| Int closed control | `li-tests/contracts_verify/linalg_dot4_int_closed.li` |
| Float prelude stub control | `li-tests/contracts_verify/linalg_dot4_float_closed.li` |
| Gap repro script | `li-tests/tooling/sum_dot_product_equiv_gap.sh` |
| G-* register | `docs/verification/provability-gaps.md` — **G-math** Partial; **G-vc** loop vs closed-form |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/math_linalg/reductions/sum_float4.li
./build/compiler/lic/lic check li-tests/math_linalg/reductions/dot_via_sum_product.li
./li-tests/tooling/sum_dot_product_equiv_gap.sh
# objdump: sum_float4 default add/sub=3, --numerically-stable add/sub=12
# objdump: dot_via_sum_product mulsd=4 unchanged under stable
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | `sum(a*b)` and `dot(a,b)` use different MIR/codegen paths | `lower.cpp`, objdump mulsd in `dot_via_sum_product` main |
| **verified** | No Lean `sum_dot` equivalence in Discharge | `Discharge.lean` grep empty |
| **verified** | `dot_via_sum_product` AutoVC trivial; manifest `verify_ok` | gap script AutoVC check |
| **verified** | `--numerically-stable` affects ArraySumF64 only | objdump add/sub 3 vs 12; mulsd count unchanged |
| **verified** | Int dot closed has real VCs; float dot uses prelude stub | gap script contrast on AutoVC |
| **deferred** | `sum_dot4_float_equiv_spec` + witness | Needs P-float / codegen unification design |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| P-linalg: prove or canonicalize `sum(a*b)` ≡ `dot(a,b)` (MIR + Lean) | lic | `proof`, `PH-2i`, `G-math` |
| `--numerically-stable`: apply Kahan/conservative policy to `ArrayDotF64` | lic | `proof`, `PH-7e`, `G-hw` |
| Downgrade `math_linalg/reductions/*` manifest tier until proc contracts land | lic | `G-test-verify`, `PH-2i` |
| lic #472 — loop implementation ≡ closed-form ensures (P-linalg gate) | lic | `proof`, `G-vc` |

---

## Deferred

- Canonical MIR rewrite `sum(a*b)` → `ArrayDotF64` (human perf/proof tradeoff).
- Float closed-form dot VCs matching int slice (prelude stub removal).
- `publish_subdir` not injected — no research-findings whitepaper (`provability_holes` auxiliary, no vertical slug per `researcher-factory.ts`).
