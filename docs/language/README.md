# Li language surface (benchmarks docs)

Educational material for **social sharing** and onboarding. **Normative compiler grammar** lives in [`lic`](https://github.com/li-langverse/lic); when the two diverge, **`lic` wins** — open an issue if this tree is stale.

| Doc | Purpose |
|-----|---------|
| [style-types-and-classes.md](style-types-and-classes.md) | **PascalCase** types, **camelCase** members; real `object` encapsulation from `lic` |
| [execution-decorators-intro.md](execution-decorators-intro.md) | `@cpu` / `@parallel` from `lic` tests + `std/execution/decorators.li` |
| [examples/README.md](examples/README.md) | Vendored `.li` sources + how to regenerate PNGs |

## Shareable code-editor images

PNG screenshots are **syntax-highlighted source** (dark editor chrome), not marketing posters. Sources are under [`examples/`](examples/); regenerate after edits:

```bash
pip install -r scripts/requirements-docs-visual.txt
python3 scripts/render-li-code-image.py --all
```

| Image | What it shows |
|-------|----------------|
| [`li-code-encapsulation-editor.png`](assets/li-code-encapsulation-editor.png) | `type Point` / `Vault` with `public` / `private` fields (`lic` encapsulation tests) |
| [`li-code-decorators-editor.png`](assets/li-code-decorators-editor.png) | `@cpu` + `@parallel` on a `parallel for` (`lic` `parallel_with_disjoint.li`) |
| [`li-code-ingest-editor.png`](assets/li-code-ingest-editor.png) | Benchmark CSV ingest with contracts (`benchmarks` PH-IO-4) |

Highlighting: [`scripts/render-li-code-image.py`](../../scripts/render-li-code-image.py) — extend `LiLexer` when new keywords land; no separate highlighter crate yet.
