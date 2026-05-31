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
    "stdlib",
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
    "stdlib": "Stdlib collections & algorithms",
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
        if via_base:
            return True
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


PLATFORM_ORDER = ("linux", "macos", "windows")


def normalize_os(raw: str | None) -> str:
    if not raw:
        return "unknown"
    os = raw.strip().lower()
    if os in ("linux", "windows"):
        return os
    if os in ("darwin", "macos", "osx"):
        return "macos"
    return os or "unknown"


def catalog_platforms(cfg: dict, catalog_defaults: dict) -> list[str]:
    raw = cfg.get("platforms") or catalog_defaults.get("platforms") or list(PLATFORM_ORDER)
    ordered = [p for p in PLATFORM_ORDER if p in raw]
    for p in raw:
        if p not in ordered:
            ordered.append(p)
    return ordered or list(PLATFORM_ORDER)


def chart_base_id(bench_id: str, cfg: dict) -> str:
    return str(cfg.get("base_id") or bench_id)


def effective_size_meta(cfg: dict, *, has_csv: bool) -> dict[str, str | None]:
    sizes = size_meta(cfg)
    sizes.pop("base_id", None)
    sl = sizes.get("size_label")
    if sl in (None, "", "harness pending", "pending"):
        if cfg.get("problem_size"):
            sizes["size_label"] = f"N={cfg['problem_size']}"
        elif cfg.get("variant") == "algo_registry":
            sizes["size_label"] = "algo registry stub"
        elif has_csv and int(cfg.get("tier", 0)) >= 2:
            sizes["size_label"] = "tier2 default grid"
        elif has_csv:
            sizes["size_label"] = "harness wired"
        elif sl == "harness pending":
            sizes["size_label"] = "harness pending"
    return sizes


def csv_passed(row: dict) -> bool | None:
    raw = row.get("passed")
    if raw is None or raw == "":
        return None
    return str(raw).strip().lower() in ("true", "1", "yes", "pass")


def metric_value(li_rows: list[dict], metric: str) -> float | None:
    for r in li_rows:
        if r.get("metric") == metric:
            try:
                return float(r["value"])
            except (TypeError, ValueError):
                return None
    return None


def oracle_kind_from_rows(rows: list[dict]) -> str:
    for r in rows:
        kind = (r.get("oracle_kind") or "").strip()
        if kind:
            return kind
    return "unknown"


def extract_numeric_validity(bench_rows: list[dict], variant: str | None) -> dict | None:
    """Analytical-oracle deviation exported by lic harness verify (Li rows)."""
    li_rows = li_rows_for_validity(bench_rows, variant)
    ulps = metric_value(li_rows, "verify_ulps")
    if ulps is None:
        return None
    within = metric_value(li_rows, "verify_within_1ulp")
    return {
        "oracle": oracle_kind_from_rows(li_rows),
        "analytical_value": metric_value(li_rows, "verify_analytical"),
        "checksum_value": metric_value(li_rows, "verify_checksum"),
        "abs_error": metric_value(li_rows, "verify_abs_err"),
        "rel_error": metric_value(li_rows, "verify_rel_err"),
        "ulps": ulps,
        "within_1ulp": bool(within is not None and within >= 1.0),
    }


def bench_os(
    rows: list[dict],
    bench_id: str,
    cfg: dict | None = None,
    *,
    variant: str | None = None,
) -> str:
    """Primary OS tag for a benchmark row (Li row preferred)."""
    tags = os_tags_for_bench(rows, bench_id, cfg, variant=variant)
    if tags == ["unknown"]:
        return "unknown"
    for preferred in PLATFORM_ORDER:
        if preferred in tags:
            return preferred
    return tags[0]


def os_tags_for_bench(
    rows: list[dict],
    bench_id: str,
    cfg: dict,
    *,
    variant: str | None = None,
) -> list[str]:
    """Distinct normalized OS tags present in CSV for this catalog benchmark."""
    bench_rows = rows_for_bench(rows, bench_id, cfg)
    tags: set[str] = set()
    for r in bench_rows:
        tags.add(normalize_os(r.get("os") or r.get("OS")))
    if variant:
        li_rows = [r for r in bench_rows if r.get("lang") == "li"]
        li_tags = {normalize_os(r.get("os") or r.get("OS")) for r in li_rows}
        if li_tags:
            tags &= li_tags or tags
    ordered = [t for t in PLATFORM_ORDER if t in tags]
    rest = sorted(t for t in tags if t not in ordered and t != "unknown")
    if ordered or rest:
        return ordered + rest
    return ["unknown"]


def rows_for_bench_os(
    rows: list[dict], bench_id: str, cfg: dict, os_tag: str
) -> list[dict]:
    bench_rows = rows_for_bench(rows, bench_id, cfg)
    if os_tag == "unknown":
        return [r for r in bench_rows if normalize_os(r.get("os") or r.get("OS")) == "unknown"]
    return [
        r
        for r in bench_rows
        if normalize_os(r.get("os") or r.get("OS")) == os_tag
    ]


def chart_id_for_os(bench_id: str, os_tag: str, *, multi: bool) -> str:
    if not multi or os_tag == "unknown":
        return bench_id
    return f"{bench_id}@{os_tag}"


def metric_lower_is_better(metric: str) -> bool:
    return metric in ("wall_time", "latency", "latency_p95")


def timing_fields_from_row(r: dict) -> dict:
    """Optional mean/stddev/sample_runs from harness CSV (value column = mean)."""
    out: dict = {}
    std = r.get("stddev", "")
    if std not in ("", None):
        try:
            out["stddev"] = float(std)
        except (TypeError, ValueError):
            pass
    runs = r.get("sample_runs", "")
    if runs not in ("", None):
        try:
            out["sample_runs"] = int(float(runs))
        except (TypeError, ValueError):
            pass
    return out


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


def relative_perf_vs_sota(
    value: float | None,
    sota_val: float | None,
    *,
    lower_is_better: bool,
) -> float | None:
    """Relative speed vs best competitor — SOTA = 1.0, higher is better."""
    if value is None or sota_val is None or value <= 0 or sota_val <= 0:
        return None
    if lower_is_better:
        return sota_val / value
    return value / sota_val


def enrich_series_relative_perf(
    series: list[dict],
    sota_lang: str | None,
    sota_val: float | None,
    *,
    lower_is_better: bool,
) -> None:
    """Attach relative_perf to each series point (SOTA lang pinned at 1.0)."""
    for s in series:
        rel = relative_perf_vs_sota(
            s.get("value"),
            sota_val,
            lower_is_better=lower_is_better,
        )
        if rel is not None:
            s["relative_perf"] = round(rel, 4)
        if sota_lang and s.get("lang") == sota_lang:
            s["relative_perf"] = 1.0


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

    within_1ulp = metric_value(li_rows, "verify_within_1ulp")
    verify_ulps = metric_value(li_rows, "verify_ulps")
    if within_1ulp is not None:
        if within_1ulp >= 1.0:
            return "pass", "latest.csv:verify_within_1ulp"
        return "fail", "latest.csv:verify_within_1ulp"
    if verify_ulps is not None:
        if verify_ulps <= 1.0:
            return "pass", "latest.csv:verify_ulps"
        return "fail", "latest.csv:verify_ulps"

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
    raw_rows: list[dict],
) -> dict:
    meta = row_meta(cfg)
    series = chart.get("series", [])
    li_pt = next((s for s in series if s["lang"] == "li"), None)
    li_val = li_pt["value"] if li_pt else None
    ref = chart.get("reference_lang", "cpp")
    ref_pt = next((s for s in series if s["lang"] == ref), None)
    ref_val = ref_pt["value"] if ref_pt else None
    sota_lang = chart.get("sota_lang")
    sota_val = next((s["value"] for s in series if s["lang"] == sota_lang), None) if sota_lang else None
    bench_rows = rows_for_bench(raw_rows, bench_id, cfg)
    numeric_validity = extract_numeric_validity(bench_rows, cfg.get("variant"))
    row = {
        "benchmark": bench_id,
        "repo": cfg.get("repo", "lic"),
        "tier": cfg.get("tier", 0),
        "category": category,
        "metric": metric,
        "li_value": li_val,
        "li_stddev": li_pt.get("stddev") if li_pt else None,
        "li_sample_runs": li_pt.get("sample_runs") if li_pt else None,
        "cpp_value": ref_val if ref == "cpp" else None,
        "cpp_stddev": ref_pt.get("stddev") if ref_pt and ref == "cpp" else None,
        "cpp_sample_runs": ref_pt.get("sample_runs") if ref_pt and ref == "cpp" else None,
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
        "problem_size": chart.get("problem_size", cfg.get("problem_size")),
        "size_label": chart.get("size_label", cfg.get("size_label")),
        "base_id": chart.get("base_id", chart_base_id(bench_id, cfg)),
    }
    if numeric_validity is not None:
        row["numeric_validity"] = numeric_validity
    return row


def lang_series(
    rows: list[dict],
    bench_id: str,
    metric: str,
    cfg: dict | None = None,
    *,
    variant: str | None = None,
    os_tag: str | None = None,
) -> list[dict]:
    if cfg and os_tag:
        scoped = rows_for_bench_os(rows, bench_id, cfg, os_tag)
    else:
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
                **timing_fields_from_row(r),
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
    os_tag: str | None = None,
) -> list[dict]:
    """All webserver oracles for tier-5 charts (multiple li variants when present)."""
    if cfg and os_tag:
        scoped = rows_for_bench_os(rows, bench_id, cfg, os_tag)
    else:
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
                **timing_fields_from_row(r),
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


def build_platform_skip_chart(
    bench_id: str,
    cfg: dict,
    os_tag: str,
    *,
    chart_id: str | None = None,
    multi: bool = False,
    validity_source: str = "platform_not_measured",
) -> dict:
    """Placeholder chart when catalog expects an OS but CSV has no measurements."""
    category = cfg.get("category", "micro")
    metric = cfg.get("metric", "wall_time")
    meta = row_meta(cfg)
    sizes = effective_size_meta(cfg, has_csv=False)
    ref = cfg.get("compare_oracle") or ("postgres" if category == "database" else "cpp")
    cid = chart_id or chart_id_for_os(bench_id, os_tag, multi=multi)
    title = chart_title(bench_id, {**cfg, **sizes})
    if multi and os_tag != "unknown":
        title = f"{title} ({os_tag})"
    return {
        "id": cid,
        "base_id": chart_base_id(bench_id, cfg),
        "title": title,
        "metric": metric,
        "unit": "ms" if category == "database" else "",
        "lower_is_better": metric in ("wall_time", "latency", "latency_p95"),
        "reference_lang": ref,
        "series": [],
        "grouped": False,
        "repo": cfg.get("repo", "lic"),
        "path": cfg.get("path", ""),
        "status": "skip",
        "perf_status": "unknown",
        "pending": True,
        "pillar": meta["pillar"],
        "package": meta["package"],
        "validity_status": "skip",
        "validity_source": validity_source,
        "os": os_tag,
        "sota_lang": None,
        "sota_value": None,
        "ratio_vs_reference": None,
        "ratio_vs_sota": None,
        **sizes,
    }


def build_perf_chart(
    bench_id: str,
    cfg: dict,
    rows: list[dict],
    *,
    validity_status: str,
    validity_source: str,
    os_tag: str | None = None,
    chart_id: str | None = None,
    has_csv: bool = True,
) -> dict:
    metric = cfg.get("metric", "wall_time")
    variant = cfg.get("variant")
    is_http = cfg.get("category") == "http"
    series_fn = http_lang_series if is_http else lang_series
    series = series_fn(rows, bench_id, metric, cfg, variant=variant, os_tag=os_tag)
    if not series:
        bench_rows = (
            rows_for_bench_os(rows, bench_id, cfg, os_tag)
            if os_tag
            else rows_for_bench(rows, bench_id, cfg)
        )
        metrics = {r.get("metric") for r in bench_rows if r.get("metric")}
        for alt in sorted(metrics):
            series = series_fn(rows, bench_id, alt, cfg, variant=variant, os_tag=os_tag)
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
    enrich_series_relative_perf(
        series, sota_lang, sota_val, lower_is_better=lower
    )
    ratio_sota = relative_perf_vs_sota(
        li_val, sota_val, lower_is_better=lower
    )
    threshold = float(cfg.get("threshold_ratio_cpp", 1.2))
    perf_st = status_for_ratio(ratio, threshold)
    st = apply_validity_gate(perf_st, validity_status)
    meta = row_meta(cfg)
    sizes = effective_size_meta(cfg, has_csv=has_csv)
    os_name = os_tag or bench_os(rows, bench_id, cfg, variant=variant)
    cid = chart_id or bench_id
    title = chart_title(bench_id, {**cfg, **sizes})
    if os_tag and os_tag != "unknown":
        title = f"{title} ({os_tag})"
    return {
        "id": cid,
        "base_id": chart_base_id(bench_id, cfg),
        "title": title,
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
        "os": os_name,
        "pillar": meta["pillar"],
        "package": meta["package"],
        **sizes,
    }


def is_pending_catalog_row(
    bench_id: str, cfg: dict, by_bench: dict[str, list], all_rows: list[dict]
) -> bool:
    """Catalog rows without harness CSV measurements become pending placeholders."""
    return not has_csv_rows(all_rows, bench_id, cfg)


def tier_le_1(cfg: dict) -> bool:
    tier = cfg.get("tier", 99)
    return tier in (0, 1, "0", "1")


def append_benchmark_summary_rows(
    results: list[dict],
    *,
    bench_id: str,
    cfg: dict,
    bench_charts: list[dict],
    category: str,
    metric: str,
    raw: list[dict],
    validity_status: str,
    validity_source: str,
    primary_status: str | None = None,
) -> None:
    """Emit one summary row per platform chart for tier 0/1; else primary only."""
    if tier_le_1(cfg):
        for chart in bench_charts:
            os_name = chart.get("os", "linux")
            scoped = rows_for_bench_os(raw, bench_id, cfg, os_name)
            st = chart.get("status", primary_status or "unknown")
            results.append(
                make_summary_row(
                    bench_id=bench_id,
                    cfg=cfg,
                    chart=chart,
                    validity_status=chart.get("validity_status", validity_status),
                    validity_source=chart.get("validity_source", validity_source),
                    os_name=os_name,
                    category=category,
                    metric=chart.get("metric", metric),
                    status=st,
                    raw_rows=scoped or raw,
                )
            )
        return

    primary = next(
        (c for c in bench_charts if c.get("os") == "linux" and c.get("series")),
        next((c for c in bench_charts if c.get("series")), bench_charts[0]),
    )
    os_name = primary.get("os", "linux")
    scoped = rows_for_bench_os(raw, bench_id, cfg, os_name)
    st = primary_status or primary.get("status", "unknown")
    results.append(
        make_summary_row(
            bench_id=bench_id,
            cfg=cfg,
            chart=primary,
            validity_status=primary.get("validity_status", validity_status),
            validity_source=primary.get("validity_source", validity_source),
            os_name=os_name,
            category=category,
            metric=primary.get("metric", metric),
            status=st,
            raw_rows=scoped or raw,
        )
    )


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
    catalog_defaults: dict,
) -> None:
    meta = row_meta(cfg)
    sizes = effective_size_meta(cfg, has_csv=False)
    ref = cfg.get("compare_oracle") or ("postgres" if category == "database" else "cpp")
    platforms = catalog_platforms(cfg, catalog_defaults)
    multi = len(platforms) > 1
    validity_source = (
        "harness_not_wired"
        if cfg.get("variant") == "algo_registry"
        else "harness_pending"
    )
    charts: list[dict] = []
    for os_tag in platforms:
        chart = build_platform_skip_chart(
            bench_id,
            cfg,
            os_tag,
            chart_id=chart_id_for_os(bench_id, os_tag, multi=multi),
            multi=multi,
            validity_source=validity_source,
        )
        charts.append(chart)
        charts_by_cat[category].append(chart)
        charts_by_pillar[meta["pillar"]].append(chart)
    tier_counts[str(cfg.get("tier", 3))]["unknown"] += 1
    if tier_le_1(cfg):
        for chart in charts:
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
                    "status": "skip",
                    "validity_status": "skip",
                    "validity_source": chart.get("validity_source", validity_source),
                    "os": chart.get("os", "linux"),
                    "ph_ids": cfg.get("ph_ids", []),
                    "path": cfg.get("path", ""),
                    "threshold_ratio_cpp": float(cfg.get("threshold_ratio_cpp", 1.2)),
                    "compare_oracle": ref,
                    "ci_url": "",
                    **meta,
                    **sizes,
                }
            )
        return

    primary = charts[0]
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
            "status": "skip",
            "validity_status": "skip",
            "validity_source": validity_source,
            "os": primary.get("os", "linux"),
            "ph_ids": cfg.get("ph_ids", []),
            "path": cfg.get("path", ""),
            "threshold_ratio_cpp": float(cfg.get("threshold_ratio_cpp", 1.2)),
            "compare_oracle": ref,
            "ci_url": "",
            **meta,
            **sizes,
        }
    )


def source_ref(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)



def git_sha(root: Path) -> str:
    import subprocess
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return ""


def collect_provenance(lic_root: Path, lic_csv: Path) -> dict:
    import os
    import platform
    import subprocess
    llvm = ""
    try:
        llvm = subprocess.check_output(
            ["clang", "--version"], stderr=subprocess.DEVNULL
        ).decode().splitlines()[0]
    except Exception:
        pass
    lis_root = Path(os.environ.get("LIS_ROOT", ROOT.parent / "lis"))
    return {
        "lic_sha": git_sha(lic_root),
        "lic_ref": os.environ.get("LIC_REF", "main"),
        "benchmarks_sha": git_sha(ROOT),
        "lis_sha": git_sha(lis_root),
        "llvm_version": llvm,
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID", ""),
        "runner_os": platform.system().lower(),
        "bench_csv": str(lic_csv),
    }


def load_catalog_defaults() -> dict:
    import tomllib

    raw = tomllib.loads((ROOT / "catalog.toml").read_text())
    merged: dict = {}
    for key in ("defaults", "reporting"):
        section = raw.get(key)
        if isinstance(section, dict):
            merged.update(section)
    return merged


def main() -> int:
    lic_root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "lic"
    lis_root = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT.parent / "lis"

    import os

    bench_csv = Path(os.environ.get("BENCHMARKS_CSV", ROOT / "results/latest.csv"))
    lic_legacy = lic_root / "benchmarks/results/latest.csv"
    lic_csv = bench_csv if bench_csv.is_file() else lic_legacy
    if not lic_csv.is_file() and lic_legacy.is_file():
        lic_csv = lic_legacy
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
        if cfg.get("catalog_lifecycle") == "planned":
            continue
        category = cfg.get("category", "micro")
        metric = cfg.get("metric", "wall_time")
        meta = row_meta(cfg)

        if category == "correctness" and bench_id == "tier0_stability":
            chart = build_stability_chart(stability_csv)
            required = validity_required_for(cfg, catalog_defaults)
            validity_status, validity_source = validity_for_benchmark(
                bench_id, cfg, raw, stability_index, required=required
            )
            st = "green" if validity_status == "pass" else (
                "red" if validity_status == "fail" else "unknown"
            )
            platforms = catalog_platforms(cfg, catalog_defaults)
            multi = len(platforms) > 1
            tier0_charts: list[dict] = []
            for os_tag in platforms:
                if os_tag == "linux" and chart:
                    tier0_charts.append(
                        {
                            **chart,
                            "base_id": chart_base_id(bench_id, cfg),
                            "os": "linux",
                            "id": chart_id_for_os(bench_id, "linux", multi=multi),
                            "status": st,
                            "validity_status": validity_status,
                            "validity_source": validity_source,
                            "size_label": chart.get("size_label")
                            or cfg.get("size_label")
                            or "stability suite",
                        }
                    )
                else:
                    tier0_charts.append(
                        build_platform_skip_chart(
                            bench_id,
                            cfg,
                            os_tag,
                            chart_id=chart_id_for_os(bench_id, os_tag, multi=multi),
                            multi=multi,
                            validity_source="platform_not_measured",
                        )
                    )
            for ch in tier0_charts:
                charts_by_cat["correctness"].append(ch)
                charts_by_pillar[ch["pillar"]].append(ch)
            bucket = st if st in ("green", "yellow", "red") else "unknown"
            tier_counts[str(cfg.get("tier", 0))][bucket] += 1
            append_benchmark_summary_rows(
                results,
                bench_id=bench_id,
                cfg=cfg,
                bench_charts=tier0_charts,
                category=category,
                metric=metric,
                raw=raw,
                validity_status=validity_status,
                validity_source=validity_source,
                primary_status=st,
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
                catalog_defaults=catalog_defaults,
            )
            continue

        required = validity_required_for(cfg, catalog_defaults)
        validity_status, validity_source = validity_for_benchmark(
            bench_id, cfg, raw, stability_index, required=required
        )
        platforms = catalog_platforms(cfg, catalog_defaults)
        os_tags_from_csv = os_tags_for_bench(raw, bench_id, cfg, variant=cfg.get("variant"))
        multi_os = len(platforms) > 1
        bench_charts: list[dict] = []
        for os_tag in platforms:
            has_data = os_tag in os_tags_from_csv and bool(
                rows_for_bench_os(raw, bench_id, cfg, os_tag)
            )
            cid = chart_id_for_os(bench_id, os_tag, multi=multi_os)
            if has_data:
                chart = build_perf_chart(
                    bench_id,
                    cfg,
                    raw,
                    validity_status=validity_status,
                    validity_source=validity_source,
                    os_tag=os_tag,
                    chart_id=cid,
                    has_csv=True,
                )
            else:
                chart = build_platform_skip_chart(
                    bench_id,
                    cfg,
                    os_tag,
                    chart_id=cid,
                    multi=multi_os,
                )
            if not chart.get("series") and chart.get("status") != "skip":
                continue
            bench_charts.append(chart)

        if not bench_charts:
            continue

        primary = next(
            (c for c in bench_charts if c.get("os") == "linux" and c.get("series")),
            next((c for c in bench_charts if c.get("series")), bench_charts[0]),
        )
        for chart in bench_charts:
            charts_by_cat[category].append(chart)
            charts_by_pillar[meta["pillar"]].append(chart)

        st = primary["status"]
        tier = str(cfg.get("tier", 0))
        bucket = st if st in ("green", "yellow", "red") else "unknown"
        tier_counts[tier][bucket] += 1

        append_benchmark_summary_rows(
            results,
            bench_id=bench_id,
            cfg=cfg,
            bench_charts=bench_charts,
            category=category,
            metric=metric,
            raw=raw,
            validity_status=validity_status,
            validity_source=validity_source,
            primary_status=st,
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

    provenance = collect_provenance(lic_root, lic_csv)
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provenance": provenance,
        "sources": {
            "lic_root": str(lic_root.resolve()),
            "lis_root": str(lis_root.resolve()),
            "bench_csv": source_ref(lic_csv, ROOT if str(lic_csv).startswith(str(ROOT)) else lic_root),
            "lic_csv": source_ref(lic_csv, lic_root),
            "lis_csv": source_ref(lis_csv, lis_root),
            "stability_csv": source_ref(stability_csv, lic_root),
            "security_csv": source_ref(security_csv, lic_root),
        },
        "reporting": {
            "value_stat": "mean",
            "sota_policy": "best_competitor_lang_excludes_li",
            "relative_perf_higher_is_better": True,
            "validity_required_default": bool(
                catalog_defaults.get("validity_required", True)
            ),
            "os_values": os_values,
            "size_labels": size_labels,
        },
        "tier_counts": dict(tier_counts),
        "categories": categories,
        "pillars": pillars,
        "rows": sorted(results, key=lambda r: (r["tier"], r["benchmark"], r.get("os", ""))),
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
