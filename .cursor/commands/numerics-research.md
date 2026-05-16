# /numerics-research

Numerics research: SOTA survey + evidence pack (add **autoresearch** for novel algorithms).

**Skills:** `research-li-numerics` · `numerics-autoresearch` (novel only)

```bash
# 1. Read methodology
cat docs/numerics/research-methodology.md

# 2. Run benches + visuals (lic required)
cd ../lic/benchmarks/harness && python3 bench.py --help
cd -
LIC_ROOT=../lic ./scripts/render-benchmark-visuals.sh

# 3. Write study (+ algorithm note if novel)
# docs/numerics/studies/YYYY-MM-DD-slug.md
# docs/numerics/algorithms/slug.md   # --novel only

python3 scripts/numerics-evidence-checklist.py --study docs/numerics/studies/YYYY-MM-DD-slug.md
python3 scripts/numerics-evidence-checklist.py --study ... --algorithm ... --novel
```
