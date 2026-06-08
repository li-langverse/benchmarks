#!/usr/bin/env python3
"""CI gate: linux wall_time rows must have equal sample_runs when BENCH_EQUALIZE_RUNS=1."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "ingest"))
from build_summary import dedupe_csv_rows, merge_csv_rows, parse_sample_runs  # noqa: E402


def equalize_enabled() -> bool:
    return os.environ.get("BENCH_EQUALIZE_RUNS", "1").strip().lower() not in (
        "0",
        "false",
        "no",
        "off",
    )


def strict_parity() -> bool:
    return os.environ.get("MEASUREMENT_STRICT_PARITY", "1").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


def min_runs() -> int:
    for key in ("MEASUREMENT_MIN_RUNS", "BENCH_MIN_RUNS"):
        raw = os.environ.get(key, "").strip()
        if raw:
            return max(1, int(raw))
    return 6


def fail(msg: str) -> None:
    print(f"check-csv-sample-run-parity: FAIL {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    if not equalize_enabled():
        print("check-csv-sample-run-parity: skip (BENCH_EQUALIZE_RUNS=0)")
        return 0

    path = Path(sys.argv[1] if len(sys.argv) > 1 else "results/latest.csv")
    if not path.is_file():
        fail(f"missing {path}")

    rows = dedupe_csv_rows(merge_csv_rows([path]))
    errors: list[str] = []
    floor = min_runs()
    strict = strict_parity()

    by_bench: dict[str, list[dict]] = {}
    for row in rows:
        if row.get("metric") != "wall_time":
            continue
        if (row.get("os") or "linux").lower() not in ("linux", ""):
            continue
        lang = row.get("lang") or ""
        if lang in ("", "harness"):
            continue
        by_bench.setdefault(row["benchmark"], []).append(row)

    for bench, bench_rows in sorted(by_bench.items()):
        li_runs = max(
            (parse_sample_runs(r) or 0 for r in bench_rows if r.get("lang") == "li"),
            default=0,
        )
        comp_runs = [
            parse_sample_runs(r) or 0
            for r in bench_rows
            if r.get("lang") not in ("li", "harness")
        ]
        comp_runs = [n for n in comp_runs if n >= 1]
        if not comp_runs or li_runs < 1:
            continue
        max_comp = max(comp_runs)
        if max_comp >= floor and li_runs < floor:
            errors.append(f"{bench}: li_runs={li_runs} < min_runs={floor} (competitors up to {max_comp})")
        elif strict and li_runs < max_comp:
            errors.append(f"{bench}: li_runs={li_runs} < max competitor {max_comp}")

    if errors:
        fail(
            f"{len(errors)} imbalance(s): " + "; ".join(errors[:12])
            + (" …" if len(errors) > 12 else "")
        )

    print(f"PASS check-csv-sample-run-parity ({path}, benches={len(by_bench)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
