# Algorithm note: <short-name>

**Status:** draft | under-review | accepted  
**Authors:** (agent/human)  
**PR:** li-langverse/lic#…  
**Date:** YYYY-MM-DD  

---

## 1. Summary

One paragraph: what problem this solves and what is **novel** vs published SOTA.

---

## 2. Mathematical specification

### 2.1 Governing equations

Write continuous and discrete forms. Use consistent notation (state **u**, grid **h**, time **Δt**).

### 2.2 Assumptions

- Domain, boundary conditions, smoothness
- Regime (e.g. incompressible, stiff ODE, symplectic structure)

### 2.3 Algorithm (pseudocode)

```
# Step-by-step or numbered list
```

### 2.4 Stability / accuracy claims

| Claim | Argument |
|-------|----------|
| Order of accuracy | |
| CFL / stability limit | |
| Conservation / invariants | |
| Known limitations | |

---

## 3. Relation to SOTA

| Reference | What we reuse | What differs |
|-----------|---------------|--------------|
| | | |

**Learned from:** (2–4 citations with links)

---

## 4. Implementation map (Li)

| Component | Path |
|-----------|------|
| Kernel | `lic/...` |
| Bench | `lic/benchmarks/tier*/...` |
| Catalog id | `benchmarks/catalog.toml` → `id = "..."` |

---

## 5. Empirical validation (reproducible)

### 5.1 Performance

| Benchmark | Li | cpp | ratio | threshold | pass? |
|-----------|----|----|-------|-----------|-------|
| | | | | 1.2× | |

Commands:

```bash
# paste exact bench.py / ingest commands
```

### 5.2 Stability

- tier-0 results:
- Energy / invariant plots: (path or PR link)
- Long-time behavior:

### 5.3 Accuracy (if applicable)

- Reference solution:
- Error norms vs **h** / **Δt**:

### 5.4 Visual evidence

| Asset | Path / URL | Vision verdict |
|-------|------------|----------------|
| GIF | | PASS/FAIL |
| PNG overlay | | |

---

## 6. Verification checklist (for human reviewers)

- [ ] Equations match code
- [ ] Stability argument plausible or empirical sweep included
- [ ] No threshold/catalog weakening
- [ ] Repro commands work on clean checkout
- [ ] Regressions absent on locked axes (see study doc)

---

## 7. Open questions / future work

- 
