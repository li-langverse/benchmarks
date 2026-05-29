# GPU chip contributions

Donate benchmark results from **your** machine so the public dashboard can compare CUDA, Metal, Vulkan, and HIP across real hardware — RTX 3060 vs 3090 vs Apple M1, and more.

**Dashboard:** [GPU chip matrix](https://li-langverse.github.io/benchmarks/gpu-matrix/)

## Rules (must follow for merge)

1. **One folder = one physical machine.** Never mix two GPUs or two hosts in one contribution.
2. **Slug naming:** lowercase, hyphens only — `{vendor}-{model}-{os}`, e.g. `nvidia-rtx-3090-linux`, `apple-m1-macos`, `amd-rx-7900-linux`.
3. **Required files** in `data/gpu-contributions/<chip-slug>/`:
   - `contribution.json` — manifest (schema `benchmarks/gpu-chip-contribution/v1`)
   - `lig-gpu-suite-latest.json` — output of the LiG full GPU suite reporter
   - `lig-gpu-suite-honest.json` — optional but recommended when you have pilot/honest timings
4. **Honesty:** do not edit timing fields by hand. Re-run the harness on your machine.
5. **Attribution:** set `contributor.github` **or** `contributor.anonymous_ok: true`.
6. **Validation:** PR must pass `python3 scripts/ingest/validate-gpu-contribution.py`.
7. **No secrets:** do not commit API keys, serial numbers, or home paths with usernames.

## Quick start (contributor)

### One command

From the **benchmarks** repo (with a sibling **lic** checkout, or set `LIC_ROOT`):

```bash
CONTRIBUTOR_GITHUB=your-handle ./scripts/donate-gpu-chip.sh nvidia-rtx-3090-linux
```

This will:

1. Build `lic` if needed (`SKIP_LIC_BUILD=1` to skip)
2. Run `./scripts/bench-lig-gpu-suite.sh` (or the harness fallback) on **your** machine
3. Create `data/gpu-contributions/<chip-slug>/`, validate, and rebuild `lig-gpu-matrix.json`

GPU name is auto-detected from `nvidia-smi` (Linux) or `system_profiler` (macOS). Override with a second argument:

```bash
./scripts/donate-gpu-chip.sh apple-m1-macos "Apple M1 Pro (Metal)"
```

Re-benchmark an existing donation:

```bash
GPU_CHIP_UPDATE=1 ./scripts/donate-gpu-chip.sh nvidia-rtx-3060-linux
```

Then open a PR:

```bash
git checkout -b donate/nvidia-rtx-3090-linux
git add data/gpu-contributions/nvidia-rtx-3090-linux/ data/latest/lig-gpu-matrix.json
git commit -m "feat(gpu): donate RTX 3090 Linux GPU matrix"
git push -u origin HEAD
```

### Manual steps (optional)

If you already ran the suite in `lic` and only need to copy artifacts:

```bash
LIC_ROOT=../lic ./scripts/ingest/submit-gpu-contribution.sh nvidia-rtx-3090-linux "NVIDIA GeForce RTX 3090"
```

CI validates the manifest and rebuilds `data/latest/lig-gpu-matrix.json`. Reviewers check:

- Slug matches directory name
- Suite JSON schema is `ph-hw/lig-full-gpu-suite/v1`
- Timings look plausible (no copy-paste from another chip folder)

## Manifest reference

```json
{
  "schema": "benchmarks/gpu-chip-contribution/v1",
  "chip_slug": "nvidia-rtx-3090-linux",
  "label": "NVIDIA GeForce RTX 3090",
  "vendor": "nvidia",
  "host_os": "Linux",
  "primary_backend": "cuda",
  "contributor": { "github": "your-handle" },
  "hardware": {
    "gpu_name": "NVIDIA GeForce RTX 3090",
    "cpu_model": "AMD Ryzen 9 5900X",
    "driver_version": "550.xx",
    "compute_capability": "8.6"
  },
  "artifacts": {
    "lig_gpu_suite": "lig-gpu-suite-latest.json",
    "lig_gpu_honest": "lig-gpu-suite-honest.json"
  },
  "submitted_at": "2026-05-29",
  "notes": "Optional free-text — driver/CUDA version, cooling, etc."
}
```

| Field | Values |
|-------|--------|
| `vendor` | `nvidia`, `amd`, `apple`, `intel`, `other` |
| `primary_backend` | `cuda`, `hip`, `metal`, `vulkan` |
| `host_os` | `Linux`, `macOS`, `Windows` |

## How ingest works

```
data/gpu-contributions/<slug>/
  contribution.json
  lig-gpu-suite-latest.json
        │
        ▼
scripts/ingest/build-lig-gpu-matrix.py
        │
        ▼
data/latest/lig-gpu-matrix.json  (schema v2, multi-chip)
        │
        ▼
dashboard-next /gpu-matrix/  (chip picker + per-chip tables)
```

Each contribution becomes one entry in `lig-gpu-matrix.json` → `contributions[]`. Open slots (M1, 3090, …) appear until someone donates that slug.

## Open slots we want

| Slug | Hardware | Backend |
|------|----------|---------|
| `nvidia-rtx-3090-linux` | RTX 3090 | CUDA |
| `apple-m1-macos` | Apple M1 | Metal |
| `apple-m2-macos` | Apple M2 / M2 Pro | Metal |
| `amd-rx-7900-linux` | RX 7900 XT/XTX | HIP |

Pick an unused slug or propose a new one in your PR description if your exact SKU is not listed.

## Related

- [benchmark honesty policy](../honesty/benchmark-dashboard.md)
- [PH-HW GPU suite in lic](https://github.com/li-langverse/lic/tree/main/benchmarks/competitive/lig-kernels.toml)
- `data/gpu-contributions/README.md` — index of donated chips
