# Li language surface (benchmarks docs)

Educational material for **social sharing** and onboarding. **Normative compiler grammar** lives in [`lic`](https://github.com/li-langverse/lic); when the two diverge, **`lic` wins** — open an issue if this tree is stale.

| Doc | Purpose |
|-----|---------|
| [style-types-and-classes.md](style-types-and-classes.md) | **PascalCase** types, **camelCase** members; real `object` encapsulation from `lic` |
| [execution-decorators-intro.md](execution-decorators-intro.md) | `@cpu` / `@parallel` from `lic` tests + `std/execution/decorators.li` |
| [examples/README.md](examples/README.md) | Vendored `.li` sources + how to generate PNGs locally |

## Shareable code-editor images (local only — not in git)

PNG screenshots are **syntax-highlighted source** (dark editor chrome). They are **generated on your machine** and saved under `docs/language/assets/` (gitignored).

```bash
pip install -r scripts/requirements-docs-visual.txt
python3 scripts/render-li-code-image.py --all
```

| Output file (local) | What it shows |
|---------------------|----------------|
| `docs/language/assets/li-code-encapsulation-editor.png` | `type Point` / `Vault` with `public` / `private` fields (`lic` encapsulation tests) |
| `docs/language/assets/li-code-decorators-editor.png` | `@cpu` + `@parallel` on a `parallel for` (`lic` `parallel_with_disjoint.li`) |
| `docs/language/assets/li-code-ingest-editor.png` | Benchmark CSV ingest with contracts (PH-IO-4) |

Highlighting: [`scripts/render-li-code-image.py`](../../scripts/render-li-code-image.py) — extend `LiLexer` when new keywords land.
