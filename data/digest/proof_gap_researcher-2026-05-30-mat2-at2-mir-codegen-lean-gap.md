# Proof gap researcher — cycle 32 (mat2_at2_eval vs MIR `@` codegen)

**Run:** 2026-05-30 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-2i / PH-2f · G-lean, G-math, G-meta, G-test-verify  
**Focus:** Closed 2×2 float `@` Lean certificate uses `mat2_at2_eval`; executable path uses `ArrayMatMul2DF64` — no MIR↔eval refinement lemma  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** `mat2_at2_eval` trusted vs MIR `@` row in `provability-gaps.md` — semantic Prop closed in `Discharge.lean`, codegen equivalence **not** proved.
- **HYPOTHESIS: verified** — AutoVC `vc_mat2_at2_ensures_0` proves `mat2_at2_float_spec A B (mat2_at2_eval A B)` with **no `result` formal**; discharge cites `mat2_at2_float_spec_proved`, not `return A @ B`.
- **HYPOTHESIS: verified** — `witness_mat2_int_at2_spec` pattern-matches `@` ensures and routes to eval-based Prop (`vc_emit_lean.cpp:347-410`, `vc_witness.cpp:415-425`).
- **HYPOTHESIS: verified** — No `ArrayMatMul` / `mir_matmul` bridge in `Discharge.lean` or `trusted.lean`; `MIR.lean` still planned (`semantics/README.md`).
- **HYPOTHESIS: verified** — `mat2_at2_codegen_probe.li` (sink on `C[1][1]`) emits `mulsd` in `li_user_main` — live `ArrayMatMul2DF64` unrolled path (2×2, no IKJ loops).
- **HYPOTHESIS: verified** — Manifest tiers closed mat2 as `verify_ok`; `run_all.sh` has no `prove_lean_ok` (**G-test-verify** honesty gap).
- **Evidence test added:** `mat2_at2_mir_codegen_lean_gap.sh` → `contracts_discharge_corpus.sh`.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| Lean `mat2_at2_eval` vs MIR `@` | **Missing (G-meta)** | No lemma in `Discharge.lean` / `trusted.lean` |
| VC ensures on eval, not return | **By design (partial 2f)** | AutoVC `vc_mat2_at2_ensures_0` — no `result` param |
| `ArrayMatMul2DF64` 2×2 lowering | **Codegen** — unrolled IKJ | `emit.cpp:1317-1326`; probe `mulsd` in `li_user_main` |
| `witness_mat2_int_at2_spec` | **Static pattern** — not MIR-linked | `vc_witness.cpp:415-425` |

**Contrast (cycle 29):** N×N matmul has **no** witness at all; 2×2 has closed **eval** semantics only.

### 2. Contract gaps

- **G-lean / G-math:** `linalg_mat2_at2_float_closed.li` passes `lic build` + zero open goals via eval substitution — certificate does **not** entail executable `@` refines `mat2_at2_eval`.
- **G-vc:** Proc body `return A @ B` is witnessed by shape match, not MIR return linkage (`mir_return_linked=` gap family).
- **G-test-verify:** `verify_ok` ≡ `lic build` only (`run_all.sh:91-93`); no kernel-level codegen proof tier.

### 3. Trusted surface

- No `trusted.lean` edits (policy). `mat2_at2_float_spec_proved` is pure `rfl` on functional `mat2_at2_eval` — not an axiom on libm/codegen.

### 4. External trust boundaries

- **Deferred:** `MIR.lean` preservation lemmas (`semantics/README.md`) — human RFC / **G-meta** research scope.
- **Deferred:** FMA reordering on `@` when default numerics vs Lean nested `+`/`* model (**G-hw**).

### 5. Evidence pack

| Item | Location |
|------|----------|
| Eval-based ensures emit | `compiler/verify/vc_emit_lean.cpp:355-410` |
| Mat2 witness matcher | `compiler/verify/vc_witness.cpp:415-425` |
| Closed eval + spec proof | `docs/semantics/Discharge.lean:38-58` |
| Closed specimen | `li-tests/contracts_verify/linalg_mat2_at2_float_closed.li` |
| Codegen probe (anti-DCE) | `li-tests/math_linalg/mat2_at2_codegen_probe.li` |
| Gap repro script | `li-tests/tooling/mat2_at2_mir_codegen_lean_gap.sh` |
| G-* register | `docs/verification/provability-gaps.md` — **G-lean** still-open `mat2_at2_eval` vs MIR |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/contracts_verify/linalg_mat2_at2_float_closed.li   # exit 0
./build/compiler/lic/lic check li-tests/math_linalg/mat2_at2_codegen_probe.li            # exit 0
./li-tests/tooling/mat2_at2_mir_codegen_lean_gap.sh                                     # exit 0 PASS
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | AutoVC mat2 ensures uses `mat2_at2_eval`, not `result` | `build/generated/AutoVC.lean` after closed specimen build |
| **verified** | Discharge proves spec on eval only (`rfl`) | `Discharge.lean:55-58` |
| **verified** | No MIR↔eval bridge in semantics package | grep `Discharge.lean`, `trusted.lean` — zero `ArrayMatMul` |
| **verified** | Executable 2×2 `@` emits multiply codegen | `mat2_at2_codegen_probe.li` + `objdump` `mulsd` in `li_user_main` |
| **verified** | Manifest `verify_ok` does not mean codegen proof | `manifest.toml` + `run_all.sh` — no `prove_lean_ok` |
| **deferred** | `ArrayMatMul2DF64` refines `mat2_at2_eval` | **G-meta** / planned `MIR.lean` |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| G-meta: `ArrayMatMul2DF64` refines `Li.Discharge.mat2_at2_eval` (2×2 pilot) | **lic** | `provability`, `G-meta`, `PH-2i`, `G-math` |
| Wire `mir_return_linked=` witness for `@` return vs eval-based ensures | **lic** | `provability`, `G-vc`, `PH-2f` |
| Split manifest `prove_lean_ok` vs `verify_ok` for closed linalg corpus | **lic** | `G-test-verify`, `li-tests` |
| Land `mat2_at2_mir_codegen_lean_gap.sh` + codegen probe | **lic** | `provability`, `testing` |

**Related:** cycle 29 matmul loop witness gap (no witness at all for N×N); cycle 31 G-par opaque stubs.

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper (`provability_holes` auxiliary, no vertical slug per `researcher-factory.ts`).
- General N×N `@` codegen proof (see `matmul_loop_codegen_witness_gap.sh`).
- `trusted.lean` — human gate only.
