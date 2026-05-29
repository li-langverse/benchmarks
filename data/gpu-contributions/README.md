# GPU chip contributions

Each subdirectory is **one physical machine** (one GPU + host CPU). Do not mix chips in one folder.

| Slug | Status | Backend |
|------|--------|---------|
| [nvidia-rtx-3060-linux](./nvidia-rtx-3060-linux/) | measured (pilot) | CUDA |
| `nvidia-rtx-3090-linux` | **open slot** — [donate](../../docs/ecosystem/gpu-chip-contributions.md) | CUDA |
| `apple-m1-macos` | **open slot** — [donate](../../docs/ecosystem/gpu-chip-contributions.md) | Metal |
| `amd-rx-7900-linux` | **open slot** — [donate](../../docs/ecosystem/gpu-chip-contributions.md) | HIP |

**How to contribute:** [docs/ecosystem/gpu-chip-contributions.md](../../docs/ecosystem/gpu-chip-contributions.md)

```bash
LIC_ROOT=../lic ./scripts/ingest/submit-gpu-contribution.sh nvidia-rtx-3090-linux "NVIDIA GeForce RTX 3090"
```
