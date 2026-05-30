# Study: num_integ_rk4 autoresearch (negative result)

**Date:** 2026-05-30  
**Mode:** Autoresearch (B) → closed as negative  
**Target:** `num_integ_rk4` — largest near-threshold tier-1 row (1.083× cpp)  
**Agent:** autoresearch proactive pass v10 (li-langverse)  
**north_star_fit:** blazingly-fast (PH-5b) + provable — shared-oracle harmonic oscillator; no novel method required

---

## 1. Hypothesis

| ID | Hypothesis | Falsifiable metric |
|----|------------|-------------------|
| H1 | A **novel** explicit integrator (low-storage RK, fused Butcher stages, or Li-specific stage reorder) closes the 1.083× gap vs cpp while preserving oracle checksum. | `ratio_vs_cpp` ≤ 1.0 with `li_num_integ_rk4_checksum()` parity vs cpp. |
| H2 | The gap is caused by missing SOTA classical RK4 in the harness (wrong discretization). | Li and cpp must diverge in stage count or Butcher coefficients — falsified if cores match. |

---

## 2. SOTA survey (Mode A — sufficient)

**Problem:** Harmonic oscillator \(y'' = -y\), converted to first-order; 200k steps, \(\Delta t = 2\times10^{-4}\); classical RK4 (Dormand–Prince family member with fixed 4 stages).

**Learned from:**

1. **Hairer, Nørsett, Wanner — *Solving ODEs I*** ([Springer](https://link.springer.com/book/10.1007/978-3-540-78862-1)) — classical RK4 as default explicit recipe for smooth non-stiff ODEs.
2. **Butcher (1964) / RK4 tableau** — standard 4-stage explicit method; no low-storage variant needed at N=200k fixed steps.
3. **Shared oracle** — `num_integ_rk4_core.c` implements identical Butcher tableau for cpp/rust/julia/li via `LI_EXTRA_C`.
4. **Li harness** — `li/main.li` is a thin FFI wrapper (`li_num_integ_rk4_kernel` + volatile checksum sink); no Li-authored stage loop.
5. **Dashboard (2026-05-30T10:00Z ingest)** — cpp 0.0012 s, li 0.0013 s → **1.083×**; all langs green, threshold 1.2.

**Conclusion:** Published RK4 is correct and already shared. The measured slack is **linkage / wrapper / compiler emit overhead**, not a missing numerical method. Autoresearch invention is out of scope until a **pure_li** RK4 kernel exists and shows algorithm-bound regression.

---

## 3. Experiments

```bash
cd ../lic/benchmarks/harness
python3 bench.py --tier 1 --only num_integ_rk4 --runs 3
```

**Ingested linux (summary.json @ 2026-05-30T10:00:49Z):**

| lang | wall_time (s) | vs cpp |
|------|---------------|--------|
| cpp | 0.0012 | 1.00× |
| rust | 0.0013 | 1.08× |
| julia | 0.0013 | 1.08× |
| li | 0.0013 | **1.083×** |

Rust/Julia share the same C core and show similar overhead → confirms **not** Li-specific algorithm gap.

---

## 4. Novel ideas considered (not pursued)

| Idea | Why rejected |
|------|--------------|
| Low-storage RK (3S*) | Different Butcher tableau → oracle parity break; SOTA for *memory*, not this microbench |
| FSAL / merged stages in Li source | Harness uses shared C; would require new pure_li variant + new catalog row |
| Adaptive step RK | Changes step count → incomparable wall_time vs fixed-step oracle |
| Symplectic split for harmonic oscillator | Different physics discretization; tier-2 `num_integ_symplectic` covers that class |

---

## 5. Quality table (no improvement shipped)

| Axis | Before | After autoresearch | Verdict |
|------|--------|-------------------|---------|
| Speed | 1.083× green | No novel kernel shipped | **No improvement** |
| Accuracy | shared checksum | unchanged | **Locked** |
| Stability | tier-1 pass | unchanged | **Locked** |

---

## 6. Recommended follow-up (not autoresearch)

| Action | Owner | Reason |
|--------|-------|--------|
| FFI / emit overhead trim on `LI_EXTRA_C` call path | **bench_improver** / codegen | Same gap in rust/julia wrappers |
| Optional **pure_li** RK4 microbench row | **numerics_researcher** Mode A | Prerequisite before any Li-native integrator autoresearch |
| Close stale swarm gap `gap-benchmark-red-num-integ-euler-tier1` | **benchmarks** | Row green on dashboard |

---

## 7. Visuals / plots

**N/A (tier-1 micro integrator).** No physics GIF or stability overlay required; speed evidence is wall_time tables above. Render after future pure_li integrator win:

```bash
LIC_ROOT=../lic ./scripts/render-benchmark-visuals.sh  # tier-2 only when applicable
```

Checklist visual gate: **BLOCKED — N/A** with reason documented (negative micro study, shared-oracle wrapper).

## 8. Commands + checklist

```bash
cd ../lic/benchmarks/harness
python3 bench.py --tier 1 --only num_integ_rk4 --runs 3

cd benchmarks
./scripts/benchmark-failures-report.sh
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/2026-05-30-num-integ-rk4-autoresearch-negative.md
```

---

## 9. Status

**Closed — negative autoresearch.** `num_integ_rk4` near-threshold slack is shared-oracle wrapper overhead, not evidence that classical RK4 is insufficient. Route to **bench_improver** for emit/FFI polish; defer pure-Li integrator invention until Mode A defines a `pure_li` catalog variant.
