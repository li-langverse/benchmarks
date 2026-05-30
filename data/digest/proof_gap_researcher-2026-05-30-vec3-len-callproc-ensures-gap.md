# Proof gap researcher — cycle 34 (vec3_len CallProc ensures chain)

**Run:** 2026-05-30 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-2i / PH-2e / PH-2f · G-vc, G-math, G-test-verify, G-trust  
**Focus:** `vec3_len` / `vec3_len_sq` CallProc ensures chain — opaque emit + vacuous `True` discharge vs `sqrt_open_bound` intentional open  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** Production `vec3_len` ensures `result == li_rt_sqrt(vec3_len_sq(a))` — nested CallProc + extern sqrt (deferred from cycle 33).
- **HYPOTHESIS: verified** — `expr_to_lean` translates only `abs` calls; `li_rt_sqrt` / user-proc calls in ensures → opaque marker + `Prop := True` + `trivial`.
- **HYPOTHESIS: verified** — `vec3_len_sq` ensures `result == vec3_dot(a, a)` same opaque stub path; `expr_same_shape` has no `Call` case (`vc_witness.cpp:52-71`).
- **HYPOTHESIS: verified** — Chain reports **zero open goals** via vacuous discharge; contrast `sqrt_open_bound` emits real `Float.abs` Prop **without** `_proved` (intentionally open).
- **HYPOTHESIS: verified** — No `vec3_len` / `vec3_dot` specs in `Discharge.lean`; extern `li_rt_sqrt` call-site requires witness `True` (callee `ensures true`).
- **HYPOTHESIS: verified** — `manifest.toml` tiers `math_linalg/vec3_ops.li` as `verify_ok` despite vacuous chain (**G-test-verify** honesty gap).
- **Evidence test added:** `vec3_len_callproc_ensures_gap.sh` → `contracts_discharge_corpus.sh`.

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| CallProc in ensures (`li_rt_sqrt`, `vec3_dot`) | **Missing (G-vc)** | `expr_to_lean` Call branch: `abs` only (`vc_emit_lean.cpp:224-231`) |
| Static witness for nested Call return | **Missing** | `expr_same_shape` default `false` for `Call` (`vc_witness.cpp:69-70`) |
| Opaque fallback still discharges | **Soundness hole** | Opaque comment + initial `prop = "True"` → `trivial` (`vc_emit_lean.cpp:343-416`) |
| Contrast: translatable float ensures | **Correct open** | `sqrt_open_bound`: `Float.abs …` Prop, no `_proved` theorem |

### 2. Contract gaps

- **G-vc:** `vec3_len` ensures cannot translate; certificate is vacuous `True` — does **not** prove `result == sqrt(dot(a,a))`.
- **G-math:** Production `packages/li-math/src/lib.li:152-163` — `vec3_len_sq` → `vec3_dot`; `vec3_len` → `li_rt_sqrt`; same chain as specimen.
- **P-float / P-linalg:** Nested CallProc ensures should either (a) emit real Props like `sqrt_open_bound` and stay **open**, or (b) wire `Li.Discharge` specs — today neither.
- **Contrast:** `sqrt_open_bound.li` `ensures abs(result * result - x) < 1e-12` — honest open float VC.

### 3. Trusted surface

- `li_rt_sqrt` extern: callee `ensures true` (`linalg_vec3_len_callproc_chain.li:8-11`); call-site requires VC trivially discharged.
- No `trusted.lean` edits (policy). Sqrt semantics live in C runtime (`li_rt`); P-float backlog (`sqrt_open_bound_placeholder` in `Discharge.lean:60-61`).

### 4. External trust boundaries

- **Deferred:** `Li.Discharge.vec3_len_spec` linking `li_rt_sqrt` postcondition to `vec3_dot(a,a)` — human RFC / **P-linalg** + **P-float** joint pass.
- **Deferred:** Whether opaque CallProc ensures should fail closed (open VC) instead of `True` stub — product policy decision.

### 5. Evidence pack

| Item | Location |
|------|----------|
| Call-only `abs` in expr_to_lean | `compiler/verify/vc_emit_lean.cpp:224-231` |
| Opaque → True → trivial path | `compiler/verify/vc_emit_lean.cpp:343-416` |
| No Call in expr_same_shape | `compiler/verify/vc_witness.cpp:52-71` |
| Production vec3_len chain | `packages/li-math/src/lib.li:152-163` |
| sqrt_open_bound open contrast | `li-tests/contracts_verify/sqrt_open_bound.li:7-12` |
| Chain specimen | `li-tests/contracts_verify/linalg_vec3_len_callproc_chain.li` |
| len_sq specimen | `li-tests/contracts_verify/linalg_vec3_len_sq_callproc.li` |
| Gap repro script | `li-tests/tooling/vec3_len_callproc_ensures_gap.sh` |
| G-* register | `docs/verification/provability-gaps.md:37,58` — float `vec3_dot`, `sqrt_open_bound` |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/contracts_verify/linalg_vec3_len_callproc_chain.li   # exit 0
./build/compiler/lic/lic check li-tests/contracts_verify/linalg_vec3_len_sq_callproc.li      # exit 0
./li-tests/tooling/vec3_len_callproc_ensures_gap.sh                                         # exit 0 PASS
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | vec3_len ensures opaque + True + trivial | AutoVC `vc_vec3_len_ensures_0 … Prop := True` + `_proved := trivial` |
| **verified** | vec3_len_sq user CallProc ensures same stub | AutoVC `vc_vec3_len_sq_ensures_0 … Prop := True` |
| **verified** | Zero open goals (vacuous) vs sqrt_open open | `check-autovc-open-goals.sh` pass on chain; fail on sqrt_open |
| **verified** | No Discharge vec3 specs | grep `Discharge.lean` — only `sqrt_open_bound_placeholder` |
| **verified** | manifest verify_ok ≠ semantic proof | `manifest.toml` `vec3_ops.li` + trivial chain discharge |
| **deferred** | Opaque CallProc should fail closed (open VC) | Policy — needs human issue |
| **deferred** | Real `vec3_len_float_spec` in Lean | **P-linalg** / **P-float** RFC |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| G-vc: opaque CallProc ensures should stay open (not True+trivial) | **lic** | `provability`, `G-vc`, `PH-2e` |
| P-linalg: `vec3_len_sq` / `vec3_len` Discharge specs + AutoVC wiring | **lic** | `provability`, `G-math`, `PH-2i`, `G-lean` |
| Land `vec3_len_callproc_ensures_gap.sh` + contracts_verify specimens | **lic** | `provability`, `testing` |
| G-test-verify: downgrade or annotate `vec3_ops.li` until chain proved | **lic** | `provability`, `G-test-verify` |
| P-float: link `li_rt_sqrt` postcondition to vec3_len chain | **lic** | `provability`, `P-float`, `G-trust` |

**Related:** cycle 33 vec3_dot FieldAccess opaque; cycle 17 sqrt codegen drift; `sqrt_open_bound` intentional open specimen.

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper (`provability_holes` auxiliary, no vertical slug per `researcher-factory.ts`).
- `vec3_cross` object-constructor ensures (FieldAccess + nested calls).
- `trusted.lean` — human gate only.
