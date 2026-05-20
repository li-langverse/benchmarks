#!/usr/bin/env python3
"""Generate data/latest/competitive-status.json — HPC + world_engine + UE proxy posture."""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WORLD_BENCHES = frozenset(
    {
        "game_world_soa_10k",
        "game_replication_encode",
        "sim_physics_frame",
        "cloth_swing",
        "rigid_body_stack",
    }
)


def load_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text())


def merge_lic_perf(lic_root: Path) -> list[dict]:
    rows = load_csv(lic_root / "benchmarks/results/latest.csv")
    by_key: dict[tuple[str, str, str], dict] = {}
    for r in rows:
        by_key[(r.get("benchmark", ""), r.get("lang", ""), r.get("metric", "wall_time"))] = r
    for name in ("world_engine_full.csv", "ingest_world_gaming.csv"):
        for r in load_csv(lic_root / "benchmarks/results" / name):
            if r.get("scale") == "quick":
                continue
            key = (r.get("benchmark", ""), r.get("lang", ""), r.get("metric", "wall_time"))
            by_key[key] = r
    return list(by_key.values())


def ratio_status(ratio: float | None, threshold: float = 1.2) -> str:
    if ratio is None:
        return "unknown"
    if ratio <= threshold:
        return "green"
    if ratio <= threshold * 1.1:
        return "yellow"
    return "red"


def ue_proxy_status(li_ms: float | None, budget_ms: float | None) -> str:
    if li_ms is None or budget_ms is None or budget_ms <= 0:
        return "unknown"
    return ratio_status(li_ms / budget_ms, threshold=1.0)


def main() -> int:
    lic_root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "lic"
    validity = lic_root / "benchmarks/results/validity.json"
    engines = lic_root / "benchmarks/competitive/engines.toml"
    world_json = lic_root / "benchmarks/competitive/world-engine-latest.json"
    unreal_proxy = lic_root / "benchmarks/competitive/unreal-proxy-targets.json"
    catalog_path = ROOT / "catalog.toml"

    try:
        import tomllib

        engine_rows = tomllib.loads(engines.read_text()).get("engine", []) if engines.is_file() else []
        catalog = {b["id"]: b for b in tomllib.loads(catalog_path.read_text()).get("benchmark", [])}
    except Exception:
        engine_rows = []
        catalog = {}

    perf_rows = merge_lic_perf(lic_root)
    val = load_json(validity)
    world_doc = load_json(world_json)
    proxy_doc = load_json(unreal_proxy)

    by_bench: dict[str, dict] = {}
    for r in perf_rows:
        if r.get("metric") != "wall_time":
            continue
        bid = r["benchmark"]
        by_bench.setdefault(bid, {})[r["lang"]] = {
            "wall_s": float(r["value"]),
            "stdev": float(r["value_stdev"]) if r.get("value_stdev") else None,
            "runs": int(r["timing_runs"]) if r.get("timing_runs") else None,
        }

    val_by = val.get("by_benchmark", {})
    harness: list[dict] = []
    for bid in sorted(set(by_bench) | set(val_by) | WORLD_BENCHES):
        langs = by_bench.get(bid, {})
        li = langs.get("li", {}).get("wall_s")
        cpp = langs.get("cpp", {}).get("wall_s")
        npy = langs.get("numpy", {}).get("wall_s")
        ratio_li = (li / cpp) if li and cpp and cpp > 0 else None
        ratio_np = (npy / cpp) if npy and cpp and cpp > 0 else None
        vinfo = val_by.get(bid, {})
        v_langs = vinfo.get("langs", {})
        validity_pass = (
            all(
                v_langs.get(lang, {}).get("passed", False)
                for lang in ("cpp", "li", "numpy")
                if lang in v_langs
            )
            if v_langs
            else None
        )
        cfg = catalog.get(bid, {})
        wc = vinfo.get("workload_class") or cfg.get("workload_class", "unknown")
        if bid in world_doc.get("full", {}) and cfg.get("workload_class_full"):
            wc = cfg.get("workload_class_full", wc)
        tgt = proxy_doc.get("targets", {}).get(bid, {})
        budget_ms = (
            cfg.get("unreal_proxy_budget_ms")
            or tgt.get("aspirational_budget_ms_at_60fps")
            or tgt.get("aspirational_budget_ms")
            or tgt.get("aspirational_budget_ms_per_tick")
        )
        li_ms = li * 1000.0 if li is not None else None
        harness.append(
            {
                "benchmark": bid,
                "workload_class": wc,
                "perf_li_vs_cpp": round(ratio_li, 4) if ratio_li else None,
                "perf_numpy_vs_cpp": round(ratio_np, 4) if ratio_np else None,
                "perf_status_li": ratio_status(ratio_li),
                "validity_all_langs": validity_pass,
                "validity_detail": v_langs,
                "wall_time_s": langs,
                "ue_proxy_budget_ms": budget_ms,
                "li_ms": round(li_ms, 4) if li_ms is not None else None,
                "vs_ue_proxy_ratio": round(li_ms / budget_ms, 4)
                if li_ms is not None and budget_ms
                else None,
                "ue_proxy_status": ue_proxy_status(li_ms, float(budget_ms) if budget_ms else None),
            }
        )

    world_engine = [h for h in harness if h["workload_class"] == "world_engine"]
    gaming_full = [h for h in harness if h["workload_class"] == "gaming_full"]
    full = [h for h in harness if h["workload_class"] == "full"]
    v0 = [h for h in harness if h["workload_class"] == "v0_gaming"]
    stub = [h for h in harness if h["workload_class"] == "pure_li_stub"]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "lic_perf_csv": "latest.csv + world_engine_full.csv",
            "validity_json": str(validity),
            "engines_toml": str(engines),
            "world_engine_json": str(world_json),
            "unreal_proxy_json": str(unreal_proxy),
        },
        "summary": {
            "harness_benches": len(harness),
            "world_engine_workloads": len(world_engine),
            "gaming_full_workloads": len(gaming_full),
            "full_workloads": len(full),
            "v0_gaming_workloads": len(v0),
            "pure_li_stub": len(stub),
            "perf_green_li": sum(1 for h in harness if h["perf_status_li"] == "green"),
            "ue_proxy_green": sum(1 for h in harness if h.get("ue_proxy_status") == "green"),
            "validity_pass_all": sum(1 for h in harness if h["validity_all_langs"] is True),
            "validity_fail": sum(1 for h in harness if h["validity_all_langs"] is False),
        },
        "harness": harness,
        "world_engine": world_engine,
        "gaming_full": gaming_full,
        "engines": engine_rows,
        "agentic_pillars": proxy_doc.get("agentic_parity_pillars", []),
        "claims_allowed": [
            "Li/cpp ratio on full/world_engine with validity pass",
            "Li ms under UE proxy budget (aspirational, not measured UE)",
            "Agent-native world.li + lic build workflow",
        ],
        "claims_forbidden": [
            "Dashboard green without validity.json pass",
            "Proxy budget labeled as measured UE5 CI",
            "Composable gates as render/ECS parity",
        ],
    }

    out = ROOT / "data/latest/competitive-status.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {out} ({report['summary']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
