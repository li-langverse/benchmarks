# Numerics study reports

Place one markdown study per numerics PR or research cycle:

`YYYY-MM-DD-<short-slug>.md`

Use the sections in [research-methodology.md](../research-methodology.md) (problem, SOTA survey, method, quality table, evidence links).

For **novel algorithms**, also add `../algorithms/<slug>.md` from [algorithm-note-template.md](../algorithm-note-template.md).

Validate before opening PR:

```bash
python3 scripts/numerics-evidence-checklist.py --study docs/numerics/studies/YYYY-MM-DD-slug.md
```
