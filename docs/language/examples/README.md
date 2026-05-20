# Li example sources for shareable code images

Vendored **real** snippets (paths noted in each file header). Regenerate editor PNGs:

```bash
pip install pillow   # once per environment
python3 scripts/render-li-code-image.py --all
```

| Source file | Output PNG | Origin |
|-------------|------------|--------|
| `object_encapsulation.li` | `../assets/li-code-encapsulation-editor.png` | `lic` `li-tests/encapsulation/*` |
| `parallel_with_disjoint.li` | `../assets/li-code-decorators-editor.png` | `lic` `li-tests/decorators/parallel_with_disjoint.li` |
| `csv_ingest_smoke.li` | `../assets/li-code-ingest-editor.png` | `benchmarks` `scripts/ingest/csv_ingest_smoke.li` |

Highlighting is provided by `scripts/render-li-code-image.py` (Pygments `LiLexer` + VS Code–style colors). When Li grammar changes, extend the lexer in that script — no separate highlighter package yet.
