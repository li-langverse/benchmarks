# Proof gap researcher digest — 2026-05-29 (cycle 18)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-vec3-field-opaque-vc`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2i, PH-2f — G-vc / P-linalg vec3_dot-style opaque ensures

## Executive summary

- **Focus:** **G-vc / P-linalg** — `vec3_dot` with **Vec3 field access** in `ensures`: Lean translation gap + certificate `True` stub vs real float codegen.
- **Verified:** `expr_to_lean` has no `Member`/field path (`vc_emit_lean.cpp:202-254`) → `/-! VC ensures (opaque): source expr not yet translated -/`.
- **Verified:** AutoVC still emits `vc_vec3_dot_ensures_0 := True` + `trivial` `_proved` while user `ensures` states dot-product formula (`vec3_dot_float_field_opaque.li:9`).
- **Verified:** Vec3 parameters lower to `(a : Int) (b : Int)` in Lean formals (`lean_type_name` Named fallback `vc_emit_lean.cpp:138`).
- **Verified:** Codegen implements mul/add (`objdump vec3_dot`) with **no** runtime contract hooks — same codegen↔Lean drift class as `sqrt_open_bound`.
- **Contrast:** `li-math` locals-in-ensures pattern gets static witness comment but still `Prop := True` (ax/bx not in Lean scope).
- **Harness:** `vec3_dot_field_opaque_lean_gap.sh` added; wired into `contracts_discharge_corpus.sh`; run → ok.
- **No `trusted.lean` edits.**

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| Field access untranslated to Lean | `vc_emit_lean.cpp:252-253` — `default: return nullopt` (no Member) |
| Opaque ensures marker in AutoVC | `build/generated/AutoVC.lean` — `VC ensures (opaque)` on field specimen |
| Vec3 → Int Lean type drift | `vc_vec3_dot_ensures_0 (a : Int) (b : Int)` — `vc_emit_lean.cpp:138` |
| Real float dot in codegen | `objdump vec3_dot` — `mulsd`/`addsd`; no `li_bounds_fail`/`li_panic` |
| Prelude `dot4_float` uses witness stub | `linalg_dot4_float_closed.li` — `Prop := True` + prelude comment (not field formula) |

### 2. Contract gaps

- User `ensures result == a.x * b.x + …` is **not** a Lean Prop in AutoVC — only `True` with `trivial` discharge.
- `lic build` + Lean typecheck **pass** on field specimen — certificate overclaims dot identity (same honesty class as `index_refinement` True stubs).
- `li-math` `vec3_dot` (`lib.li:136`) references locals `ax`/`bx` in ensures: static witness path, still **no** real formula in Lean (`Prop := True`).
- **P-linalg** backlog row “float `vec3_dot` Props” remains open despite working codegen.

### 3. Trusted surface

- `trusted.lean` unchanged (`docs/semantics/trusted.lean:1-41`).
- Gap is VC emission / `lean_type_name`, not axiom growth.

### 4. External trust boundaries

- Closing requires `expr_to_lean` field/member lowering + `Li.Vec3` (or struct) in Lean + **P-linalg** lemmas — human review; not `trusted.lean` without RFC.
- `packages/li-math` consumers inherit stub certificate until discharge lands.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-vc** / **P-linalg** | `vec3_dot_float_field_opaque.li:9` — field ensures |
| **G-vc** | `vc_emit_lean.cpp:202-254` — no field translation |
| **G-vc** | `vc_emit_lean.cpp:138` — Named → `Int` fallback |
| **G-vc** (codegen) | `objdump -d … --disassemble=vec3_dot` — mulsd/addsd |
| **G-lean** | AutoVC `vc_vec3_dot_ensures_0 := True` + `_proved := trivial` |
| **Contrast** | `packages/li-math/src/lib.li:134-145` — locals ensures, static witness |
| **Harness** | `bash li-tests/tooling/vec3_dot_field_opaque_lean_gap.sh` → ok |
| **lic check** | `lic check li-tests/contracts_verify/vec3_dot_float_field_opaque.li` → exit 0 |
| **Retest** | `bash li-tests/tooling/sqrt_open_bound_contract_tier.sh` → ok |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — Vec3 field access in ensures emits opaque VC marker and True stub | evidence: vec3_dot_field_opaque_lean_gap.sh; AutoVC.lean`
- `HYPOTHESIS: verified — Vec3 params lower to Int in Lean AutoVC formals | evidence: vc_emit_lean.cpp:138; vec3_dot_field_opaque_lean_gap.sh`
- `HYPOTHESIS: verified — vec3_dot codegen computes float products without runtime ensures witness | evidence: objdump vec3_dot; vec3_dot_field_opaque_lean_gap.sh`
- `HYPOTHESIS: verified — lic build + Lean typecheck pass despite missing dot-product Prop | evidence: vec3_dot_field_opaque_lean_gap.sh`
- `HYPOTHESIS: verified — li-math locals-in-ensures uses static witness but still True Prop | evidence: build vec3_dot_locals pattern; lib.li:136; AutoVC static witness comment`
- `HYPOTHESIS: falsified — field ensures translate to Lean formula with _proved discharge | evidence: grep AutoVC; vec3_dot_field_opaque_lean_gap.sh`
- `HYPOTHESIS: falsified — expr_to_lean supports a.x member access today | evidence: vc_emit_lean.cpp:202-254`
- `HYPOTHESIS: deferred — close via Li.Vec3 + field expr_to_lean + P-linalg lemmas | evidence: proof-corpus-roadmap P-linalg open float vec3_dot`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| feat(G-vc): expr_to_lean Member/field access for Vec3 ensures | **lic** | `PH-2e`, G-vc, P-linalg |
| feat(G-vc): lean_type_name for user object types (Vec3 → struct, not Int) | **lic** | `PH-2f`, G-vc |
| feat(P-linalg): discharge vec3_dot ensures via Li.Discharge lemmas | **lic** | `PH-2i`, research |
| test(provability): vec3_dot_field_opaque_lean_gap regression harness | **lic** | G-vc, research |
| docs: provability-gaps G-vc — vec3_dot field opaque + Vec3 Lean type drift | **lic** | provability-gaps |

## Deferred

- **G-vc** sqrt_open_bound codegen drift (cycle 17 — not retested).
- **G-par** disjoint_elem executable race (cycle 16 — not retested).
- **G-net** recv/send triple drift (cycle 14 — not retested).
- **G-bnd** refinement True stubs (cycle 11 — not retested).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
