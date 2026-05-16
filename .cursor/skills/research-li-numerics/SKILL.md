---
name: research-li-numerics
description: >-
  Research numerical methods for Li physics — survey references, document error
  bounds, pick tier-appropriate integrators, add stability benches. Use when
  adding physics kernels or numerical policy in lic.
---

# Research Li numerics

Canonical copy lives in **`lic`** at `.cursor/skills/research-li-numerics/SKILL.md`.

When working in **`li-langverse/benchmarks`**, after adding a `catalog.toml` row:

1. Ensure the kernel exists under `lic/benchmarks/tier2_physics/`
2. Run ingest: `./scripts/ingest/ingest-lic.sh` with `LIC_ROOT` pointing at `lic`
3. Follow the lic skill checklist for Tier-0 stability and `params.toml`

See [lic numerical policy](https://github.com/li-langverse/lic/blob/main/docs/physics/numerical-policy.md).
