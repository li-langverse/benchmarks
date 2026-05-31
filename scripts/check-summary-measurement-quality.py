#!/usr/bin/env python3
"""CI gate: published ratios and sample-run counts must be fair and internally consistent."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/latest/summary.json"
COLORED = frozenset({"green", "yellow", "red"})
PERF_METRICS = frozenset(
    {
        "wall_time",
        "latency",
        "latency_p95",
        "rps",
        "throughput",
        "queries_per_sec",
    }
)
RATIO_EPS = 0.002
MAX_REPORT = 12


def is_perf_row(row: dict, chart: dict | None) -> bool:
    metric = (chart or {}).get("metric") or row.get("metric") or ""
    if metric in PERF_METRICS:
        return True
    category = row.get("category") or ""
    return category not in ("correctness", "security") and metric not in (
        "stability",
        "verify_pass",
        "pass_rate",
    )


def fail(msg: str) -> None:
    print(f"check-summary-measurement-quality: FAIL {msg}", file=sys.stderr)
    sys.exit(1)


def min_publish_runs() -> int:
    for key in ("MEASUREMENT_MIN_RUNS", "BENCH_MIN_RUNS"):
        raw = os.environ.get(key, "").strip()
        if raw:
            return max(1, int(raw))
    return 20


def strict_run_parity() -> bool:
    return os.environ.get("MEASUREMENT_STRICT_PARITY", "").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


def resolve_csv(summary: dict) -> Path | None:
    for env_key in ("BENCHMARKS_CSV",):
        raw = os.environ.get(env_key, "").strip()
        if raw:
            p = Path(raw)
            if p.is_file():
                return p
    lic_root = os.environ.get("LIC_ROOT", "").strip()
    if lic_root:
        p = Path(lic_root) / "benchmarks/results/latest.csv"
        if p.is_file():
            return p
    src = (summary.get("sources") or {}).get("lic_csv")
    if src:
        p = Path(src)
        if p.is_file():
            return p
        alt = ROOT / "results/latest.csv"
        if alt.is_file():
            return alt
    fallback = ROOT / "results/latest.csv"
    return fallback if fallback.is_file() else None


def chart_for_row(summary: dict, row: dict) -> dict | None:
    bench = row["benchmark"]
    os_tag = row.get("os") or "linux"
    for cat in summary.get("categories", {}).values():
        for ch in cat.get("charts", []):
            ch_id = str(ch.get("id", "")).split("@")[0]
            base = ch.get("base_id") or ch_id
            ch_os = ch.get("os") or "linux"
            if ch_os != os_tag or not ch.get("series"):
                continue
            if ch_id == bench or base == bench:
                return ch
    return None


def ratio_close(stored: float | None, expected: float | None) -> bool:
    if stored is None and expected is None:
        return True
    if stored is None or expected is None:
        return False
    return abs(stored - expected) <= RATIO_EPS


def main() -> int:
    if not SUMMARY.is_file():
        fail(f"missing {SUMMARY}")

    sys.path.insert(0, str(ROOT / "scripts/ingest"))
    from build_summary import (  # noqa: E402
        dedupe_csv_rows,
        merge_csv_rows,
        metric_lower_is_better,
        parse_csv,
        parse_sample_runs,
        ratio_li_vs_ref,
        relative_perf_vs_sota,
    )

    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    min_runs = min_publish_runs()
    ratio_errors: list[str] = []
    run_errors: list[str] = []
    csv_errors: list[str] = []

    for row in summary.get("rows") or []:
        if row.get("os") != "linux":
            continue
        if row.get("status") not in COLORED:
            continue
        if row.get("li_value") is None:
            continue

        chart = chart_for_row(summary, row)
        if not chart:
            if is_perf_row(row, None):
                ratio_errors.append(f"{row['benchmark']}: no chart series for ratio audit")
            continue

        series = chart.get("series") or []
        perf = is_perf_row(row, chart)
        if not perf:
            continue

        metric = chart.get("metric") or row.get("metric") or "wall_time"
        lower = bool(chart.get("lower_is_better", metric_lower_is_better(metric)))
        li_pt = next((s for s in series if s.get("lang") == "li"), None)
        if not li_pt:
            ratio_errors.append(f"{row['benchmark']}: missing li in chart series")
            continue

        sota_ref = row.get("sota_ref_lang") or chart.get("sota_ref_lang")
        sota_val = (
            next((s["value"] for s in series if s.get("lang") == sota_ref), None)
            if sota_ref
            else None
        )
        if perf:
            expected_sota = relative_perf_vs_sota(
                li_pt["value"], sota_val, lower_is_better=lower
            )
            stored_sota = row.get("ratio_vs_sota")
            if not ratio_close(stored_sota, expected_sota):
                ratio_errors.append(
                    f"{row['benchmark']}: ratio_vs_sota {stored_sota!r} != "
                    f"recomputed {expected_sota!r} (li={li_pt['value']}, sota={sota_val})"
                )

        if perf:
            ref = row.get("compare_oracle") or chart.get("reference_lang") or "cpp"
            ref_pt = next((s for s in series if s.get("lang") == ref), None)
            if ref_pt:
                expected_ref = ratio_li_vs_ref(
                    li_pt["value"],
                    ref_pt["value"],
                    metric=metric,
                    lower_is_better=lower,
                )
                stored_ref = row.get("ratio_vs_cpp")
                if ref == "cpp" and not ratio_close(stored_ref, expected_ref):
                    ratio_errors.append(
                        f"{row['benchmark']}: ratio_vs_cpp {stored_ref!r} != "
                        f"recomputed {expected_ref!r}"
                    )

        li_runs = li_pt.get("sample_runs") or row.get("li_sample_runs")
        if li_runs is None or int(li_runs) < 1:
            run_errors.append(f"{row['benchmark']}: li_sample_runs missing or zero")
            continue
        li_runs = int(li_runs)

        comp_runs = [
            int(s["sample_runs"])
            for s in series
            if s.get("lang") not in ("li", "harness")
            and s.get("sample_runs") is not None
            and int(s["sample_runs"]) >= 1
        ]
        if not comp_runs:
            continue
        max_comp = max(comp_runs)
        if max_comp >= min_runs and li_runs < min_runs:
            run_errors.append(
                f"{row['benchmark']}: li ran {li_runs}x but competitors up to "
                f"{max_comp}x (need >={min_runs})"
            )
        elif strict_run_parity() and li_runs < max_comp:
            run_errors.append(
                f"{row['benchmark']}: li ran {li_runs}x < max competitor {max_comp}x"
            )

    csv_path = resolve_csv(summary)
    if csv_path:
        raw = dedupe_csv_rows(merge_csv_rows([csv_path]))
        by_bench: dict[str, list[dict]] = {}
        for r in raw:
            if r.get("metric") != "wall_time":
                continue
            if r.get("lang") in ("", "harness"):
                continue
            os_tag = (r.get("os") or "linux").lower()
            if os_tag not in ("linux",):
                continue
            by_bench.setdefault(r["benchmark"], []).append(r)

        row_by_bench = {
            r["benchmark"]: r
            for r in summary.get("rows") or []
            if r.get("os") == "linux" and r.get("status") in COLORED
        }
        for bench, rows in by_bench.items():
            if bench not in row_by_bench:
                continue
            li_rows = [r for r in rows if r.get("lang") == "li"]
            if not li_rows:
                continue
            li_runs = max(parse_sample_runs(r) or 0 for r in li_rows)
            comp_runs = [
                parse_sample_runs(r) or 0
                for r in rows
                if r.get("lang") not in ("li", "harness")
            ]
            comp_runs = [n for n in comp_runs if n >= 1]
            if not comp_runs:
                continue
            max_comp = max(comp_runs)
            if max_comp >= min_runs and li_runs < min_runs:
                csv_errors.append(
                    f"{bench}: CSV li_runs={li_runs} while competitors up to {max_comp}"
                )
            elif strict_run_parity() and li_runs < max_comp:
                csv_errors.append(
                    f"{bench}: CSV li_runs={li_runs} < max competitor {max_comp}"
                )

    if ratio_errors:
        fail(
            f"{len(ratio_errors)} ratio mismatch(es): "
            + "; ".join(ratio_errors[:MAX_REPORT])
            + (" …" if len(ratio_errors) > MAX_REPORT else "")
        )
    if run_errors:
        fail(
            f"{len(run_errors)} sample-run imbalance(s) (min_runs={min_runs}): "
            + "; ".join(run_errors[:MAX_REPORT])
            + (" …" if len(run_errors) > MAX_REPORT else "")
        )
    if csv_errors:
        fail(
            f"{len(csv_errors)} CSV sample-run issue(s): "
            + "; ".join(csv_errors[:MAX_REPORT])
            + (" …" if len(csv_errors) > MAX_REPORT else "")
        )

    print(
        "PASS check-summary-measurement-quality "
        f"(min_runs={min_runs}, strict_parity={strict_run_parity()}, linux_colored_checked="
        f"{sum(1 for r in summary.get('rows', []) if r.get('os')=='linux' and r.get('status') in COLORED)}"
        + (f", csv={csv_path}" if csv_path else "")
        + ")"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
