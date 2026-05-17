# Numerics study reports

Place one markdown study per numerics PR or research cycle:

`YYYY-MM-DD-<short-slug>.md`

**Recent:**

- [2026-05-17 — `horner_pure_li` (red, pure-Li / PH-7e)](./2026-05-17-horner-pure-li-codegen.md)
- [2026-05-17 — near-limit tier-1/2 greens above 1.0× cpp](./2026-05-17-near-limit-tier12-sota.md)

Use the sections in [research-methodology.md](../research-methodology.md) (problem, SOTA survey, method, quality table, evidence links).

For **novel algorithms**, also add `../algorithms/<slug>.md` from [algorithm-note-template.md](../algorithm-note-template.md).

Validate before opening PR:

```bash
python3 scripts/numerics-evidence-checklist.py --study docs/numerics/studies/YYYY-MM-DD-slug.md
```
