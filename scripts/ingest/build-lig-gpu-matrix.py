#!/usr/bin/env python3
"""Build data/latest/lig-gpu-matrix.json from data/gpu-contributions/*/."""

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
CONTRIB_ROOT = ROOT / "data" / "gpu-contributions"
MANIFEST_SCHEMA = "benchmarks/gpu-chip-contribution/v1"

BACKEND_ORDER = ["li_native", "cuda", "vulkan", "hip", "metal"]
DISPLAY_BACKENDS = {
    "cuda": "CUDA",
    "vulkan": "Vulkan (WebGPU/SPIR-V)",
    "hip": "HIP (AMD)",
    "metal": "Metal (Apple)",
    "li_native": "Li native (CPU)",
}

OPEN_SLOTS = [
    {
        "chip_slug": "nvidia-rtx-3090-linux",
        "label": "NVIDIA GeForce RTX 3090",
        "vendor": "nvidia",
        "host_os": "Linux",
        "primary_backend": "cuda",
        "status": "open",
    },
    {
        "chip_slug": "apple-m1-macos",
        "label": "Apple M1 (Metal)",
        "vendor": "apple",
        "host_os": "macOS",
        "primary_backend": "metal",
        "status": "open",
    },
    {
        "chip_slug": "apple-m2-macos",
        "label": "Apple M2 / M2 Pro",
        "vendor": "apple",
        "host_os": "macOS",
        "primary_backend": "metal",
        "status": "open",
    },
    {
        "chip_slug": "amd-rx-7900-linux",
        "label": "AMD Radeon RX 7900 (ROCm)",
        "vendor": "amd",
        "host_os": "Linux",
        "primary_backend": "hip",
        "status": "open",
    },
]

CONTRIBUTION_POLICY = (
    "https://github.com/li-langverse/benchmarks/blob/main/docs/ecosystem/gpu-chip-contributions.md"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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
    primary_backend: str,
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
        gpu_ns = honest_root.get("gpu_timing_ns") or honest_root.get("cuda_timing_ns")
        if primary_backend == "cuda":
            overlay["cuda"] = {
                "gpu_sec": ns_to_sec(gpu_ns),
                "gpu_timing_ns": gpu_ns,
                "status": honest_root.get("status", "cuda_device_pilot"),
                "validity_gate_pass": (honest_root.get("parity") or {}).get("validity_gate_pass"),
            }
        elif primary_backend == "metal":
            metal_ns = honest_root.get("metal_timing_ns")
            if metal_ns not in (None, "N/A"):
                overlay["metal"] = {
                    "gpu_sec": ns_to_sec(metal_ns),
                    "gpu_timing_ns": metal_ns,
                    "status": honest_root.get("status", "metal_device_pilot"),
                }
        elif primary_backend == "hip":
            hip_ns = honest_root.get("hip_timing_ns")
            if hip_ns not in (None, "N/A"):
                overlay["hip"] = {
                    "gpu_sec": ns_to_sec(hip_ns),
                    "gpu_timing_ns": hip_ns,
                    "status": honest_root.get("status", "hip_device_pilot"),
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


def build_rows(
    suite: dict[str, Any],
    honest: dict[str, Any] | None,
    primary_backend: str,
) -> list[dict[str, Any]]:
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
        overlay = merge_honest_timings(workload_id, honest_kernels, honest, primary_backend)

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


def chip_diagram_series(rows: list[dict[str, Any]], backend_key: str, field: str) -> list[dict[str, Any]]:
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


def summary_for_rows(rows: list[dict[str, Any]], suite_summary: dict[str, Any]) -> dict[str, Any]:
    status_counts = Counter()
    for row in rows:
        for b in row.get("backends", {}).values():
            status_counts[str(b.get("status") or "unknown")] += 1

    return {
        **suite_summary,
        "dashboard_workloads": len(rows),
        "timed_cpu_rows": sum(
            1 for r in rows if (r.get("backends", {}).get("li_native") or {}).get("cpu_sec") is not None
        ),
        "timed_cuda_rows": sum(
            1 for r in rows if (r.get("backends", {}).get("cuda") or {}).get("gpu_sec") is not None
        ),
        "timed_vulkan_rows": sum(
            1 for r in rows if (r.get("backends", {}).get("vulkan") or {}).get("gpu_sec") is not None
        ),
        "timed_metal_rows": sum(
            1 for r in rows if (r.get("backends", {}).get("metal") or {}).get("gpu_sec") is not None
        ),
        "timed_hip_rows": sum(
            1 for r in rows if (r.get("backends", {}).get("hip") or {}).get("gpu_sec") is not None
        ),
        "backend_status_counts": dict(status_counts),
    }


def build_diagrams(rows: list[dict[str, Any]], primary_backend: str) -> dict[str, Any]:
    gpu_backend = primary_backend if primary_backend in ("cuda", "hip", "metal") else "cuda"
    return {
        "host_cpu": {
            "title": "Host CPU — Li native wall time",
            "backend": "li_native",
            "field": "cpu_sec",
            "unit": "s",
            "series": chip_diagram_series(rows, "li_native", "cpu_sec"),
        },
        "primary_gpu": {
            "title": f"{DISPLAY_BACKENDS.get(gpu_backend, gpu_backend)} device time",
            "backend": gpu_backend,
            "field": "gpu_sec",
            "unit": "s",
            "series": chip_diagram_series(rows, gpu_backend, "gpu_sec"),
        },
        "vulkan_gpu": {
            "title": "Vulkan / WebGPU dispatch",
            "backend": "vulkan",
            "field": "gpu_sec",
            "unit": "s",
            "series": chip_diagram_series(rows, "vulkan", "gpu_sec"),
        },
    }


def build_contribution(contrib_dir: Path) -> dict[str, Any]:
    manifest = load_json(contrib_dir / "contribution.json")
    artifacts = manifest.get("artifacts") or {}
    suite_path = contrib_dir / str(artifacts["lig_gpu_suite"])
    suite = load_json(suite_path)

    honest_path = None
    honest = None
    if artifacts.get("lig_gpu_honest"):
        honest_path = contrib_dir / str(artifacts["lig_gpu_honest"])
        if honest_path.is_file():
            honest = load_json(honest_path)

    primary_backend = str(manifest.get("primary_backend") or "cuda")
    rows = build_rows(suite, honest, primary_backend)
    hw = manifest.get("hardware") or {}
    gpu = suite.get("gpu") or {}

    return {
        "chip_slug": manifest["chip_slug"],
        "label": manifest["label"],
        "vendor": manifest.get("vendor"),
        "host_os": manifest.get("host_os") or suite.get("host_os"),
        "primary_backend": primary_backend,
        "contributor": manifest.get("contributor"),
        "submitted_at": manifest.get("submitted_at"),
        "notes": manifest.get("notes"),
        "hardware": {
            **hw,
            "gpu_name": hw.get("gpu_name") or gpu.get("name"),
            "driver_version": hw.get("driver_version") or gpu.get("driver_version"),
            "compute_capability": hw.get("compute_capability") or gpu.get("compute_capability"),
            "memory_total_mib": hw.get("memory_total_mib") or gpu.get("memory_total_mib"),
        },
        "sources": {
            "contribution_dir": rel_path(contrib_dir),
            "lig_gpu_suite": rel_path(suite_path),
            "lig_gpu_honest": rel_path(honest_path) if honest_path and honest_path.is_file() else "",
        },
        "gpu": gpu,
        "backends": suite.get("backends"),
        "summary": summary_for_rows(rows, suite.get("summary") or {}),
        "possible_now": suite.get("possible_now"),
        "funding_gaps": suite.get("funding_gaps"),
        "honest_pilot": {
            "status": honest.get("status") if honest else None,
            "gpu_timing_ns": honest.get("gpu_timing_ns") if honest else None,
            "note": honest.get("note") if honest else None,
        },
        "diagrams": build_diagrams(rows, primary_backend),
        "rows": rows,
    }


def cross_chip_compare(contributions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_workload: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"workload_id": "", "label": "", "chips": {}}
    )
    for contrib in contributions:
        slug = contrib["chip_slug"]
        backend = contrib["primary_backend"]
        for row in contrib["rows"]:
            wid = row["workload_id"]
            b = row.get("backends", {}).get(backend) or row.get("backends", {}).get("cuda") or {}
            gpu_sec = b.get("gpu_sec")
            cpu_b = row.get("backends", {}).get("li_native") or {}
            cpu_sec = cpu_b.get("cpu_sec")
            if gpu_sec is None and cpu_sec is None:
                continue
            entry = by_workload[wid]
            entry["workload_id"] = wid
            entry["label"] = row.get("label") or wid
            entry["workload_kind"] = row.get("workload_kind")
            entry["chips"][slug] = {
                "gpu_sec": gpu_sec,
                "cpu_sec": cpu_sec,
                "validity_gate_pass": b.get("validity_gate_pass") or cpu_b.get("validity_gate_pass"),
                "backend": backend,
                "status": b.get("status"),
            }

    multi = [v for v in by_workload.values() if len(v["chips"]) >= 2]
    multi.sort(key=lambda x: x["workload_id"])
    return multi


def discover_contributions() -> list[Path]:
    if not CONTRIB_ROOT.is_dir():
        return []
    return sorted(
        p for p in CONTRIB_ROOT.iterdir()
        if p.is_dir() and (p / "contribution.json").is_file() and not p.name.startswith("_")
    )


def legacy_single_contribution() -> tuple[Path, Path | None] | None:
    suite = ROOT / "data" / "latest" / "sources" / "lig-gpu-suite-latest.json"
    honest = ROOT / "data" / "latest" / "sources" / "lig-gpu-suite-honest.json"
    if suite.is_file():
        return suite, honest if honest.is_file() else None
    lic_root = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if lic_root:
        alt_suite = lic_root / "benchmarks" / "results" / "lig-gpu-suite-latest.json"
        alt_honest = lic_root / "benchmarks" / "results" / "lig-gpu-suite-honest.json"
        if alt_suite.is_file():
            return alt_suite, alt_honest if alt_honest.is_file() else None
    return None


def build_aggregate() -> dict[str, Any]:
    contributions = [build_contribution(d) for d in discover_contributions()]

    if not contributions:
        legacy = legacy_single_contribution()
        if legacy:
            suite_path, honest_path = legacy
            suite = load_json(suite_path)
            honest = load_json(honest_path) if honest_path else None
            rows = build_rows(suite, honest, "cuda")
            contributions.append(
                {
                    "chip_slug": "legacy-lab",
                    "label": str((suite.get("gpu") or {}).get("name") or "Lab GPU"),
                    "vendor": "nvidia",
                    "host_os": suite.get("host_os") or platform.system(),
                    "primary_backend": "cuda",
                    "contributor": {"org": "li-langverse", "role": "lab"},
                    "submitted_at": (suite.get("generated_at") or "")[:10],
                    "hardware": {"gpu_name": (suite.get("gpu") or {}).get("name")},
                    "sources": {
                        "lig_gpu_suite": rel_path(suite_path),
                        "lig_gpu_honest": rel_path(honest_path) if honest_path else "",
                    },
                    "gpu": suite.get("gpu"),
                    "backends": suite.get("backends"),
                    "summary": summary_for_rows(rows, suite.get("summary") or {}),
                    "possible_now": suite.get("possible_now"),
                    "funding_gaps": suite.get("funding_gaps"),
                    "honest_pilot": {
                        "status": honest.get("status") if honest else None,
                        "gpu_timing_ns": honest.get("gpu_timing_ns") if honest else None,
                        "note": honest.get("note") if honest else None,
                    },
                    "diagrams": build_diagrams(rows, "cuda"),
                    "rows": rows,
                }
            )

    contributed_slugs = {c["chip_slug"] for c in contributions}
    open_slots = [s for s in OPEN_SLOTS if s["chip_slug"] not in contributed_slugs]

    return {
        "schema": "benchmarks/lig-gpu-matrix/v2",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "contribution_policy_url": CONTRIBUTION_POLICY,
        "summary": {
            "contribution_count": len(contributions),
            "open_slot_count": len(open_slots),
            "total_timed_cuda_rows": sum(c["summary"].get("timed_cuda_rows", 0) for c in contributions),
            "total_timed_cpu_rows": sum(c["summary"].get("timed_cpu_rows", 0) for c in contributions),
        },
        "contributions": contributions,
        "open_slots": open_slots,
        "cross_chip": cross_chip_compare(contributions),
    }


def main() -> int:
    if not discover_contributions() and not legacy_single_contribution():
        print("No GPU contributions — skipping matrix build", file=sys.stderr)
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = build_aggregate()
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(payload['contributions'])} chips, {len(payload['open_slots'])} open slots)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
