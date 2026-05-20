#!/usr/bin/env python3
"""Patch only HTTP category in summary.json from lis tier-5 CSV (no lic CSV required).

Use when ingesting nginx oracle rows without re-running full build_summary.py
(which would clear physics/micro series if lic latest.csv is missing).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUMMARY = ROOT / "data/latest/summary.json"


def load_catalog_http_ids() -> dict[str, dict]:
    import tomllib

    raw = tomllib.loads((ROOT / "catalog.toml").read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for b in raw.get("benchmark", []):
        if b.get("category") == "http":
            out[b["id"]] = b
    return out


def parse_lis_csv(path: Path) -> dict[str, list[dict]]:
    by_bench: dict[str, list[dict]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            bid = row.get("benchmark") or ""
            if not bid:
                continue
            by_bench.setdefault(bid, []).append(row)
    return by_bench


HTTP_ORACLE_LANGS = ("li", "nginx", "apache", "lighttpd", "caddy", "node", "bun", "harness")


def series_from_rows(rows: list[dict], metric: str) -> list[dict]:
    series = []
    for lang in HTTP_ORACLE_LANGS:
        matches = [r for r in rows if r.get("lang") == lang and r.get("metric") == metric]
        if not matches:
            continue
        r = matches[0]
        try:
            val = float(r["value"])
        except (TypeError, ValueError):
            continue
        series.append(
            {
                "lang": lang,
                "value": val,
                "unit": r.get("unit") or "",
                "variant": r.get("variant") or "",
            }
        )
    if not series:
        for r in rows:
            if r.get("metric") == "verify_only" and r.get("lang") == "harness":
                series.append(
                    {
                        "lang": "harness",
                        "value": float(r.get("value") or 1),
                        "unit": "bool",
                        "variant": r.get("variant") or "ci",
                    }
                )
                break
    return series


def chart_for_bench(bid: str, cfg: dict, rows: list[dict]) -> dict:
    metric = cfg.get("metric", "rps")
    series = series_from_rows(rows, metric)
    if not series:
        for alt in ("rps", "verify_only"):
            series = series_from_rows(rows, alt)
            if series:
                metric = alt
                break

    oracle = cfg.get("compare_oracle", "nginx")
    li_val = next((s["value"] for s in series if s["lang"] == "li"), None)
    ref_val = next((s["value"] for s in series if s["lang"] == oracle), None)
    ratio = (li_val / ref_val) if li_val and ref_val and ref_val > 0 else None
    threshold = float(cfg.get("threshold_ratio_cpp", 1.0))
    if metric in ("rps", "throughput") and ratio is not None:
        ratio = 1.0 / ratio if ratio > 0 else None

    status = "unknown"
    if ratio is not None:
        if ratio <= threshold:
            status = "green"
        elif ratio <= threshold * 1.1:
            status = "yellow"
        else:
            status = "red"
    elif any(s["lang"] == oracle for s in series) and metric == "rps":
        status = "unknown"  # nginx baseline only — honest

    return {
        "id": bid,
        "title": bid.replace("_", " "),
        "metric": metric,
        "unit": series[0]["unit"] if series else "",
        "lower_is_better": metric in ("wall_time", "latency"),
        "reference_lang": oracle,
        "series": series,
        "grouped": False,
        "repo": cfg.get("repo", "lis"),
        "path": cfg.get("path", ""),
        "status": status,
        "ratio_vs_reference": round(ratio, 4) if ratio is not None else None,
    }


def row_for_chart(chart: dict, cfg: dict) -> dict:
    li_val = next((s["value"] for s in chart["series"] if s["lang"] == "li"), None)
    ref = chart["reference_lang"]
    ref_val = next((s["value"] for s in chart["series"] if s["lang"] == ref), None)
    return {
        "benchmark": chart["id"],
        "repo": cfg.get("repo", "lis"),
        "tier": cfg.get("tier", 5),
        "category": "http",
        "metric": chart["metric"],
        "li_value": li_val,
        "cpp_value": ref_val if ref == "cpp" else None,
        "ratio_vs_cpp": chart.get("ratio_vs_reference"),
        "unit": chart.get("unit"),
        "variant": cfg.get("variant"),
        "status": chart["status"],
        "ph_ids": cfg.get("ph_ids", []),
        "path": cfg.get("path", ""),
        "threshold_ratio_cpp": float(cfg.get("threshold_ratio_cpp", 1.0)),
        "ci_url": "",
        "langs": chart["series"],
    }


def main() -> int:
    lis_csv = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "lis/results/latest.csv"
    summary_path = Path(sys.argv[2]) if len(sys.argv) > 2 else SUMMARY

    if not lis_csv.is_file():
        print(f"merge_lis_http: missing {lis_csv}", file=sys.stderr)
        return 1
    if not summary_path.is_file():
        print(f"merge_lis_http: missing {summary_path}", file=sys.stderr)
        return 1

    catalog = load_catalog_http_ids()
    by_bench = parse_lis_csv(lis_csv)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    charts = []
    rows_out = []
    for bid, cfg in sorted(catalog.items()):
        bench_rows = by_bench.get(bid, [])
        chart = chart_for_bench(bid, cfg, bench_rows)
        charts.append(chart)
        rows_out.append(row_for_chart(chart, cfg))

    cats = summary.setdefault("categories", {})
    cats["http"] = {
        "label": "HTTP / webserver (li-httpd · lis)",
        "charts": sorted(charts, key=lambda c: c["id"]),
    }

    existing = {r["benchmark"]: i for i, r in enumerate(summary.get("rows") or [])}
    for row in rows_out:
        if row["benchmark"] in existing:
            summary["rows"][existing[row["benchmark"]]] = row
        else:
            summary.setdefault("rows", []).append(row)

    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"merge_lis_http: updated http ({len(charts)} charts) from {lis_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
