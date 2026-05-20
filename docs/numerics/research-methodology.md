# Li numerics research methodology

**Audience:** agents and human researchers working on **lic** physics/math kernels, **li-std-*** numerics packages, and **benchmarks** catalog rows.

**Philosophy:** [ecosystem-first](../ecosystem/ecosystem-first.md) — use org harness and visuals before inventing ad-hoc measurement. **Vision:** [vision-and-roadmap](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md) (PH-5b benchmark posture, PH-7e pure-Li performance). **Standards:** [engineering-standards](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md).

**SOTA / simulation breadth:** [sota-comparison-matrix.md](./sota-comparison-matrix.md) — small vs large N, memory, long horizons, and how field SOTA (engines, MD codes, CFD) maps to catalog tiers **without overclaiming** the dashboard.

---

## Two research modes

| Mode | Goal | Novelty |
|------|------|---------|
| **SOTA survey** | Adopt or adapt proven numerical recipes and reference implementations | Low — cite sources; match or beat oracle |
| **Autoresearch** | Propose new discretizations, solvers, fusion patterns, or Li-specific algorithms | High — must be **documented for verification** and pass quality gates |

Both modes share the same **evidence pack** and **quality criteria**. Autoresearch adds mandatory **algorithm notes** and human-review labels.

---

## SOTA survey (Mode A)

1. **Problem definition** — PDE/ODE, constraints, units, expected invariants (energy, mass, divergence-free, etc.).
2. **Literature & recipes** — textbooks (e.g. Hairer, LeVeque, Trefethen), survey papers, and **reference code** (PETSc, Eigen, FFTW, reference MD codes, Julia/Rust crates used in org benches).
3. **Implementation map** — where logic lives in Li (`lic/packages/`, `benchmarks/tier*`, shared `common/*_core.c` oracle).
4. **Stability analysis** — CFL/DL condition, stiffness, symplectic vs dissipative choice, known failure modes.
5. **Complexity** — asymptotic cost, memory, vectorization/SIMD opportunities in pure-Li path.
6. **Benchmark binding** — tier-0 correctness/stability, tier-1 micro, tier-2 physics; `catalog.toml` row + ingest.

**Learned from:** document **2–4** concrete references (paper URL, book section, upstream file path).

---

## Autoresearch (Mode B)

Agents **may** invent new equations, splittings, preconditioners, or Li-only fusion — when survey SOTA is insufficient for PH goals.

**Allowed:**

- New temporal integrators, limiters, or preconditioners with written derivation
- Li-specific IR/codegen patterns that preserve stability while improving speed
- Multi-physics coupling schemes justified by invariants

**Not allowed without human approval:**

- Merging without an **algorithm note** and **evidence pack**
- Weakening `threshold_ratio_cpp`, tier-0 tolerances, or CVE/stability tests
- Claiming improvement from a single micro-benchmark while physics regresses
- Undocumented magic constants or “works on my grid” fixes

**Verification path for novel work:**

1. Publish `docs/numerics/algorithms/<slug>.md` from [algorithm-note-template.md](./algorithm-note-template.md)
2. Label PR `novel-algorithm` (and `numerics-research` if org labels exist)
3. Request review from someone who can check stability proofs / order of accuracy
4. Attach reproducible study under `docs/numerics/studies/`

---

## Quality criteria (acceptance)

A change is an **improvement** only if **at least one** primary axis improves and **no** locked axis regresses.

| Axis | Primary metrics | Regression = reject |
|------|-----------------|---------------------|
| **Stability** | tier-0; energy drift plots; `md_stability_by_lang`; no NaN/ blow-up in GIFs | New failure vs cpp oracle |
| **Speed** | `wall_time`, `ratio_vs_cpp` vs `catalog.toml` threshold | Slower than threshold or prior green row |
| **Accuracy** | L2/L∞ vs fine reference, conserved quantities, RMSE on oracles | Error norm worse at same resolution |
| **Memory** | peak RSS / allocations (when relevant) | >10% regression without speed trade documented |

**Locked axes** for a given PR are those listed in the PR’s study doc. Default: stability + accuracy are never traded away for speed unless the study explicitly argues otherwise and a human approves.

---

## Evidence pack (required)

Every numerics PR must include or link:

| Artifact | Path / tool |
|----------|-------------|
| **Study report** | `docs/numerics/studies/YYYY-MM-DD-<slug>.md` |
| **Performance** | `lic/benchmarks/harness/bench.py` results; dashboard ingest |
| **Stability** | tier-0 + energy/time-series PNGs |
| **Real-world / physics** | tier-2 benches; **GIF/PNG** via `render-benchmark-visuals.sh` |
| **Summary plots** | speed bars, speedup vs cpp, stability-by-lang |
| **Animations** | MD/grid movies where applicable (vision validation) |

Run locally:

```bash
# lic
cd lic/benchmarks/harness && python3 bench.py --help

# benchmarks (after lic results)
cd benchmarks
LIC_ROOT=../lic ./scripts/render-benchmark-visuals.sh
./scripts/benchmark-failures-report.sh
python3 scripts/numerics-evidence-checklist.py --study docs/numerics/studies/YYYY-MM-DD-slug.md
```

**Dashboard:** https://li-langverse.github.io/benchmarks/

---

## Oracle policy

**cpp / rust / julia** on shared `common/*_core.c` are the **physics-shape oracle**. Li must match morphology and stability; beating wall_time is secondary until shape is correct.

Pure-Li paths (`horner_pure_li`, future tier-1) are judged against cpp for **speed** with separate codegen work (PH-7e).

---

## Catalog & ingest

1. Implement kernel under `lic/benchmarks/tier*/` or package
2. Add `[[benchmark]]` in `benchmarks/catalog.toml`
3. `./scripts/ingest/ingest-lic.sh` with `LIC_ROOT`
4. Do not duplicate harness into **benchmarks**

---

## Related skills & automations

- Skill **`research-li-numerics`** — agent checklist (SOTA + autoresearch)
- Skill **`numerics-autoresearch`** — stricter gates for novel algorithms
- Automation **`benchmark-visual-validation`** — vision on GIFs/PNGs
- Automation **`failed-benchmarks-maintainer`** — red row fixes
- **lic** [numerical policy](https://github.com/li-langverse/lic/blob/main/docs/physics/numerical-policy.md) (when present on `main`)
