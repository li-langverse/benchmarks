# Li example sources for shareable code images

Sources match **`lic` / benchmarks** files that compile today (no banner comments in `.li` — provenance below).

```bash
pip install -r scripts/requirements-docs-visual.txt
python3 scripts/render-li-code-image.py --all
```

| Source file | Output PNG (gitignored) | Upstream |
|-------------|-------------------------|----------|
| `object_encapsulation.li` | `../assets/li-code-encapsulation-editor.png` | `lic` `li-tests/encapsulation/object_public_field.li` + `private_field_access.li` |
| `parallel_with_disjoint.li` | `../assets/li-code-decorators-editor.png` | `lic` `li-tests/decorators/parallel_with_disjoint.li` (exact) |
| `csv_ingest_smoke.li` | `../assets/li-code-ingest-editor.png` | `benchmarks` `scripts/ingest/csv_ingest_smoke.li` — `def`, `import std.io`, `raises IO, Alloc` (matches `lic` effects tests) |

Renderer: `scripts/render-li-code-image.py` — strips `#` lines from PNG output, tight width (default max 520px).
