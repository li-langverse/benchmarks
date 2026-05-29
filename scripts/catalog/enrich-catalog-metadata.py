#!/usr/bin/env python3
"""Enrich catalog.toml: problem_size from harness params, package paths, remove package stubs.

  LIC_ROOT=../lic python3 scripts/catalog/enrich-catalog-metadata.py --write
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"
DEFAULT_LIC = ROOT.parent / "lic"
STUB_IDS = frozenset({"lig_viewport_stub", "li_math_gemm_stub"})
PACKAGE_PREFIX: list[tuple[str, str, str, str]] = [
    ("viz_", "lig", "lig", "benchmarks/viewport/{id}"),
    ("ml_", "li-math", "li-math", "benchmarks/ml/{id}"),
]
HTTP_SIZE_LABELS: dict[str, tuple[str, str]] = {
    "static_small": ("payload_1k", "1 KiB static /"),
    "static_large": ("payload_1mib", "1 MiB file.bin"),
    "keepalive_pipelining": ("pipeline_16", "16-pipeline keepalive"),
    "proxy_loopback": ("loopback_wrk", "loopback wrk"),
    "https_static": ("tls_static", "TLS static M15"),
}
SIZE_VARIANTS: dict[str, list[tuple[str, str, str]]] = {
    "matmul_naive": [("1024", "N=1024", "1024")],
    "matmul_blocked": [("1024", "N=1024 block=64", "1024")],
}


def load_header(text: str) -> str:
    idx = text.find("[[benchmark]]")
    return text[:idx].rstrip() + "\n\n" if idx != -1 else ""


def parse_params(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    out: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        out[key.strip().lower()] = val.strip()
    return out


def size_from_params(params: dict[str, str]) -> tuple[str | None, str | None]:
    if "n" in params:
        n = params["n"]
        block = params.get("block")
        return n, f"N={n}" + (f" block={block}" if block else "")
    return None, None


def format_benchmark(b: dict) -> str:
    lines = ["[[benchmark]]", f'id = "{b["id"]}"']
    for key in (
        "base_id", "category", "pillar", "package", "tier", "repo", "path", "metric",
        "threshold_ratio_cpp", "compare_oracle", "variant", "problem_size", "size_label",
        "validity_required", "catalog_lifecycle",
    ):
        if key not in b or b[key] is None:
            continue
        val = b[key]
        if isinstance(val, bool):
            lines.append(f"{key} = {'true' if val else 'false'}")
        elif isinstance(val, (int, float)):
            lines.append(f"{key} = {val}")
        else:
            lines.append(f'{key} = "{val}"')
    ph = b.get("ph_ids") or []
    if ph:
        lines.append("ph_ids = [" + ", ".join(f'"{p}"' for p in ph) + "]")
    plats = b.get("platforms")
    if plats:
        lines.append(
            "platforms = [" + ", ".join(f'"{p}"' for p in plats) + "]"
        )
    return "\n".join(lines)


def apply_package_rules(b: dict) -> None:
    bid = b["id"]
    for prefix, pkg, repo, path_tmpl in PACKAGE_PREFIX:
        if bid.startswith(prefix):
            b["package"] = pkg
            b["repo"] = repo
            if b.get("path") in (None, "", "unknown"):
                b["path"] = path_tmpl.format(id=bid)
            return


def enrich_benchmark(b: dict, lic_root: Path) -> dict:
    if not b.get("package"):
        b["package"] = str(b.get("repo") or "lic")
    apply_package_rules(b)
    if b["id"] in HTTP_SIZE_LABELS and not b.get("problem_size"):
        ps, sl = HTTP_SIZE_LABELS[b["id"]]
        b["problem_size"], b["size_label"] = ps, sl
    path = str(b.get("path") or "")
    if path.startswith("benchmarks/tier1_micro/") and not b.get("problem_size"):
        ps, sl = size_from_params(parse_params(lic_root / path / "params.toml"))
        if ps:
            b["problem_size"], b["size_label"] = ps, sl
    if b.get("path") == "unknown":
        b.setdefault("size_label", "workload TBD")
    if b.get("size_label") == "harness pending":
        if b.get("variant") == "algo_registry":
            b["size_label"] = "registry catalog entry"
            b.setdefault("problem_size", "catalog")
        elif b.get("problem_size"):
            ps = str(b["problem_size"])
            b["size_label"] = f"N={ps}" if ps.isdigit() else ps
        else:
            b["size_label"] = "workload TBD"
    b.setdefault("platforms", ["linux", "macos", "windows"])
    return b


def extra_size_rows(benchmarks: list[dict]) -> list[dict]:
    by_id = {b["id"]: b for b in benchmarks}
    extra: list[dict] = []
    for base_id, variants in SIZE_VARIANTS.items():
        base = by_id.get(base_id)
        if not base:
            continue
        for suffix, label, ps in variants:
            vid = f"{base_id}_N{suffix}"
            if vid in by_id:
                continue
            row = dict(base)
            row.update(id=vid, base_id=base_id, problem_size=ps, size_label=label)
            extra.append(row)
    return extra


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lic-root", type=Path, default=Path(__import__("os").environ.get("LIC_ROOT", str(DEFAULT_LIC))))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    lic_root = args.lic_root.resolve()
    import tomllib

    text = CATALOG.read_text()
    header = load_header(text)
    benchmarks = [enrich_benchmark(dict(b), lic_root) for b in tomllib.loads(text).get("benchmark", []) if b["id"] not in STUB_IDS]
    benchmarks.extend(extra_size_rows(benchmarks))
    benchmarks.sort(key=lambda b: (b.get("tier", 99), b["id"]))
    print(f"rows {len(benchmarks)}")
    if not args.write:
        return 1
    CATALOG.write_text(header + "\n\n".join(format_benchmark(b) for b in benchmarks) + "\n")
    print(f"wrote {CATALOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
