#!/usr/bin/env python3
"""Build data/latest/lig-gpu-matrix.json for dashboard-next GPU matrix page."""

from __future__ import annotations

import json
import platform
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "latest" / "lig-gpu-matrix.json"

BACKEND_ORDER = ["li_native", "cuda", "vulkan", "hip", "metal"]
DISPLAY_BACKENDS = {
    "cuda": "CUDA",
    "vulkan": "Vulkan (WebGPU/SPIR-V)",
    "hip": "HIP (AMD)",
    "metal": "Metal (Apple)",
    "li_native": "Li native (CPU)",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def host_cpu_chip() -> dict[str, Any]:
    return {
        "chip_id": "host_cpu",
        "kind": "cpu",
        "label": "Host CPU",
        "model": platform.processor() or "unknown",
        "platform": platform.platform(),
        "visible": True,
    }


def gpu_chips(suite: dict[str, Any]) -> list[dict[str, Any]]:
    chips: list[dict[str, Any]] = [host_cpu_chip()]
    gpu = suite.get("gpu") or {}
    if gpu.get("visible"):
        chips.append(
            {
                "chip_id": "nvidia_lab",
                "kind": "gpu",
                "vendor": "nvidia",
                "label": str(gpu.get("name") or "NVIDIA GPU"),
                "model": gpu.get("name"),
                "driver_version": gpu.get("driver_version"),
                "compute_capability": gpu.get("compute_capability"),
                "memory_total_mib": gpu.get("memory_total_mib"),
                "visible": True,
            }
        )
    else:
        chips.append(
            {
                "chip_id": "nvidia_lab",
                "kind": "gpu",
                "vendor": "nvidia",
                "label": "NVIDIA GPU (not visible)",
                "visible": False,
            }
        )

    backend_visible = {b["backend"]: b.get("hardware_visible") for b in suite.get("backends", [])}
    chips.append(
        {
            "chip_id": "amd_lab",
            "kind": "gpu",
            "vendor": "amd",
            "label": "AMD ROCm GPU",
            "visible": bool(backend_visible.get("hip")),
            "backend": "hip",
        }
    )
    chips.append(
        {
            "chip_id": "apple_lab",
            "kind": "gpu",
            "vendor": "apple",
            "label": "Apple Silicon (Metal)",
            "visible": bool(backend_visible.get("metal")),
            "backend": "metal",
        }
    )
    return chips


def honest_kernel_map(honest: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not honest:
        return {}
    out: dict[str, dict[str, Any]] = {}
    parity = honest.get("parity") or {}
    for k in parity.get("kernels") or []:
        kid = k.get("kernel_id")
        if kid:
            out[str(kid)] = k
    top_kid = parity.get("kernel_id")
    if top_kid and top_kid not in out:
        out[str(top_kid)] = {
            "kernel_id": top_kid,
            "cpu_sec": parity.get("cpu_sec"),
            "validity_gate_pass": parity.get("validity_gate_pass"),
            "validity_ratio": parity.get("validity_ratio"),
            "validity_min": parity.get("validity_min"),
            "compile_ok": parity.get("compile_ok"),
            "status": honest.get("status", "pilot"),
        }
    return out


def ns_to_sec(value: Any) -> float | None:
    if value is None or value == "N/A":
        return None
    try:
        return float(value) / 1e9
    except (TypeError, ValueError):
        return None


def merge_honest_timings(
    workload_id: str,
    honest_kernels: dict[str, dict[str, Any]],
    honest_root: dict[str, Any] | None,
) -> dict[str, Any]:
    overlay: dict[str, Any] = {}
    hk = honest_kernels.get(workload_id)
    if hk:
        overlay["li_native"] = {
            "cpu_sec": hk.get("cpu_sec"),
            "status": hk.get("status", "unknown"),
            "validity_gate_pass": hk.get("validity_gate_pass"),
            "validity_ratio": hk.get("validity_ratio"),
            "validity_min": hk.get("validity_min"),
            "compile_ok": hk.get("compile_ok"),
        }
    if honest_root and workload_id == (honest_root.get("parity") or {}).get("kernel_id"):
        cuda_sec = ns_to_sec(honest_root.get("gpu_timing_ns") or honest_root.get("cuda_timing_ns"))
        overlay["cuda"] = {
            "gpu_sec": cuda_sec,
            "gpu_timing_ns": honest_root.get("gpu_timing_ns") or honest_root.get("cuda_timing_ns"),
            "status": honest_root.get("status", "cuda_device_pilot"),
            "vulkan_dispatch": honest_root.get("vulkan_dispatch"),
            "validity_gate_pass": (honest_root.get("parity") or {}).get("validity_gate_pass"),
        }
        overlay["vulkan"] = {
            "status": honest_root.get("vulkan_dispatch", "not_timed"),
            "gpu_sec": None,
            "note": honest_root.get("note"),
        }
    return overlay


def cell_to_backend_entry(cell: dict[str, Any]) -> dict[str, Any]:
    backend = cell.get("backend")
    if backend == "webgpu":
        backend = "vulkan"
    return {
        "backend": backend,
        "status": cell.get("status"),
        "gpu_execution_status": cell.get("gpu_execution_status"),
        "reason": cell.get("reason"),
        "kernel_id": cell.get("kernel_id"),
        "cpu_sec": cell.get("cpu_sec"),
        "gpu_sec": cell.get("gpu_sec") or ns_to_sec(cell.get("gpu_timing_ns")),
        "gpu_timing_ns": cell.get("gpu_timing_ns"),
        "validity_gate_pass": cell.get("validity_gate_pass"),
    }


def build_rows(suite: dict[str, Any], honest: dict[str, Any] | None) -> list[dict[str, Any]]:
    honest_kernels = honest_kernel_map(honest)
    grouped: dict[tuple[str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    meta: dict[tuple[str, str], dict[str, Any]] = {}

    for cell in suite.get("matrix") or []:
        key = (cell["workload_kind"], cell["workload_id"])
        entry = cell_to_backend_entry(cell)
        backend = entry.pop("backend")
        grouped[key][backend] = entry
        if key not in meta:
            meta[key] = {
                "workload_kind": cell["workload_kind"],
                "workload_id": cell["workload_id"],
                "label": cell["workload_id"].split(".")[-1],
            }

    rows: list[dict[str, Any]] = []
    for key, backends in sorted(grouped.items(), key=lambda x: x[0][1]):
        workload_id = key[1]
        overlay = merge_honest_timings(workload_id, honest_kernels, honest)

        li_native = overlay.get("li_native") or backends.get("li_native") or {}
        if not li_native and "cuda" in backends and backends["cuda"].get("status") == "li_smoke_cpu_only":
            li_native = {
                "status": "li_smoke_cpu_only",
                "cpu_sec": None,
                "validity_gate_pass": None,
            }

        merged_backends: dict[str, Any] = {}
        for bid in BACKEND_ORDER:
            if bid == "li_native":
                base = li_native
            else:
                base = overlay.get(bid) or backends.get(bid) or {}
            if not base:
                continue
            merged_backends[bid] = {
                "label": DISPLAY_BACKENDS[bid],
                "cpu_sec": base.get("cpu_sec"),
                "gpu_sec": base.get("gpu_sec"),
                "gpu_timing_ns": base.get("gpu_timing_ns"),
                "status": base.get("status"),
                "gpu_execution_status": base.get("gpu_execution_status"),
                "reason": base.get("reason"),
                "validity_gate_pass": base.get("validity_gate_pass"),
                "validity_ratio": base.get("validity_ratio"),
                "compile_ok": base.get("compile_ok"),
                "note": base.get("note"),
            }

        rows.append({**meta[key], "backends": merged_backends})

    return rows


def chip_diagram_series(
    rows: list[dict[str, Any]], chip_id: str, backend_key: str, field: str
) -> list[dict[str, Any]]:
    series: list[dict[str, Any]] = []
    for row in rows:
        b = row.get("backends", {}).get(backend_key) or {}
        val = b.get(field)
        if val is None:
            continue
        try:
            fval = float(val)
        except (TypeError, ValueError):
            continue
        series.append(
            {
                "workload_id": row["workload_id"],
                "label": row.get("label") or row["workload_id"],
                "value_sec": fval,
                "validity_gate_pass": b.get("validity_gate_pass"),
                "status": b.get("status"),
            }
        )
    series.sort(key=lambda x: x["value_sec"], reverse=True)
    return series[:24]


def build_matrix(suite_path: Path, honest_path: Path | None) -> dict[str, Any]:
    suite = load_json(suite_path)
    honest = load_json(honest_path) if honest_path and honest_path.is_file() else None
    rows = build_rows(suite, honest)
    chips = gpu_chips(suite)

    status_counts = Counter()
    for row in rows:
        for b in row.get("backends", {}).values():
            status_counts[str(b.get("status") or "unknown")] += 1

    timed_cpu = sum(
        1
        for r in rows
        if (r.get("backends", {}).get("li_native") or {}).get("cpu_sec") is not None
    )
    timed_cuda = sum(
        1
        for r in rows
        if (r.get("backends", {}).get("cuda") or {}).get("gpu_sec") is not None
    )
    timed_vulkan = sum(
        1
        for r in rows
        if (r.get("backends", {}).get("vulkan") or {}).get("gpu_sec") is not None
    )

    return {
        "schema": "benchmarks/lig-gpu-matrix/v1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sources": {
            "lig_gpu_suite": str(suite_path.relative_to(ROOT))
            if suite_path.is_relative_to(ROOT)
            else str(suite_path),
            "lig_gpu_honest": str(honest_path.relative_to(ROOT))
            if honest_path and honest_path.is_relative_to(ROOT)
            else (str(honest_path) if honest_path else ""),
        },
        "host_os": suite.get("host_os") or platform.system(),
        "gpu": suite.get("gpu"),
        "backends": suite.get("backends"),
        "summary": {
            **(suite.get("summary") or {}),
            "dashboard_workloads": len(rows),
            "timed_cpu_rows": timed_cpu,
            "timed_cuda_rows": timed_cuda,
            "timed_vulkan_rows": timed_vulkan,
            "backend_status_counts": dict(status_counts),
        },
        "possible_now": suite.get("possible_now"),
        "funding_gaps": suite.get("funding_gaps"),
        "honest_pilot": {
            "status": honest.get("status") if honest else None,
            "gpu_timing_ns": honest.get("gpu_timing_ns") if honest else None,
            "note": honest.get("note") if honest else None,
        },
        "chips": chips,
        "diagrams": {
            "host_cpu": {
                "chip_id": "host_cpu",
                "title": "Host CPU — Li native wall time",
                "backend": "li_native",
                "field": "cpu_sec",
                "unit": "s",
                "series": chip_diagram_series(rows, "host_cpu", "li_native", "cpu_sec"),
            },
            "nvidia_gpu": {
                "chip_id": "nvidia_lab",
                "title": "NVIDIA GPU — CUDA device time",
                "backend": "cuda",
                "field": "gpu_sec",
                "unit": "s",
                "series": chip_diagram_series(rows, "nvidia_lab", "cuda", "gpu_sec"),
            },
            "vulkan_gpu": {
                "chip_id": "nvidia_lab",
                "title": "Vulkan / WebGPU dispatch",
                "backend": "vulkan",
                "field": "gpu_sec",
                "unit": "s",
                "series": chip_diagram_series(rows, "nvidia_lab", "vulkan", "gpu_sec"),
            },
            "amd_gpu": {
                "chip_id": "amd_lab",
                "title": "AMD ROCm (HIP) — pending lab hardware",
                "backend": "hip",
                "field": "gpu_sec",
                "unit": "s",
                "series": chip_diagram_series(rows, "amd_lab", "hip", "gpu_sec"),
            },
            "apple_gpu": {
                "chip_id": "apple_lab",
                "title": "Apple Metal — pending macOS lab node",
                "backend": "metal",
                "field": "gpu_sec",
                "unit": "s",
                "series": chip_diagram_series(rows, "apple_lab", "metal", "gpu_sec"),
            },
        },
        "rows": rows,
    }


def resolve_inputs() -> tuple[Path, Path | None]:
    suite = ROOT / "data" / "latest" / "sources" / "lig-gpu-suite-latest.json"
    honest = ROOT / "data" / "latest" / "sources" / "lig-gpu-suite-honest.json"
    lic_root = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if lic_root:
        alt_suite = lic_root / "benchmarks" / "results" / "lig-gpu-suite-latest.json"
        alt_honest = lic_root / "benchmarks" / "results" / "lig-gpu-suite-honest.json"
        if alt_suite.is_file():
            suite = alt_suite
        if alt_honest.is_file():
            honest = alt_honest
    if not suite.is_file():
        fallback = (
            ROOT.parent
            / "lic-gpu-bench-5b3a"
            / "benchmarks"
            / "results"
            / "lig-gpu-suite-latest.json"
        )
        if fallback.is_file():
            suite = fallback
    return suite, honest if honest.is_file() else None


def main() -> int:
    suite_path, honest_path = resolve_inputs()
    if not suite_path.is_file():
        print(f"lig-gpu-suite source missing: {suite_path}", file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = build_matrix(suite_path, honest_path)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(payload['rows'])} workloads)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
