# lic merge queue (reopened 2026-05-20)

**Requested merge order** (rebase each onto `main` after the previous merge):

| Order | PR | Branch | Topic |
|------|-----|--------|--------|
| 1 | [#70](https://github.com/li-langverse/lic/pull/70) | `cursor/enforce-strict-ensures-57b4` | Strict contracts — vacuous `ensures` / E0303 |
| 2 | [#71](https://github.com/li-langverse/lic/pull/71) | `cursor/scalar-precision-types-57b4` | Scalar precision `float4`–`float512`, `int4`–`int512` |
| 3 | [#69](https://github.com/li-langverse/lic/pull/69) | `cursor/fix-import-multiline-params-57b4` | Workspace import members + multiline `def` params |
| 4 | [#68](https://github.com/li-langverse/lic/pull/68) | `cursor/rigid-var-param-57b4` | Physics rigid `var RigidBody` param |
| 5 | [#72](https://github.com/li-langverse/lic/pull/72) | `cursor/ph-h-http-p0-and-li-http-54aa` | Phase-H `li-http` + P0 stubs |
| 6 | [#73](https://github.com/li-langverse/lic/pull/73) | `cursor/object-field-mir-54aa` | MIR object field access |

**Agent note:** Reopened via `gh pr reopen`; push/rebase requires write access on `lic` (blocked for `cursor[bot]`). Human or org token: `git fetch origin pull/N/head && git rebase origin/main && git push`.

**#70 CI:** Last run had `build-and-test` / `build-and-test-macos` red — re-run after rebase on current `main`.
