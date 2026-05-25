#!/usr/bin/env python3
"""Build data/latest/summary.json from lic/lis CSV exports and catalog.toml."""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

LANG_ORDER = ["li", "cpp", "rust", "julia", "nginx", "harness", "go", "python"]
HTTP_LANG_ORDER = [
    "li",
    "nginx",
    "apache",
    "lighttpd",
    "caddy",
    "node",
    "bun",
    "harness",
]
CATEGORY_ORDER = [
    "micro",
    "physics",
    "http",
    "database",
    "tooling",
    "security",
    "correctness",
]
CATEGORY_LABELS = {
    "micro": "Micro / SIMD & linear algebra",
    "physics": "Physics & simulations",
    "http": "HTTP / webserver (li-httpd · lis)",
    "database": "Registry OLTP (lidb vs Postgres · tier_db_registry)",
    "tooling": "Ecosystem tooling (lip · lit · lic compile)",
    "security": "Security gates (CVE · webserver registry)",
    "correctness": "Correctness & stability",
}
PILLAR_ORDER = [
    "compiler",
    "numerics",
    "physics",
    "server",
    "database",
    "tooling",
    "security",
    "graphics",
    "correctness",
]
PILLAR_LABELS = {
    "compiler": "Compiler & codegen",
    "numerics": "Numerics & SIMD / linear algebra",
    "physics": "Physics & simulations",
    "server": "HTTP / webserver",
    "database": "Database & registry OLTP",
    "tooling": "Ecosystem tooling",
    "security": "Security gates",
    "graphics": "Graphics & viewport",
    "correctness": "Correctness & stability",
}


def benchmark_pillar(cfg: dict) -> str:
    return str(cfg.get("pillar") or cfg.get("category", "micro"))


def benchmark_package(cfg: dict) -> str:
    if pkg := cfg.get("package"):
        return str(pkg)
    return str(cfg.get("repo", "lic"))


def build_pillars(charts_by_pillar: dict[str, list[dict]]) -> dict[str, dict]:
    pillars: dict[str, dict] = {}
    for pillar in PILLAR_ORDER:
        if pillar not in charts_by_pillar:
            continue
        pillars[pillar] = {
            "label": PILLAR_LABELS.get(pillar, pillar),
            "charts": sorted(charts_by_pillar[pillar], key=lambda c: c["id"]),
        }
    return pillars


def row_meta(cfg: dict) -> dict[str, str]:
    return {"pillar": benchmark_pillar(cfg), "package": benchmark_package(cfg)}


def load_catalog() -> dict[str, dict]:
    import tomllib

    catalog: dict[str, dict] = {}
    raw = tomllib.loads((ROOT / "catalog.toml").read_text())
    for b in raw.get("benchmark", []):
        catalog[b["id"]] = b
    return catalog


def parse_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def merge_csv_rows(paths: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for p in paths:
        rows.extend(parse_csv(p))
    return rows


def status_for_ratio(ratio: float | None, threshold: float) -> str:
    if ratio is None:
        return "unknown"
    if ratio <= threshold:
        return "green"
    if ratio <= threshold * 1.1:
        return "yellow"
    return "red"


def lang_series(
    rows: list[dict], bench_id: str, metric: str, *, variant: str | None = None
) -> list[dict]:
    out = []
    for lang in LANG_ORDER:
        matches = [
            r
            for r in rows
            if r.get("benchmark") == bench_id
            and r.get("lang") == lang
            and r.get("metric") == metric
        ]
        if variant and lang == "li":
            preferred = [r for r in matches if (r.get("variant") or "") == variant]
            if preferred:
                matches = preferred
        if not matches:
            continue
        r = matches[0]
        try:
            val = float(r["value"])
        except (TypeError, ValueError):
            continue
        out.append(
            {
                "lang": lang,
                "value": val,
                "unit": r.get("unit") or "",
                "variant": r.get("variant") or "",
            }
        )
    return out


def http_lang_series(
    rows: list[dict], bench_id: str, metric: str, *, variant: str | None = None
) -> list[dict]:
    """All webserver oracles for tier-5 charts (multiple li variants when present)."""
    bench_rows = [
        r
        for r in rows
        if r.get("benchmark") == bench_id and r.get("metric") == metric
    ]
    out: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def append_row(r: dict) -> None:
        lang = r.get("lang") or ""
        var = r.get("variant") or ""
        key = (lang, var)
        if key in seen:
            return
        try:
            val = float(r["value"])
        except (TypeError, ValueError):
            return
        seen.add(key)
        out.append(
            {
                "lang": lang,
                "value": val,
                "unit": r.get("unit") or "",
                "variant": var,
            }
        )

    for lang in HTTP_LANG_ORDER:
        matches = [r for r in bench_rows if r.get("lang") == lang]
        if not matches:
            continue
        if lang == "li":
            for r in matches:
                append_row(r)
        else:
            append_row(matches[0])
    return out


def build_security_chart(security_path: Path) -> dict | None:
    rows = parse_csv(security_path)
    if not rows:
        return None
    series = []
    for r in rows:
        try:
            val = float(r["value"])
        except (TypeError, ValueError):
            continue
        series.append(
            {
                "lang": r.get("lang") or "harness",
                "value": val,
                "unit": r.get("metric") or "s",
                "label": r.get("test") or "",
            }
        )
    if not series:
        return None
    return {
        "id": "security_gates",
        "title": "Security gate wall time",
        "metric": "wall_time",
        "unit": "s",
        "lower_is_better": True,
        "reference_lang": "harness",
        "series": series,
        "grouped": True,
        "repo": "lic",
        "path": "scripts/ci-security.sh",
        "status": "unknown",
        "pillar": "security",
        "package": "lic",
    }


def build_stability_chart(stability_path: Path) -> dict | None:
    rows = parse_csv(stability_path)
    if not rows:
        return None
    tests: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        tests[r["test"]].append(
            {
                "lang": r["lang"],
                "value": 1.0 if r.get("passed", "").lower() == "true" else 0.0,
                "unit": "pass",
                "passed": r.get("passed", "").lower() == "true",
            }
        )
    series_flat = []
    for test_name, langs in sorted(tests.items()):
        for entry in langs:
            series_flat.append(
                {
                    "lang": entry["lang"],
                    "value": entry["value"],
                    "unit": "pass",
                    "label": test_name,
                }
            )
    return {
        "id": "tier0_stability",
        "title": "Tier 0 stability (pass=1)",
        "metric": "stability",
        "unit": "pass",
        "lower_is_better": False,
        "reference_lang": "cpp",
        "series": series_flat,
        "grouped": True,
        "repo": "lic",
        "path": "benchmarks/tier0_correctness",
        "status": "unknown",
        "pillar": "correctness",
        "package": "lic",
    }


def build_perf_chart(
    bench_id: str, cfg: dict, rows: list[dict]
) -> dict:
    metric = cfg.get("metric", "wall_time")
    variant = cfg.get("variant")
    is_http = cfg.get("category") == "http"
    series_fn = http_lang_series if is_http else lang_series
    series = series_fn(rows, bench_id, metric, variant=variant)
    if not series:
        bench_rows = [r for r in rows if r.get("benchmark") == bench_id]
        metrics = {r.get("metric") for r in bench_rows if r.get("metric")}
        for alt in sorted(metrics):
            series = series_fn(rows, bench_id, alt, variant=variant)
            if series:
                metric = alt
                break
    if variant:
        li_val = next(
            (s["value"] for s in series if s["lang"] == "li" and s.get("variant") == variant),
            next((s["value"] for s in series if s["lang"] == "li"), None),
        )
    else:
        li_val = next((s["value"] for s in series if s["lang"] == "li"), None)
    cpp_val = next((s["value"] for s in series if s["lang"] == "cpp"), None)
    oracle = cfg.get("compare_oracle", "cpp")
    ref_val = next((s["value"] for s in series if s["lang"] == oracle), cpp_val)
    ratio = (li_val / ref_val) if li_val and ref_val and ref_val > 0 else None
    threshold = float(cfg.get("threshold_ratio_cpp", 1.2))
    if metric in ("rps", "throughput") and ratio is not None:
        ratio = 1.0 / ratio if ratio > 0 else None
    st = status_for_ratio(ratio, threshold)
    meta = row_meta(cfg)
    return {
        "id": bench_id,
        "title": bench_id.replace("_", " "),
        "metric": metric,
        "unit": series[0]["unit"] if series else "",
        "lower_is_better": metric in ("wall_time", "latency"),
        "reference_lang": oracle,
        "series": series,
        "grouped": False,
        "repo": cfg.get("repo", "lic"),
        "path": cfg.get("path", ""),
        "status": st,
        "ratio_vs_reference": round(ratio, 4) if ratio is not None else None,
        "pillar": meta["pillar"],
        "package": meta["package"],
    }


def is_pending_catalog_row(bench_id: str, cfg: dict, by_bench: dict[str, list]) -> bool:
    if cfg.get("path") == "unknown" or bench_id.endswith("_stub"):
        return True
    category = cfg.get("category", "micro")
    return category in ("tooling", "database") and bench_id not in by_bench


def append_pending_row(
    *,
    bench_id: str,
    cfg: dict,
    category: str,
    metric: str,
    charts_by_cat: dict[str, list[dict]],
    charts_by_pillar: dict[str, list[dict]],
    tier_counts: dict[str, dict[str, int]],
    results: list[dict],
) -> None:
    meta = row_meta(cfg)
    chart = {
        "id": bench_id,
        "title": bench_id,
        "metric": metric,
        "unit": "",
        "lower_is_better": True,
        "reference_lang": "cpp",
        "series": [],
        "grouped": False,
        "repo": cfg.get("repo", "lic"),
        "path": cfg.get("path", ""),
        "status": "unknown",
        "pending": True,
        "pillar": meta["pillar"],
        "package": meta["package"],
    }
    charts_by_cat[category].append(chart)
    charts_by_pillar[meta["pillar"]].append(chart)
    tier_counts[str(cfg.get("tier", 3))]["unknown"] += 1
    results.append(
        {
            "benchmark": bench_id,
            "repo": cfg.get("repo", "lic"),
            "tier": cfg.get("tier", 0),
            "category": category,
            "metric": metric,
            "li_value": None,
            "cpp_value": None,
            "ratio_vs_cpp": None,
            "unit": None,
            "variant": cfg.get("variant"),
            "status": "unknown",
            "ph_ids": cfg.get("ph_ids", []),
            "path": cfg.get("path", ""),
            "threshold_ratio_cpp": float(cfg.get("threshold_ratio_cpp", 1.2)),
            "ci_url": "",
            **meta,
        }
    )


def main() -> int:
    lic_root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "li"
    lis_root = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT.parent / "lis"

    lic_csv = lic_root / "benchmarks/results/latest.csv"
    lis_csv = lis_root / "results/latest.csv"
    stability_csv = lic_root / "benchmarks/results/stability.csv"
    security_csv = lic_root / "benchmarks/results/security.csv"

    catalog = load_catalog()
    raw = merge_csv_rows([lic_csv, lis_csv])

    by_bench: dict[str, list[dict]] = defaultdict(list)
    for row in raw:
        by_bench[row["benchmark"]].append(row)

    results = []
    tier_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"green": 0, "yellow": 0, "red": 0, "unknown": 0}
    )
    charts_by_cat: dict[str, list[dict]] = defaultdict(list)
    charts_by_pillar: dict[str, list[dict]] = defaultdict(list)

    sec_chart = build_security_chart(security_csv)
    if sec_chart:
        charts_by_cat["security"].append(sec_chart)
        charts_by_pillar[sec_chart["pillar"]].append(sec_chart)

    for bench_id, cfg in catalog.items():
        category = cfg.get("category", "micro")
        metric = cfg.get("metric", "wall_time")
        meta = row_meta(cfg)

        if category == "correctness" and bench_id == "tier0_stability":
            chart = build_stability_chart(stability_csv)
            if chart:
                charts_by_cat["correctness"].append(chart)
                charts_by_pillar[chart["pillar"]].append(chart)
            tier_counts[str(cfg.get("tier", 0))]["unknown"] += 1
            results.append(
                {
                    "benchmark": bench_id,
                    "repo": cfg.get("repo", "lic"),
                    "tier": cfg.get("tier", 0),
                    "category": category,
                    "metric": metric,
                    "li_value": None,
                    "cpp_value": None,
                    "ratio_vs_cpp": None,
                    "unit": None,
                    "variant": None,
                    "status": "unknown",
                    "ph_ids": cfg.get("ph_ids", []),
                    "path": cfg.get("path", ""),
                    "threshold_ratio_cpp": float(cfg.get("threshold_ratio_cpp", 1.2)),
                    "ci_url": "",
                    **meta,
                }
            )
            continue

        if is_pending_catalog_row(bench_id, cfg, by_bench):
            append_pending_row(
                bench_id=bench_id,
                cfg=cfg,
                category=category,
                metric=metric,
                charts_by_cat=charts_by_cat,
                charts_by_pillar=charts_by_pillar,
                tier_counts=tier_counts,
                results=results,
            )
            continue

        chart = build_perf_chart(bench_id, cfg, raw)
        charts_by_cat[category].append(chart)
        charts_by_pillar[meta["pillar"]].append(chart)

        li_val = next((s["value"] for s in chart["series"] if s["lang"] == "li"), None)
        ref = chart["reference_lang"]
        ref_val = next((s["value"] for s in chart["series"] if s["lang"] == ref), None)
        ratio = chart.get("ratio_vs_reference")
        st = chart["status"]
        tier = str(cfg.get("tier", 0))
        tier_counts[tier][st] += 1

        results.append(
            {
                "benchmark": bench_id,
                "repo": cfg.get("repo", "lic"),
                "tier": cfg.get("tier", 0),
                "category": category,
                "metric": metric,
                "li_value": li_val,
                "cpp_value": ref_val if ref == "cpp" else None,
                "ratio_vs_cpp": ratio,
                "unit": chart.get("unit"),
                "variant": cfg.get("variant"),
                "status": st,
                "ph_ids": cfg.get("ph_ids", []),
                "path": cfg.get("path", ""),
                "threshold_ratio_cpp": float(cfg.get("threshold_ratio_cpp", 1.2)),
                "ci_url": "",
                "langs": chart["series"],
                **meta,
            }
        )

    categories = {}
    for cat in CATEGORY_ORDER:
        if cat not in charts_by_cat:
            continue
        categories[cat] = {
            "label": CATEGORY_LABELS.get(cat, cat),
            "charts": sorted(charts_by_cat[cat], key=lambda c: c["id"]),
        }

    pillars = build_pillars(charts_by_pillar)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "lic_csv": str(lic_csv),
            "lis_csv": str(lis_csv),
            "stability_csv": str(stability_csv),
            "security_csv": str(security_csv),
        },
        "tier_counts": dict(tier_counts),
        "categories": categories,
        "pillars": pillars,
        "rows": sorted(results, key=lambda r: (r["tier"], r["benchmark"])),
    }

    out_dir = ROOT / "data/latest"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(
        f"wrote {out_dir / 'summary.json'} "
        f"({len(results)} rows, {sum(len(c['charts']) for c in categories.values())} charts, "
        f"{len(pillars)} pillars)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
