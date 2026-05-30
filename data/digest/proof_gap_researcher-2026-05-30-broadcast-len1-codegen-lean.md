# Proof gap researcher — cycle 26 (broadcast_len1 codegen ↔ Lean)

**Run:** 2026-05-30 · **Goal:** `provability_holes` · **north_star_fit:** provable pillar · PH-2i · G-math, G-vc  
**Focus:** length-1 array broadcast (`array[1]` → `array[N]`) — codegen present, Lean certificate absent  
**Lic root:** `/home/s4il0r/Documents/Cursor/li-langverse/lic`

---

## Executive summary

- **One focus:** PH-2i **length-1 broadcast** — MIR/codegen path is real; **no** `Discharge.lean` spec, **no** `vc_witness` hook, manifest **`compile_ok` only** (not `verify_ok`).
- **HYPOTHESIS: verified** — `lower.cpp` sets `array_broadcast_*_len1`; `emit.cpp` disables SIMD when either flag is set (`:1126-1127`).
- **HYPOTHESIS: verified** — debug codegen reuses scalar rhs via `movaps xmm0` + repeated `addsd` (`emit.cpp:1137-1162`; objdump on `broadcast_len1_add_float4.li`).
- **HYPOTHESIS: verified** — `Discharge.lean` and `vc_witness.cpp` have no broadcast symbols; AutoVC from broadcast smoke has no broadcast predicates.
- **HYPOTHESIS: falsified** — “broadcast specimens are `verify_ok` in manifest” — both are **`compile_ok`** (`manifest.toml:825-831`).
- **Evidence test added:** `li-tests/tooling/broadcast_len1_codegen_lean_gap.sh` (wired into `contracts_discharge_corpus.sh`).
- **`lic check`:** `broadcast_len1_add_float4.li`, `broadcast_len1_mul_int4.li` — exit 0.
- **Corpus:** `./li-tests/tooling/broadcast_len1_codegen_lean_gap.sh` → PASS; `contracts_discharge_corpus.sh` → ok (~57s).

---

## Deliverable / findings

### 1. Compiler / semantics gaps

| Gap | Status | Evidence |
|-----|--------|----------|
| NumPy rank broadcast | **Rejected** at typecheck (by design) | `typecheck.cpp:883`, `broadcast_numpy_reject_*.li` |
| **Length-1 broadcast** | **Codegen only** — no Lean eval | `lower.cpp:413-414`, `emit.cpp:1137-1162` |
| SIMD on broadcast ops | **Disabled** | `emit.cpp:1126-1127` (`simd_ok` false when broadcast flags set) |

### 2. Contract gaps

- Broadcast smoke tests use **`ensures result == 0` on `main` only** — no proc-level `ensures` on `c[i] = a[i] + b[0]`, so **P-linalg / G-vc** has nothing to discharge for broadcast semantics yet (contrast `linalg_dot4_int_loop_open.li` + `dot4_loop_ensures_lean_stub_gap.sh`).

### 3. Trusted surface

- No `trusted.lean` edits (policy). Broadcast is pure user/MIR lowering.

### 4. External trust boundaries

- **Deferred:** IEEE float associativity for broadcast element-wise chains — **G-hw** axiomatic; not in scope for len-1 slice.

### 5. Evidence pack

| Item | Location |
|------|----------|
| MIR broadcast flags | `compiler/mir/lower.cpp:413-414`, `433-434` |
| Codegen broadcast + SIMD gate | `compiler/codegen/emit.cpp:1126-1162` |
| Manifest tier | `li-tests/manifest.toml:825-831` (`compile_ok`) |
| Gap repro script | `li-tests/tooling/broadcast_len1_codegen_lean_gap.sh` |
| Specimens | `li-tests/math_linalg/broadcast_len1_add_float4.li`, `broadcast_len1_mul_int4.li` |
| G-* register | `docs/verification/provability-gaps.md` — **G-math** Partial, length-1 broadcast listed under PH-2i |

**Commands run:**

```bash
cd lic
./build/compiler/lic/lic check li-tests/math_linalg/broadcast_len1_add_float4.li
./build/compiler/lic/lic check li-tests/math_linalg/broadcast_len1_mul_int4.li
./li-tests/tooling/broadcast_len1_codegen_lean_gap.sh
./li-tests/tooling/contracts_discharge_corpus.sh
```

---

## Hypothesis outcomes (session)

| Outcome | Statement | Evidence |
|---------|-----------|----------|
| **verified** | MIR lowers `array[1] op array[N]` with `array_broadcast_rhs_len1` | `lower.cpp:413-414` |
| **verified** | SIMD vectorization skipped for broadcast binops | `emit.cpp:1126-1127` |
| **verified** | No Lean broadcast semantics or witness | `Discharge.lean`, `vc_witness.cpp` (grep); gap script |
| **verified** | Debug IR reuses scalar load for rhs broadcast | objdump `movaps xmm0` + `addsd` in `li_user_main` |
| **falsified** | Manifest marks broadcast tests `verify_ok` | `manifest.toml:826`, `831` → `compile_ok` |
| **deferred** | Wire `broadcast_len1_add_spec` + witness like `dot4_int_loop_eval_spec` | Needs P-linalg design (lic **#472** family) |

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| P-linalg: `broadcast_len1_*_spec` in Discharge + VC witness (not `Prop := True`) | **lic** | `provability`, `PH-2i`, `G-math`, `G-vc` |
| Extend `provability-gaps.md` G-math row: len-1 broadcast codegen without Lean | **lic** | `documentation`, `provability` |
| PH-2i: promote `broadcast_len1_*` to `verify_ok` after witness lands | **lic** | `PH-2i`, `li-tests` |

**Existing (no duplicate):** lic **#472** (P-linalg loop ≡ ensures), lic **#461** (provability-gaps doc hygiene), lic **#387** (G-par Lean).

---

## Deferred

- `publish_subdir` not injected — no research-findings whitepaper this run.
- Full NumPy rank broadcast (explicitly out of scope per agent-scope rules).
- `@vectorized` + broadcast interaction (7d / G-dec) — separate focus.
- `trusted.lean` — human gate only.
