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

### 1. Build lic and run the GPU suite

```bash
git clone https://github.com/li-langverse/lic.git
cd lic
./scripts/build.sh

# NVIDIA + CUDA example
export CUDA_HOME=/usr/lib/cuda   # or your CUDA install
./scripts/bench-lig-gpu-suite.sh

# Apple Silicon — on macOS with Metal toolchain when available
# LIG_EMIT_METAL=1 ./scripts/bench-lig-gpu-suite.sh
```

Results land in `lic/benchmarks/results/lig-gpu-suite-latest.json` (and optionally `lig-gpu-suite-honest.json`).

### 2. Scaffold the contribution folder (benchmarks repo)

```bash
git clone https://github.com/li-langverse/benchmarks.git
cd benchmarks

LIC_ROOT=../lic \
CONTRIBUTOR_GITHUB=your-github-handle \
CPU_MODEL="Apple M1 Pro" \
./scripts/ingest/submit-gpu-contribution.sh apple-m1-macos "Apple M1 Pro (Metal)"
```

For anonymous donation:

```bash
ANONYMOUS_OK=1 LIC_ROOT=../lic ./scripts/ingest/submit-gpu-contribution.sh nvidia-rtx-3090-linux "NVIDIA GeForce RTX 3090"
```

### 3. Open a PR

```bash
git checkout -b donate/nvidia-rtx-3090-linux
git add data/gpu-contributions/nvidia-rtx-3090-linux/
git commit -m "feat(gpu): donate RTX 3090 Linux GPU matrix"
git push -u origin HEAD
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
