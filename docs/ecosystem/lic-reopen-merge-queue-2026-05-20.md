# lic merge queue (reopened 2026-05-20)

**Requested merge order** (rebase each onto `main` after the previous merge):

| Order | PR | Branch | Status (2026-05-20) |
|------|-----|--------|----------------------|
| 1 | [#70](https://github.com/li-langverse/lic/pull/70) | `cursor/enforce-strict-ensures-57b4` | **Merged** — E0303 strict `ensures` |
| 2 | [#71](https://github.com/li-langverse/lic/pull/71) | `cursor/scalar-precision-types-57b4` | **Merged** — scalar precision types |
| 3 | [#69](https://github.com/li-langverse/lic/pull/69) | `cursor/fix-import-multiline-params-57b4` | **Merged** — workspace imports + multiline `def` |
| 4 | [#75](https://github.com/li-langverse/lic/pull/75) | `cursor/rigid-var-param-57b4` | **Merged** — docs-only (implementation via #69); replaces closed #68 |
| 5 | [#72](https://github.com/li-langverse/lic/pull/72) | `cursor/ph-h-http-p0-and-li-http-54aa` | **Open** — CI fix: `import_parse` local fixture (`c2913db`) |
| 6 | [#73](https://github.com/li-langverse/lic/pull/73) | `cursor/object-field-mir-54aa` | **Merged** — MIR object fields (`ce42928` on `main`) |

**Merge discipline:** Never delete progress when merging or rebasing — integrate both sides (union of features, regenerate generated files). Do not close PRs to “clean the queue” without landing or cherry-picking their commits. See [merge-conflict-resolution.md](merge-conflict-resolution.md) and skill `resolve-merge-conflicts`.

**Push:** `git push "https://x-access-token:$(gh auth token)@github.com/li-langverse/lic.git" <branch>` when `cursor[bot]` gets 403.

**#72 import_parse:** PR enforces resolution for all imports (not only `std.*`). Test uses `li-tests/encapsulation/import_fixture.li` instead of placeholder `std_math`.
