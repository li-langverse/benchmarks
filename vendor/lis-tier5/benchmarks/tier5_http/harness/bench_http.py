#!/usr/bin/env python3
"""HTTP tier-5 harness — TOML verify + optional nginx/wrk RPS → results/latest.csv.

When ``nginx`` and ``wrk`` are on PATH (typical Linux CI after apt install), runs a
short load test against stock nginx serving ``fixtures/static`` and records
``lang=nginx`` ``metric=rps`` rows. ``lang=li`` rows are emitted only if
``LI_HTTPD_BIN`` points to an executable that speaks HTTP on the bench port
(not implemented yet — placeholder for li-httpd).

See ``benchmarks/tier5_http/README.md`` for local usage.
"""
from __future__ import annotations

import argparse
import csv
import os
import platform
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # py3.10
    import tomli as tomllib  # type: ignore

CSV_FIELDS = (
    "benchmark",
    "lang",
    "variant",
    "threads",
    "metric",
    "value",
    "unit",
    "git_sha",
    "cpu_model",
    "flags",
)


def tier5_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_toml(path: Path) -> dict[str, Any]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_suite(profile: str) -> tuple[list[str], bool]:
    """Return (scenario_names, timing_enabled)."""
    suite_path = tier5_root() / "suite.toml"
    data = load_toml(suite_path)
    prof = data.get("profiles", {}).get(profile)
    if not prof:
        prof = data.get("default", {})
    include = list(prof.get("include") or data.get("default", {}).get("include") or ["static_small"])
    timing = bool(prof.get("timing", data.get("default", {}).get("timing", False)))
    return include, timing


def merge_scenario(name: str) -> dict[str, Any]:
    root = tier5_root()
    defaults = load_toml(root / "defaults.toml")
    scenario_path = root / "scenarios" / name / "bench.toml"
    scenario = load_toml(scenario_path)
    out: dict[str, Any] = {"name": name}
    out["_fixtures"] = defaults.get("fixtures", {})
    out["_tools"] = defaults.get("tools", {})
    out["_load_defaults"] = defaults.get("load", {})
    out.update(scenario)
    return out


def lis_repo_root() -> Path:
    """tier5_http → benchmarks → lis repo root."""
    return tier5_root().parents[1]


def git_sha_short() -> str:
    try:
        p = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=lis_repo_root(),
            capture_output=True,
            text=True,
            check=False,
        )
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip()
    except OSError:
        pass
    return "unknown"


def cpu_model() -> str:
    return platform.processor() or platform.machine() or "unknown"


def pick_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    _, port = s.getsockname()
    s.close()
    return int(port)


def nginx_prefix_conf(document_root: Path, port: int, prefix: Path) -> str:
    dr = str(document_root.resolve()).replace("\\", "/")
    px = str(prefix.resolve()).replace("\\", "/")
    return f"""worker_processes 1;
error_log {px}/error.log warn;
pid {px}/nginx.pid;
daemon on;
events {{ worker_connections 4096; }}
http {{
  access_log off;
  sendfile on;
  client_body_temp_path {px}/client_temp;
  proxy_temp_path {px}/proxy_temp;
  fastcgi_temp_path {px}/fastcgi_temp;
  uwsgi_temp_path {px}/uwsgi_temp;
  scgi_temp_path {px}/scgi_temp;
  server {{
    listen 127.0.0.1:{port};
    server_name _;
    root {dr};
    location / {{
      try_files $uri /index.html =404;
    }}
  }}
}}
"""


def parse_wrk_rps(text: str) -> float | None:
    # "Requests/sec:   12345.67" or with thousands separators rarely
    m = re.search(r"Requests/sec:\s*([\d,.]+)", text, re.IGNORECASE)
    if not m:
        return None
    raw = m.group(1).replace(",", "")
    try:
        return float(raw)
    except ValueError:
        return None


def write_wrk_pipeline_lua(path: Path, port: int, depth: int) -> None:
    path.write_text(
        f"""-- Auto-generated for HTTP/1.1 pipelined requests (depth={depth})
local depth = {int(depth)}
request = function()
  local host = "127.0.0.1:{port}"
  local chunk = "GET / HTTP/1.1\\r\\nHost: " .. host .. "\\r\\nConnection: keep-alive\\r\\n\\r\\n"
  local r = ""
  for _ = 1, depth do
    r = r .. chunk
  end
  return r
end
""",
        encoding="utf-8",
    )


def run_wrk(
    url: str,
    threads: int,
    connections: int,
    duration_sec: int,
    lua_script: Path | None,
) -> tuple[float | None, str]:
    cmd = [
        "wrk",
        "-t",
        str(threads),
        "-c",
        str(connections),
        "-d",
        f"{duration_sec}s",
        "--latency",
    ]
    if lua_script is not None:
        cmd.extend(["-s", str(lua_script)])
    cmd.append(url)
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    blob = (proc.stdout or "") + (proc.stderr or "")
    return parse_wrk_rps(blob), blob


def launch_nginx(prefix: Path, conf_text: str) -> bool:
    prefix.mkdir(parents=True, exist_ok=True)
    for sub in ("logs", "client_temp", "proxy_temp", "fastcgi_temp", "uwsgi_temp", "scgi_temp"):
        (prefix / sub).mkdir(parents=True, exist_ok=True)
    conf_path = prefix / "nginx.conf"
    conf_path.write_text(conf_text, encoding="utf-8")
    nginx = shutil.which("nginx")
    if not nginx:
        return False
    pfx = str(prefix.resolve()) + os.sep
    proc = subprocess.run(
        [nginx, "-p", pfx, "-c", str(conf_path.resolve())],
        cwd=prefix,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        err = (proc.stderr or "") + (proc.stdout or "")
        sys.stderr.write(f"nginx start failed rc={proc.returncode}: {err}\n")
        return False
    pid_path = prefix / "nginx.pid"
    for _ in range(200):
        if pid_path.is_file():
            time.sleep(0.02)
            return True
        time.sleep(0.02)
    return False


def stop_nginx(prefix: Path) -> None:
    pid_path = prefix / "nginx.pid"
    if pid_path.is_file():
        try:
            pid = int(pid_path.read_text().strip())
            os.kill(pid, signal.SIGQUIT)
        except (ValueError, ProcessLookupError, OSError):
            pass
    # allow worker shutdown
    time.sleep(0.1)
def bench_nginx_scenario(
    name: str,
    cfg: dict[str, Any],
    *,
    quick: bool,
) -> tuple[list[dict[str, str]], str]:
    """Return CSV rows and human log tail."""
    rows: list[dict[str, str]] = []
    log_bits: list[str] = []

    load = cfg.get("load") or {}
    threads = int(load.get("threads") or cfg.get("_load_defaults", {}).get("threads") or 2)
    connections = int(load.get("connections") or 8)
    duration = int(load.get("duration_sec") or 10)
    if quick:
        duration = min(duration, int(os.environ.get("BENCH_HTTP_QUICK_SEC", "3")))
    pipeline = int(load.get("pipeline") or 1)

    fixtures = cfg.get("_fixtures", {})
    rel_static = fixtures.get("static_root", "fixtures/static")
    doc_root = tier5_root() / rel_static
    if not (doc_root / "index.html").is_file():
        rows.append(_harness_row(name, f"missing_fixture:{doc_root}"))
        return rows, "missing static fixture"

    wrk_bin = shutil.which("wrk")
    if not wrk_bin:
        rows.append(_harness_row(name, "no_wrk"))
        return rows, "wrk not found"

    port = pick_port()
    lua_path: Path | None = None
    tmp_lua: tempfile.TemporaryDirectory[str] | None = None
    if pipeline > 1:
        tmp_lua = tempfile.TemporaryDirectory(prefix="lis-wrk-")
        lua_path = Path(tmp_lua.name) / "pipeline.lua"
        write_wrk_pipeline_lua(lua_path, port, pipeline)

    tmp = tempfile.TemporaryDirectory(prefix="lis-nginx-")
    prefix = Path(tmp.name)
    conf = nginx_prefix_conf(doc_root, port, prefix)
    try:
        if not launch_nginx(prefix, conf):
            rows.append(_harness_row(name, "no_nginx"))
            return rows, "nginx not available or failed to start"

        url = f"http://127.0.0.1:{port}/"
        # small wait for bind
        for _ in range(100):
            try:
                s = socket.create_connection(("127.0.0.1", port), timeout=0.1)
                s.close()
                break
            except OSError:
                time.sleep(0.02)

        verify_cfg = cfg.get("verify") or {}
        for req in verify_cfg.get("requests") or []:
            path = req.get("path") or "/"
            expect = int(req.get("expect_status") or 200)
            if not verify_http_get(f"http://127.0.0.1:{port}{path}", expect):
                rows.append(_harness_row(name, f"verify_fail:{path}"))
                return rows, "HTTP verify failed before wrk"

        rps, blob = run_wrk(url, threads, connections, duration, lua_path)
        log_bits.append(blob[-2000:])

        variant = "ci" if quick else "release"
        sha = git_sha_short()
        cpu = cpu_model()
        flags = f"wrk pipeline={pipeline}" if pipeline > 1 else "wrk"

        if rps is not None and rps > 0:
            rows.append(
                {
                    "benchmark": name,
                    "lang": "nginx",
                    "variant": variant,
                    "threads": str(connections),
                    "metric": "rps",
                    "value": f"{rps:.4f}",
                    "unit": "req/s",
                    "git_sha": sha,
                    "cpu_model": cpu,
                    "flags": flags,
                }
            )
        else:
            rows.append(_harness_row(name, "wrk_parse_fail"))

        # Future: LI_HTTPD_BIN → start li-httpd, second wrk, lang=li row
        li_bin = os.environ.get("LI_HTTPD_BIN")
        if li_bin and Path(li_bin).is_file():
            rows.append(
                {
                    "benchmark": name,
                    "lang": "harness",
                    "variant": "stub",
                    "threads": "1",
                    "metric": "verify_only",
                    "value": "1",
                    "unit": "bool",
                    "git_sha": sha,
                    "cpu_model": cpu,
                    "flags": "li_httpd_bench_notwired",
                }
            )

    finally:
        stop_nginx(prefix)
        tmp.cleanup()
        if tmp_lua is not None:
            tmp_lua.cleanup()

    return rows, "\n".join(log_bits)


def _harness_row(name: str, flags: str) -> dict[str, str]:
    return {
        "benchmark": name,
        "lang": "harness",
        "variant": "ci",
        "threads": "1",
        "metric": "verify_only",
        "value": "1",
        "unit": "bool",
        "git_sha": git_sha_short(),
        "cpu_model": cpu_model(),
        "flags": flags,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in CSV_FIELDS})


def verify_http_get(url: str, expect_status: int = 200) -> bool:
    import urllib.error
    import urllib.request

    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return int(resp.status) == expect_status
    except (urllib.error.URLError, OSError, ValueError):
        return False


def verify_toml(name: str) -> bool:
    merge_scenario(name)
    return True


def main() -> int:
    p = argparse.ArgumentParser(description="tier5_http bench harness")
    p.add_argument("scenario", nargs="?", default=None, help="single scenario id (default: suite profile)")
    p.add_argument("--profile", default="ci", help="suite.toml profile name")
    p.add_argument("--csv", type=Path, default=None, help="output CSV (default: <repo>/results/latest.csv)")
    p.add_argument(
        "--no-bench",
        action="store_true",
        help="TOML verify + harness-only CSV rows (no nginx/wrk)",
    )
    args = p.parse_args()

    csv_path = args.csv
    if csv_path is None:
        csv_path = lis_repo_root() / "results" / "latest.csv"

    if args.scenario:
        scenarios = [args.scenario]
        _, timing = load_suite(args.profile)
    else:
        scenarios, timing = load_suite(args.profile)
    quick = not timing

    all_rows: list[dict[str, str]] = []
    for name in scenarios:
        try:
            verify_toml(name)
        except Exception as e:
            print(f"bench_http: TOML error {name}: {e}", file=sys.stderr)
            return 1
        if args.no_bench:
            all_rows.append(_harness_row(name, "no_bench_flag"))
            continue
        cfg = merge_scenario(name)
        rows, _log = bench_nginx_scenario(name, cfg, quick=quick)
        all_rows.extend(rows)

    write_csv(csv_path, all_rows)
    print(f"bench_http: wrote {len(all_rows)} row(s) -> {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())