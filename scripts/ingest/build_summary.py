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
    "numerics",
    "compiler",
    "server",
    "physics",
    "proofs",
    "security",
    "database",
    "graphics",
    "tooling",
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
    "proofs": "Proofs & correctness gates",
    "correctness": "Correctness & stability",
}


def benchmark_pillar(cfg: dict) -> str:
    pillar = str(cfg.get("pillar") or cfg.get("category", "micro"))
    if pillar == "correctness":
        return "proofs"
    return pillar


def benchmark_package(cfg: dict) -> str:
    if pkg := cfg.get("package"):
        return str(pkg)
    return str(cfg.get("repo", "lic"))


def build_pillars(charts_by_pillar: dict[str, list[dict]]) -> dict[str, dict]:
    pillars: dict[str, dict] = {}
    for pillar in PILLAR_ORDER:
        charts = charts_by_pillar.get(pillar, [])
        pillars[pillar] = {
            "label": PILLAR_LABELS.get(pillar, pillar),
            "charts": sorted(charts, key=lambda c: c["id"]),
        }
    return pillars


def row_meta(cfg: dict) -> dict[str, str]:
    return {"pillar": benchmark_pillar(cfg), "package": benchmark_package(cfg)}


def size_meta(cfg: dict) -> dict[str, str | None]:
    return {
        "problem_size": cfg.get("problem_size"),
        "size_label": cfg.get("size_label"),
        "base_id": cfg.get("base_id"),
    }


def chart_title(bench_id: str, cfg: dict) -> str:
    label = cfg.get("size_label") or cfg.get("problem_size")
    base = str(cfg.get("base_id") or bench_id).replace("_", " ")
    if label:
        return f"{base} ({label})"
    return bench_id.replace("_", " ")


def row_problem_size(row: dict) -> str:
    return str(row.get("problem_size") or "").strip()


def row_matches_catalog(row: dict, bench_id: str, cfg: dict) -> bool:
    """Match CSV rows to a catalog entry (benchmark id + optional problem_size)."""
    csv_bench = row.get("benchmark") or ""
    cat_ps = str(cfg.get("problem_size") or "").strip()
    base_id = str(cfg.get("base_id") or "").strip()
    csv_ps = row_problem_size(row)
    direct = csv_bench == bench_id
    via_base = bool(base_id and cat_ps and csv_bench == base_id)
    if not (direct or via_base):
        return False
    if cat_ps:
        if csv_ps:
            return csv_ps == cat_ps
        return direct and not (base_id and bench_id != base_id)
    if csv_ps:
        return False
    return True


def rows_for_bench(rows: list[dict], bench_id: str, cfg: dict) -> list[dict]:
    return [r for r in rows if row_matches_catalog(r, bench_id, cfg)]


def has_csv_rows(rows: list[dict], bench_id: str, cfg: dict) -> bool:
    return bool(rows_for_bench(rows, bench_id, cfg))


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


def is_sota_candidate(lang: str) -> bool:
    """Li is never SOTA; harness rows are infra, not competitive oracles."""
    return bool(lang) and lang not in ("li", "harness")


def normalize_os(raw: str | None) -> str:
    if not raw:
        return "unknown"
    os = raw.strip().lower()
    if os in ("linux", "darwin", "windows"):
        return os
    if os in ("macos", "osx"):
        return "darwin"
    return os or "unknown"


def csv_passed(row: dict) -> bool | None:
    raw = row.get("passed")
    if raw is None or raw == "":
        return None
    return str(raw).strip().lower() in ("true", "1", "yes", "pass")


def bench_os(
    rows: list[dict],
    bench_id: str,
    cfg: dict | None = None,
    *,
    variant: str | None = None,
) -> str:
    """Primary OS tag for a benchmark row (Li row preferred)."""
    bench_rows = (
        rows_for_bench(rows, bench_id, cfg)
        if cfg is not None
        else [r for r in rows if r.get("benchmark") == bench_id]
    )
    li_rows = li_rows_for_validity(bench_rows, variant)
    for r in li_rows + bench_rows:
        os = normalize_os(r.get("os") or r.get("OS"))
        if os != "unknown":
            return os
    return "unknown"


def metric_lower_is_better(metric: str) -> bool:
    return metric in ("wall_time", "latency", "latency_p95")


def compute_sota(
    series: list[dict], *, lower_is_better: bool
) -> tuple[str | None, float | None]:
    competitors = [s for s in series if is_sota_candidate(s.get("lang", ""))]
    if not competitors:
        return None, None
    pick = min if lower_is_better else max
    best = pick(competitors, key=lambda s: s["value"])
    return best["lang"], best["value"]


def ratio_li_vs_ref(
    li_val: float | None,
    ref_val: float | None,
    *,
    metric: str,
    lower_is_better: bool,
) -> float | None:
    if li_val is None or ref_val is None or ref_val <= 0:
        return None
    ratio = li_val / ref_val
    if not lower_is_better and ratio > 0:
        ratio = 1.0 / ratio
    if metric in ("rps", "throughput", "queries_per_sec") and ratio > 0:
        ratio = 1.0 / ratio
    return ratio


def load_stability_index(stability_path: Path) -> dict[str, dict[str, bool]]:
    index: dict[str, dict[str, bool]] = defaultdict(dict)
    for r in parse_csv(stability_path):
        test = r.get("test") or ""
        lang = r.get("lang") or ""
        if not test or not lang:
            continue
        index[test][lang] = csv_passed(r) is True
    return index


def validity_required_for(cfg: dict, catalog_defaults: dict) -> bool:
    if "validity_required" in cfg:
        return bool(cfg["validity_required"])
    return bool(catalog_defaults.get("validity_required", True))




def li_rows_for_validity(bench_rows: list[dict], variant: str | None) -> list[dict]:
    """Li CSV rows for validity — align variant fallback with lang_series."""
    li = [r for r in bench_rows if r.get("lang") == "li"]
    if not variant:
        return li
    preferred = [r for r in li if (r.get("variant") or "") == variant]
    return preferred if preferred else li


def validity_for_benchmark(
    bench_id: str,
    cfg: dict,
    raw_rows: list[dict],
    stability_index: dict[str, dict[str, bool]],
    *,
    required: bool,
) -> tuple[str, str]:
    """Return (validity_status, validity_source) — pass | fail | unknown."""
    if not required:
        return "pass", "validity_not_required"

    metric = cfg.get("metric", "wall_time")
    variant = cfg.get("variant")
    bench_rows = rows_for_bench(raw_rows, bench_id, cfg)
    li_rows = li_rows_for_validity(bench_rows, variant)

    passed_flags = [csv_passed(r) for r in li_rows if csv_passed(r) is not None]
    if passed_flags:
        if all(passed_flags):
            return "pass", "latest.csv:passed"
        return "fail", "latest.csv:passed"

    if metric in ("verify_pass", "pass_rate"):
        for r in li_rows:
            try:
                val = float(r["value"])
            except (TypeError, ValueError):
                continue
            if val >= 1.0:
                return "pass", f"metric:{metric}"
            return "fail", f"metric:{metric}"
        return "unknown", "none"

    if bench_id == "tier0_stability" or cfg.get("category") == "correctness":
        li_stab = stability_index.get(bench_id, {}).get("li")
        if li_stab is True:
            return "pass", "stability.csv"
        if li_stab is False:
            return "fail", "stability.csv"
        for test, langs in stability_index.items():
            if bench_id in test or test in bench_id:
                if langs.get("li") is True:
                    return "pass", "stability.csv"
                if langs.get("li") is False:
                    return "fail", "stability.csv"
        if stability_index:
            return "unknown", "stability.csv"
        return "unknown", "none"

    if stability_index.get(bench_id, {}).get("li") is True:
        return "pass", "stability.csv"
    if stability_index.get(bench_id, {}).get("li") is False:
        return "fail", "stability.csv"

    if not bench_rows:
        return "unknown", "none"

    for r in li_rows:
        try:
            float(r["value"])
        except (TypeError, ValueError):
            continue
        return "pass", "latest.csv:perf_present"

    return "unknown", "none"


def apply_validity_gate(perf_status: str, validity_status: str) -> str:
    if validity_status == "pass":
        return perf_status
    if validity_status == "fail":
        return "red"
    return "unknown"


def make_summary_row(
    *,
    bench_id: str,
    cfg: dict,
    chart: dict,
    validity_status: str,
    validity_source: str,
    os_name: str,
    category: str,
    metric: str,
    status: str,
) -> dict:
    meta = row_meta(cfg)
    series = chart.get("series", [])
    li_val = next((s["value"] for s in series if s["lang"] == "li"), None)
    ref = chart.get("reference_lang", "cpp")
    ref_val = next((s["value"] for s in series if s["lang"] == ref), None)
    sota_lang = chart.get("sota_lang")
    sota_val = next((s["value"] for s in series if s["lang"] == sota_lang), None) if sota_lang else None
    return {
        "benchmark": bench_id,
        "repo": cfg.get("repo", "lic"),
        "tier": cfg.get("tier", 0),
        "category": category,
        "metric": metric,
        "li_value": li_val,
        "cpp_value": ref_val if ref == "cpp" else None,
        "ratio_vs_cpp": chart.get("ratio_vs_reference"),
        "sota_lang": sota_lang,
        "sota_value": sota_val,
        "ratio_vs_sota": chart.get("ratio_vs_sota"),
        "unit": chart.get("unit"),
        "variant": cfg.get("variant"),
        "status": status,
        "validity_status": validity_status,
        "validity_source": validity_source,
        "os": os_name,
        "ph_ids": cfg.get("ph_ids", []),
        "path": cfg.get("path", ""),
        "threshold_ratio_cpp": float(cfg.get("threshold_ratio_cpp", 1.2)),
        "compare_oracle": ref,
        "ci_url": "",
        "langs": series,
        **meta,
        **size_meta(cfg),
    }


def lang_series(
    rows: list[dict],
    bench_id: str,
    metric: str,
    cfg: dict | None = None,
    *,
    variant: str | None = None,
) -> list[dict]:
    scoped = rows_for_bench(rows, bench_id, cfg) if cfg else rows
    out = []
    for lang in LANG_ORDER:
        matches = [
            r
            for r in scoped
            if r.get("lang") == lang and r.get("metric") == metric
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
                "os": normalize_os(r.get("os") or r.get("OS")),
            }
        )
    return out


def http_lang_series(
    rows: list[dict],
    bench_id: str,
    metric: str,
    cfg: dict | None = None,
    *,
    variant: str | None = None,
) -> list[dict]:
    """All webserver oracles for tier-5 charts (multiple li variants when present)."""
    scoped = rows_for_bench(rows, bench_id, cfg) if cfg else rows
    bench_rows = [r for r in scoped if r.get("metric") == metric]
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
                "os": normalize_os(r.get("os") or r.get("OS")),
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
        "pillar": "proofs",
        "package": "lic",
        "validity_status": "unknown",
        "validity_source": "stability.csv",
    }


def build_perf_chart(
    bench_id: str,
    cfg: dict,
    rows: list[dict],
    *,
    validity_status: str,
    validity_source: str,
) -> dict:
    metric = cfg.get("metric", "wall_time")
    variant = cfg.get("variant")
    is_http = cfg.get("category") == "http"
    series_fn = http_lang_series if is_http else lang_series
    series = series_fn(rows, bench_id, metric, cfg, variant=variant)
    if not series:
        bench_rows = rows_for_bench(rows, bench_id, cfg)
        metrics = {r.get("metric") for r in bench_rows if r.get("metric")}
        for alt in sorted(metrics):
            series = series_fn(rows, bench_id, alt, cfg, variant=variant)
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
    lower = metric_lower_is_better(metric)
    ratio = ratio_li_vs_ref(li_val, ref_val, metric=metric, lower_is_better=lower)
    sota_lang, sota_val = compute_sota(series, lower_is_better=lower)
    ratio_sota = ratio_li_vs_ref(li_val, sota_val, metric=metric, lower_is_better=lower)
    threshold = float(cfg.get("threshold_ratio_cpp", 1.2))
    perf_st = status_for_ratio(ratio, threshold)
    st = apply_validity_gate(perf_st, validity_status)
    meta = row_meta(cfg)
    sizes = size_meta(cfg)
    return {
        "id": bench_id,
        "title": chart_title(bench_id, cfg),
        "metric": metric,
        "unit": series[0]["unit"] if series else "",
        "lower_is_better": lower,
        "reference_lang": oracle,
        "sota_lang": sota_lang,
        "series": series,
        "grouped": False,
        "repo": cfg.get("repo", "lic"),
        "path": cfg.get("path", ""),
        "status": st,
        "perf_status": perf_st,
        "ratio_vs_reference": round(ratio, 4) if ratio is not None else None,
        "ratio_vs_sota": round(ratio_sota, 4) if ratio_sota is not None else None,
        "validity_status": validity_status,
        "validity_source": validity_source,
        "os": bench_os(rows, bench_id, cfg, variant=variant),
        "pillar": meta["pillar"],
        "package": meta["package"],
        **sizes,
    }


def is_pending_catalog_row(
    bench_id: str, cfg: dict, by_bench: dict[str, list], all_rows: list[dict]
) -> bool:
    if has_csv_rows(all_rows, bench_id, cfg):
        return False
    if cfg.get("base_id"):
        return True
    if cfg.get("path") == "unknown" or bench_id.endswith("_stub"):
        return True
    category = cfg.get("category", "micro")
    if category == "database" and bench_id not in by_bench:
        return True
    return category in ("tooling",) and bench_id not in by_bench


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
    sizes = size_meta(cfg)
    ref = cfg.get("compare_oracle") or ("postgres" if category == "database" else "cpp")
    chart = {
        "id": bench_id,
        "title": chart_title(bench_id, cfg),
        "metric": metric,
        "unit": "ms" if category == "database" else "",
        "lower_is_better": metric in ("wall_time", "latency", "latency_p95"),
        "reference_lang": ref,
        "series": [],
        "grouped": False,
        "repo": cfg.get("repo", "lic"),
        "path": cfg.get("path", ""),
        "status": "unknown",
        "pending": True,
        "pillar": meta["pillar"],
        "package": meta["package"],
        **sizes,
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
            "sota_lang": None,
            "sota_value": None,
            "ratio_vs_sota": None,
            "unit": "ms" if category == "database" else None,
            "variant": cfg.get("variant"),
            "status": "unknown",
            "validity_status": "unknown",
            "validity_source": "none",
            "os": "unknown",
            "ph_ids": cfg.get("ph_ids", []),
            "path": cfg.get("path", ""),
            "threshold_ratio_cpp": float(cfg.get("threshold_ratio_cpp", 1.2)),
            "compare_oracle": ref,
            "ci_url": "",
            **meta,
            **sizes,
        }
    )


def load_catalog_defaults() -> dict:
    import tomllib

    raw = tomllib.loads((ROOT / "catalog.toml").read_text())
    return {k: v for k, v in raw.items() if k != "benchmark"}


def main() -> int:
    lic_root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "lic"
    lis_root = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT.parent / "lis"

    lic_csv = lic_root / "benchmarks/results/latest.csv"
    lis_csv = lis_root / "results/latest.csv"
    stability_csv = lic_root / "benchmarks/results/stability.csv"
    security_csv = lic_root / "benchmarks/results/security.csv"

    catalog_defaults = load_catalog_defaults()
    catalog = load_catalog()
    raw = merge_csv_rows([lic_csv, lis_csv])
    stability_index = load_stability_index(stability_csv)

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
            required = validity_required_for(cfg, catalog_defaults)
            validity_status, validity_source = validity_for_benchmark(
                bench_id, cfg, raw, stability_index, required=required
            )
            st = "green" if validity_status == "pass" else (
                "red" if validity_status == "fail" else "unknown"
            )
            tier_counts[str(cfg.get("tier", 0))][st] += 1
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
                    "sota_lang": None,
                    "sota_value": None,
                    "ratio_vs_sota": None,
                    "unit": None,
                    "variant": None,
                    "status": st,
                    "validity_status": validity_status,
                    "validity_source": validity_source,
                    "os": bench_os(raw, bench_id, cfg),
                    "ph_ids": cfg.get("ph_ids", []),
                    "path": cfg.get("path", ""),
                    "threshold_ratio_cpp": float(cfg.get("threshold_ratio_cpp", 1.2)),
                    "compare_oracle": cfg.get("compare_oracle", "cpp"),
                    "ci_url": "",
                    **meta,
                }
            )
            continue

        if is_pending_catalog_row(bench_id, cfg, by_bench, raw):
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

        required = validity_required_for(cfg, catalog_defaults)
        validity_status, validity_source = validity_for_benchmark(
            bench_id, cfg, raw, stability_index, required=required
        )
        chart = build_perf_chart(
            bench_id,
            cfg,
            raw,
            validity_status=validity_status,
            validity_source=validity_source,
        )
        charts_by_cat[category].append(chart)
        charts_by_pillar[meta["pillar"]].append(chart)

        st = chart["status"]
        tier = str(cfg.get("tier", 0))
        tier_counts[tier][st] += 1

        results.append(
            make_summary_row(
                bench_id=bench_id,
                cfg=cfg,
                chart=chart,
                validity_status=validity_status,
                validity_source=validity_source,
                os_name=chart.get("os", "unknown"),
                category=category,
                metric=chart.get("metric", metric),
                status=st,
            )
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

    os_values = sorted({r.get("os", "unknown") for r in results if r.get("os")})
    size_labels = sorted(
        {
            str(r["size_label"])
            for r in results
            if r.get("size_label")
        }
    )

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "lic_csv": str(lic_csv),
            "lis_csv": str(lis_csv),
            "stability_csv": str(stability_csv),
            "security_csv": str(security_csv),
        },
        "reporting": {
            "sota_policy": "best_competitor_lang_excludes_li",
            "validity_required_default": bool(
                catalog_defaults.get("validity_required", True)
            ),
            "os_values": os_values,
            "size_labels": size_labels,
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
