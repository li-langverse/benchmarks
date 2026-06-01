# Physics codegen matrix benchmark

Compare **Cursor Auto vs Qwen 3.5-9B/20B** (Arm A) and **C++/Rust/Julia/Li token cost** (Arm B) on tier-2 PDE workloads.

## Sprint goal

[`li-cursor-agents/data/goal-directed-sprints/physics-codegen-matrix.md`](../../li-cursor-agents/data/goal-directed-sprints/physics-codegen-matrix.md)

## K8s detached worker

```bash
cd li-cursor-agents
export KUBECONFIG=~/.kube/config-homelab
export GH_TOKEN=... CURSOR_API_KEY=...
export PHYSICS_CODEGEN_MODELS=default,<qwen-9b>,<qwen-20b>
bash scripts/k8s-physics-codegen-readiness.sh
bash scripts/setup-engine-k8s-physics-codegen-matrix.sh
kubectl -n li-swarm logs -f deploy/li-physics-codegen-matrix
```

Deployment: `deploy/k8s/engine/deployment-physics-codegen-matrix.yaml` (dedicated PVC, `code_implementer`, `LI_SDK_LOG_SKIP_TOKEN_DELTAS=0`).

## Local goal-directed loop

```bash
cd li-cursor-agents
./scripts/goal-directed-loop.sh \
  --goal-file data/goal-directed-sprints/physics-codegen-matrix.md \
  --agent code_implementer \
  --cwd ../lic \
  --workflow-repo lic
```

## Results

`benchmarks/results/physics-codegen-matrix.json` — one row per (model, bench, lang) with `llm.thinking_tokens`, `validity.verify_within_1ulp`, `runtime.wall_time_s`.

## Harness

Pilot benches: `wave_equation_1d`, `heat_equation_2d`, `schrodinger_1d_barrier`. Full set: `TIER2_GROUP_PDE` in `scripts/bench_tier2_groups.py`.
