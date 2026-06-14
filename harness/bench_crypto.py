#!/usr/bin/env python3
"""tier_crypto harness — cross-impl validity + Li/OpenSSL throughput."""

from __future__ import annotations

import argparse
import csv
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_HARNESS = Path(__file__).resolve().parent
if str(_HARNESS) not in sys.path:
    sys.path.insert(0, str(_HARNESS))

from paths import lic_root, lic_compiler_bin
from timing_stats import TimingStats, default_bench_runs, stats_from_samples

TIER_CRYPTO = _HARNESS.parent / "benchmarks" / "workloads" / "tier_crypto"
RESULTS = TIER_CRYPTO / "results"
BASELINE = TIER_CRYPTO / "baseline.csv"
BASELINE_RATIO = TIER_CRYPTO / "baseline-ratio.csv"

CSV_HEADER = [
    "benchmark",
    "lang",
    "variant",
    "threads",
    "metric",
    "value",
    "stddev",
    "sample_runs",
    "unit",
    "git_sha",
    "cpu_model",
    "flags",
]


@dataclass(frozen=True)
class LiBench:
    name: str
    rel_src: str
    ops_per_run: float


LI_BENCHES: tuple[LiBench, ...] = (
    LiBench("sha256", "packages/li-crypto/li-tests/bench/sha256_bench.li", 5000.0 * 2.0),
    LiBench("chacha20_poly1305", "packages/li-crypto/li-tests/bench/chacha_bench.li", 5000.0),
    LiBench("x25519", "packages/li-crypto/li-tests/bench/x25519_bench.li", 5000.0),
    LiBench("ml_dsa65_kat", "packages/li-pqc/li-tests/bench/kat_bench.li", 2000.0),
)

OPENSSL_SPEED: dict[str, str] = {
    "sha256": "sha256",
    "chacha20_poly1305": "chacha20-poly1305",
    "x25519": "x25519",
}


def git_sha(root: Path) -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def cpu_model() -> str:
    try:
        with open("/proc/cpuinfo", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform_node_fallback()


def platform_node_fallback() -> str:
    import platform

    return platform.processor() or "unknown"


def ensure_lic(root: Path) -> Path:
    lic = lic_compiler_bin(root)
    if lic.is_file():
        return lic
    build = root / "scripts" / "build.sh"
    if build.is_file():
        subprocess.run([str(build)], cwd=root, check=True)
    lic = lic_compiler_bin(root)
    if not lic.is_file():
        raise RuntimeError(f"lic compiler missing at {lic}")
    return lic


def build_li_bench(root: Path, lic: Path, spec: LiBench, out: Path) -> None:
    src = root / spec.rel_src
    if not src.is_file():
        raise FileNotFoundError(src)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            str(lic),
            "build",
            "--allow-open-vc",
            "--no-lean-verify",
            str(src),
            "-o",
            str(out),
        ],
        cwd=root,
        check=True,
    )


def time_binary_wall(path: Path, runs: int) -> TimingStats:
    import time

    samples: list[float] = []
    for _ in range(max(runs, 1)):
        t0 = time.perf_counter()
        subprocess.run([str(path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        samples.append(max(time.perf_counter() - t0, 1e-9))
    return stats_from_samples(samples)


def openssl_speed_ops(name: str, seconds: float) -> float | None:
    algo = OPENSSL_SPEED.get(name)
    if not algo:
        return None
    if not shutil_which("openssl"):
        return None
    try:
        p = subprocess.run(
            ["openssl", "speed", "-seconds", str(seconds), algo],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    text = p.stdout + p.stderr
    best = 0.0
    for line in text.splitlines():
        if algo.replace("-", "") not in line.replace("-", "").lower() and algo.split("-")[0] not in line.lower():
            continue
        for m in re.finditer(r"([\d.]+)\s*k", line):
            val = float(m.group(1)) * 1000.0
            best = max(best, val)
    return best if best > 0 else None


def shutil_which(cmd: str) -> str | None:
    import shutil

    return shutil.which(cmd)


def run_validity(root: Path, profile: str) -> None:
    script = root / "scripts" / "bench_crypto_validity.py"
    if not script.is_file():
        raise FileNotFoundError(script)
    subprocess.run(
        [sys.executable, str(script), "--profile", profile],
        cwd=root,
        check=True,
    )


def load_ratio_ceilings() -> dict[str, float]:
    ceilings: dict[str, float] = {}
    if not BASELINE_RATIO.is_file():
        return ceilings
    with BASELINE_RATIO.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("lang") != "li":
                continue
            ceilings[row["primitive"]] = float(row["max_openssl_ratio"])
    return ceilings


def check_ratios(rows: list[dict[str, str]], ceilings: dict[str, float]) -> list[str]:
    errs: list[str] = []
    li_ops: dict[str, float] = {}
    ossl_ops: dict[str, float] = {}
    for row in rows:
        if row.get("metric") != "ops_per_sec":
            continue
        if row["lang"] == "li":
            li_ops[row["benchmark"]] = float(row["value"])
        elif row["lang"] == "openssl":
            ossl_ops[row["benchmark"]] = float(row["value"])
    for prim, max_ratio in ceilings.items():
        li = li_ops.get(prim)
        ossl = ossl_ops.get(prim)
        if li is None or ossl is None or ossl <= 0:
            continue
        ratio = ossl / li if li > 0 else float("inf")
        if ratio > max_ratio:
            errs.append(
                f"tier_crypto: {prim} openssl/li ratio {ratio:.1f} > max {max_ratio}"
            )
    return errs


def load_baseline() -> dict[tuple[str, str], float]:
    floors: dict[tuple[str, str], float] = {}
    if not BASELINE.is_file():
        return floors
    with BASELINE.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["primitive"], row["lang"])
            floors[key] = float(row["min_ops_per_sec"])
    return floors


def check_floors(rows: list[dict[str, str]], floors: dict[tuple[str, str], float], slack: float) -> list[str]:
    errs: list[str] = []
    by_key: dict[tuple[str, str], float] = {}
    for row in rows:
        if row.get("metric") != "ops_per_sec":
            continue
        by_key[(row["benchmark"], row["lang"])] = float(row["value"])
    for (prim, lang), floor in floors.items():
        got = by_key.get((prim, lang))
        if got is None:
            if lang == "openssl":
                continue
            errs.append(f"tier_crypto: missing result for {prim}/{lang}")
            continue
        if got < floor * slack:
            errs.append(f"tier_crypto: {prim}/{lang} ops/s {got:.0f} < floor {floor * slack:.0f}")
    return errs


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def row_for(
    name: str,
    lang: str,
    ops: float,
    stddev: float,
    runs: int,
    root: Path,
) -> dict[str, str]:
    return {
        "benchmark": name,
        "lang": lang,
        "variant": "default",
        "threads": "1",
        "metric": "ops_per_sec",
        "value": f"{ops:.2f}",
        "stddev": f"{stddev:.4f}",
        "sample_runs": str(runs),
        "unit": "ops/s",
        "git_sha": git_sha(root),
        "cpu_model": cpu_model(),
        "flags": "",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="ci", choices=("ci", "baseline"))
    ap.add_argument("--skip-validity", action="store_true")
    ap.add_argument("--skip-openssl", action="store_true")
    ap.add_argument("--out", type=Path, default=RESULTS / "tier_crypto.csv")
    ap.add_argument("--runs", type=int, default=0)
    args = ap.parse_args()

    root = lic_root()
    runs = args.runs or (3 if args.profile == "ci" else default_bench_runs())
    speed_sec = 1.0 if args.profile == "ci" else 3.0
    slack = 0.25 if args.profile == "ci" else 0.5

    if not args.skip_validity:
        print("== tier_crypto: cross-impl validity ==")
        run_validity(root, args.profile)

    lic = ensure_lic(root)
    build_dir = root / "build" / "tier-crypto"
    rows: list[dict[str, str]] = []

    print("== tier_crypto: Li microbenches ==")
    for spec in LI_BENCHES:
        out = build_dir / f"{spec.name}-li"
        build_li_bench(root, lic, spec, out)
        stats = time_binary_wall(out, runs)
        ops = spec.ops_per_run / stats.mean if stats.mean > 0 else 0.0
        rows.append(row_for(spec.name, "li", ops, stats.stddev, stats.sample_runs, root))
        print(f"tier_crypto: {spec.name} li {ops:.0f} ops/s ({stats.sample_runs} runs)")

    if not args.skip_openssl:
        print("== tier_crypto: OpenSSL speed reference ==")
        for name in OPENSSL_SPEED:
            ops = openssl_speed_ops(name, speed_sec)
            if ops is None:
                print(f"tier_crypto: openssl {name} skipped (no openssl speed)", file=sys.stderr)
                continue
            rows.append(row_for(name, "openssl", ops, 0.0, 1, root))
            print(f"tier_crypto: {name} openssl {ops:.0f} ops/s")

    write_csv(args.out, rows)
    print(f"tier_crypto: wrote {len(rows)} rows -> {args.out}")

    floors = load_baseline()
    if floors:
        errs = check_floors(rows, floors, slack)
        for e in errs:
            print(e, file=sys.stderr)
        if errs:
            return 1

    if args.profile == "baseline":
        ceilings = load_ratio_ceilings()
        if ceilings:
            ratio_errs = check_ratios(rows, ceilings)
            for e in ratio_errs:
                print(e, file=sys.stderr)
            if ratio_errs:
                return 1

    # Li must stay within 100x of OpenSSL on sha256 (sanity, not perf target)
    li_sha = next((float(r["value"]) for r in rows if r["benchmark"] == "sha256" and r["lang"] == "li"), None)
    ossl_sha = next((float(r["value"]) for r in rows if r["benchmark"] == "sha256" and r["lang"] == "openssl"), None)
    if li_sha and ossl_sha and li_sha > ossl_sha * 100:
        print("tier_crypto: li sha256 suspiciously faster than openssl", file=sys.stderr)
        return 1

    print("tier_crypto: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
