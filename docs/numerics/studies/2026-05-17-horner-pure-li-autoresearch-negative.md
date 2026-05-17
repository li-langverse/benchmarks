# Study: horner_pure_li autoresearch (negative result)

**Date:** 2026-05-17  
**Mode:** Autoresearch (B) → closed as negative  
**Target:** `horner_pure_li` (PH-5b, PH-7e) — only pure_li red in ecosystem audit  
**Agent:** autoresearch pass (li-langverse)

---

## 1. Hypothesis

| ID | Hypothesis | Falsifiable metric |
|----|------------|-------------------|
| H1 | Pure-Li Horner is ~88× slower than cpp due to immature PH-7e codegen (scalar float loop). | `wall_time` Li/cpp ≤ 1.2 after novel lowering (FMA chain, LICM). |
| H2 | A Li-specific fused Horner recurrence beats textbook scalar codegen once PH-7e exists. | Same metric + bitwise checksum vs C oracle. |

---

## 2. SOTA survey (Mode A — sufficient)

**Problem:** Evaluate `acc = acc * x + 1.0` for `x = 1.1`, `5_000_000` steps (tier-1 micro).

**Learned from:**

1. **Classical Horner / polynomial evaluation** — standard fused multiply-add recurrence; no alternative algorithm needed for this micro-bench.
2. **C oracle** — `lic/benchmarks/tier1_micro/horner_pure_li/common/horner_core.c` stores checksum in `g_li_horner_checksum`; `cpp/main.c` uses `volatile double sink` so `-O3` cannot delete the loop.
3. **Li source** — `li/main.li` implements the same recurrence but `return 0` with no observable use of `acc`.

**Conclusion:** SOTA recipe is already implemented in Li source; gap is **measurement + LLVM DCE**, not missing numerics.

---

## 3. Experiments (local repro)

```bash
cd ../li/benchmarks/harness
python3 bench.py --tier 1 --runs 2   # LIC_ROOT implicit: repo = li checkout
```

**Median wall_time (2026-05-17, Apple Silicon):**

| lang | horner_pure_li | simd_dot (pure_li) |
|------|----------------|---------------------|
| cpp | 0.0153 s | 0.0294 s |
| li | 0.6789 s | 0.6787 s |

**Disassembly (`otool -tv`, `-O3 -ffast-math -march=native`):** `_li_user_main` for both pure_li benches is an **integer countdown loop with no float/SIMD ops** — the hot recurrence was optimized away.

**Disassembly at `-O0`:** Horner body contains `fmul` / `fadd` on stack slots — MIR lowering is present; LLVM removes work at `-O3` because `acc` is dead.

---

## 4. Quality table (no improvement)

| Axis | Before | After autoresearch | Verdict |
|------|--------|-------------------|---------|
| Speed (Li/cpp) | ~44–89× (dashboard) | No code change shipped | **No improvement** |
| Accuracy | N/A (no observable output) | — | **Invalid bench** |
| Stability | N/A tier-0 | — | — |

**Root cause:** Asymmetric anti-DCE — C/cpp column runs real Horner; Li column times an empty loop. Identical ~0.68 s Li times for `horner_pure_li` and `simd_dot` confirm a shared artifact, not Horner-specific codegen cost.

---

## 5. Novel ideas considered (not pursued)

| Idea | Why deferred |
|------|----------------|
| FMA-locked Horner codegen | Valid only after observable `acc` / checksum in binary |
| `llvm.loop.vectorize` metadata on pure_li while loops | Same prerequisite |
| Contract-guided “do not DCE” for `decreases` loops | Needs compiler design + human review; not a numerics algorithm |

---

## 6. Recommended follow-up (lic, not benchmarks)

1. **P1 — Bench oracle parity:** Pure_li `main.li` must export the same checksum as `horner_core.c` (e.g. return low bits of `acc`, `echo`, or `extern` sink) so `-O3` measures real work.
2. **P1 — PH-7e:** Re-benchmark after (1); then profile scalar float loop vs cpp (FMA, LICM, GVN).
3. **P2 — Policy:** Document fast-math + dead-pure-Li-accumulator interaction in compiler/bench docs.

Do **not** relax `threshold_ratio_cpp` in `catalog.toml`.

---

## 7. Commands

```bash
cd /path/to/li/benchmarks/harness && python3 bench.py --tier 1 --runs 3
otool -tv build/bench/horner_pure_li/horner_pure_li_li | sed -n '/_li_user_main:/,/^_/p'
```

---

## 8. Status

**Closed — negative autoresearch.** Valuable finding: red row is currently a **harness/oracle bug**, not evidence that novel Horner algorithms are required.
