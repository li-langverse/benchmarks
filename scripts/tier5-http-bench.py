#!/usr/bin/env python3
"""Tier-5 HTTP benches (nginx oracle + li-httpd). Writes lis-compatible latest.csv."""

from __future__ import annotations

import argparse
import csv
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from statistics import mean

CSV_HEADER = [
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
]


def git_sha(cwd: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=cwd, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def cpu_model() -> str:
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def kill_port(port: int) -> None:
    try:
        out = subprocess.check_output(
            ["ss", "-lptn", f"sport = :{port}"], text=True, stderr=subprocess.DEVNULL
        )
        for line in out.splitlines():
            m = re.search(r"pid=(\d+)", line)
            if m:
                os.kill(int(m.group(1)), 15)
    except (subprocess.CalledProcessError, ProcessLookupError, ValueError):
        pass
    time.sleep(0.2)


def wrk_pipeline_script() -> Path:
    script = Path("/tmp/wrk-http-pipeline.lua")
    if script.is_file():
        return script
    script.write_text(
        """init = function(args)
  depth = tonumber(args[1]) or 8
  local parts = {}
  for i = 1, depth do
    parts[i] = wrk.format("GET", wrk.path)
  end
  req = table.concat(parts)
end
request = function()
  return req
end
""",
        encoding="utf-8",
    )
    return script


def wrk_rps(url: str, *, threads: int, conn: int, duration: str, pipeline: int) -> float:
    cmd = ["wrk", f"-t{threads}", f"-c{conn}", f"-d{duration}"]
    if pipeline > 1:
        cmd.extend(["-s", str(wrk_pipeline_script()), url, "--", str(pipeline)])
    else:
        cmd.append(url)
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    for line in out.splitlines():
        if "Requests/sec:" in line:
            return float(line.split()[1])
    raise RuntimeError(f"wrk parse failed: {out[:400]}")


def bench_runs(
    url: str, *, runs: int, threads: int, conn: int, duration: str, pipeline: int
) -> float:
    samples = [
        wrk_rps(url, threads=threads, conn=conn, duration=duration, pipeline=pipeline)
        for _ in range(runs)
    ]
    return mean(samples)


def row(
    *,
    benchmark: str,
    lang: str,
    value: float,
    sha: str,
    cpu: str,
    flags: str,
    variant: str = "ci",
    threads: int = 8,
) -> dict[str, object]:
    return {
        "benchmark": benchmark,
        "lang": lang,
        "variant": variant,
        "threads": threads,
        "metric": "rps",
        "value": round(value, 2),
        "unit": "req/s",
        "git_sha": sha,
        "cpu_model": cpu,
        "flags": flags,
    }


def nginx_temp_dirs() -> None:
    base = Path("/tmp/nginx-bench")
    for name in ("client_body", "proxy", "fastcgi", "uwsgi", "scgi"):
        (base / name).mkdir(parents=True, exist_ok=True)


def nginx_temp_block() -> str:
    base = "/tmp/nginx-bench"
    return f"""
  client_body_temp_path {base}/client_body;
  proxy_temp_path {base}/proxy;
  fastcgi_temp_path {base}/fastcgi;
  uwsgi_temp_path {base}/uwsgi;
  scgi_temp_path {base}/scgi;
"""


def write_nginx_static(port: int, root: Path) -> Path:
    nginx_temp_dirs()
    root.mkdir(parents=True, exist_ok=True)
    (root / "file.bin").write_bytes(b"x" * 1024)
    conf = Path("/tmp/nginx-bench-static.conf")
    conf.write_text(
        f"""pid /tmp/nginx-bench/nginx-static.pid;
error_log /tmp/nginx-bench/error-static.log;
worker_processes 1;
events {{ worker_connections 4096; }}
http {{
  access_log off;
{nginx_temp_block()}
  server {{
    listen {port};
    root {root};
    location /file.bin {{ }}
  }}
}}
""",
        encoding="utf-8",
    )
    return conf


def write_nginx_proxy(port: int, back: int) -> Path:
    nginx_temp_dirs()
    conf = Path("/tmp/nginx-bench-proxy.conf")
    conf.write_text(
        f"""pid /tmp/nginx-bench/nginx-proxy.pid;
error_log /tmp/nginx-bench/error-proxy.log;
worker_processes 1;
events {{ worker_connections 4096; }}
http {{
  access_log off;
{nginx_temp_block()}
  upstream backend {{
    server 127.0.0.1:{back};
    keepalive 32;
  }}
  server {{
    listen {port};
    location / {{
      proxy_pass http://backend;
      proxy_http_version 1.1;
      proxy_set_header Connection "";
      proxy_buffering off;
    }}
  }}
}}
""",
        encoding="utf-8",
    )
    return conf


def start_nginx(conf: Path, port: int) -> None:
    kill_port(port)
    pid_file = conf.read_text(encoding="utf-8").split("pid ")[1].split(";")[0].strip()
    if Path(pid_file).is_file():
        subprocess.run(["nginx", "-s", "stop", "-c", str(conf)], check=False)
    subprocess.check_call(["nginx", "-c", str(conf)])


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lic-root", type=Path, default=Path(os.environ.get("LIC_ROOT", "/workspace/lic")))
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--runs", type=int, default=int(os.environ.get("HTTP_BENCH_RUNS", "5")))
    p.add_argument("--threads", type=int, default=8)
    p.add_argument("--connections", type=int, default=200)
    p.add_argument("--duration", default="10s")
    args = p.parse_args()

    lic = args.lic_root.resolve()
    httpd = lic / "build/li-httpd"
    if not httpd.is_file():
        print(f"missing {httpd} — run ./scripts/setup-lic-for-bench.sh", file=sys.stderr)
        return 1
    if not shutil.which("wrk"):
        print("install wrk", file=sys.stderr)
        return 1

    out = args.out or (lic / "benchmarks/results/http_tier5.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    sha = git_sha(lic)
    cpu = cpu_model()
    rows: list[dict[str, object]] = []

    static_root = Path("/tmp/httpd-static-root")
    static_root.mkdir(parents=True, exist_ok=True)
    (static_root / "index.html").write_text("<html><body>ok</body></html>\n", encoding="utf-8")
    (static_root / "file.bin").write_bytes(b"x" * 1024)

    proxy_root = Path("/tmp/httpd-proxy-root")
    proxy_root.mkdir(parents=True, exist_ok=True)
    (proxy_root / "index.html").write_text("ok\n", encoding="utf-8")

    static_port = 18090
    proxy_front = 18080
    proxy_back = 18081
    nginx_static = 18092
    nginx_proxy = 18082

    # --- static_small ---
    kill_port(static_port)
    subprocess.Popen(
        [str(httpd), str(static_port), str(static_root)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.4)
    li_static = bench_runs(
        f"http://127.0.0.1:{static_port}/file.bin",
        runs=args.runs,
        threads=args.threads,
        conn=args.connections,
        duration=args.duration,
        pipeline=1,
    )
    kill_port(static_port)
    rows.append(
        row(
            benchmark="static_small",
            lang="li",
            value=li_static,
            sha=sha,
            cpu=cpu,
            flags=f"wrk static_small",
            threads=args.threads,
        )
    )
    conf = write_nginx_static(nginx_static, static_root)
    start_nginx(conf, nginx_static)
    ng_static = bench_runs(
        f"http://127.0.0.1:{nginx_static}/file.bin",
        runs=args.runs,
        threads=args.threads,
        conn=args.connections,
        duration=args.duration,
        pipeline=1,
    )
    subprocess.run(["nginx", "-s", "stop", "-c", str(conf)], check=False)
    rows.append(
        row(
            benchmark="static_small",
            lang="nginx",
            value=ng_static,
            sha=sha,
            cpu=cpu,
            flags="wrk static_small",
            threads=args.threads,
        )
    )
    print(f"static_small li={li_static:.0f} nginx={ng_static:.0f}")

    # --- keepalive_pipelining ---
    kill_port(static_port)
    subprocess.Popen(
        [str(httpd), str(static_port), str(static_root)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.4)
    li_ka = bench_runs(
        f"http://127.0.0.1:{static_port}/file.bin",
        runs=args.runs,
        threads=args.threads,
        conn=args.connections,
        duration=args.duration,
        pipeline=8,
    )
    kill_port(static_port)
    rows.append(
        row(
            benchmark="keepalive_pipelining",
            lang="li",
            value=li_ka,
            sha=sha,
            cpu=cpu,
            flags="wrk pipeline=8",
            threads=args.threads,
        )
    )
    start_nginx(conf, nginx_static)
    ng_ka = bench_runs(
        f"http://127.0.0.1:{nginx_static}/file.bin",
        runs=args.runs,
        threads=args.threads,
        conn=args.connections,
        duration=args.duration,
        pipeline=8,
    )
    subprocess.run(["nginx", "-s", "stop", "-c", str(conf)], check=False)
    rows.append(
        row(
            benchmark="keepalive_pipelining",
            lang="nginx",
            value=ng_ka,
            sha=sha,
            cpu=cpu,
            flags="wrk pipeline=8",
            threads=args.threads,
        )
    )
    print(f"keepalive_pipelining li={li_ka:.0f} nginx={ng_ka:.0f}")

    # --- proxy_loopback ---
    kill_port(proxy_back)
    subprocess.Popen(
        [str(httpd), str(proxy_back), str(proxy_root)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.3)

    def proxy_bench(use_c: bool) -> float:
        kill_port(proxy_front)
        env = os.environ.copy()
        if use_c:
            env["LI_HTTPD_PROXY_C"] = "1"
        else:
            env.pop("LI_HTTPD_PROXY_C", None)
        subprocess.Popen(
            [str(httpd), str(proxy_front), str(proxy_root), str(proxy_back)],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(0.5)
        return bench_runs(
            f"http://127.0.0.1:{proxy_front}/",
            runs=args.runs,
            threads=args.threads,
            conn=args.connections,
            duration=args.duration,
            pipeline=1,
        )

    li_proxy = proxy_bench(False)
    rows.append(
        row(
            benchmark="proxy_loopback",
            lang="li",
            value=li_proxy,
            sha=sha,
            cpu=cpu,
            flags="wrk proxy_loopback li_epoll",
            variant="li_epoll",
            threads=args.threads,
        )
    )
    kill_port(proxy_front)
    li_proxy_c = proxy_bench(True)
    rows.append(
        row(
            benchmark="proxy_loopback",
            lang="li",
            value=li_proxy_c,
            sha=sha,
            cpu=cpu,
            flags="wrk proxy_loopback LI_HTTPD_PROXY_C=1",
            variant="c_epoll",
            threads=args.threads,
        )
    )
    kill_port(proxy_back)
    kill_port(proxy_front)

    pconf = write_nginx_proxy(nginx_proxy, proxy_back)
    kill_port(proxy_back)
    subprocess.Popen(
        [str(httpd), str(proxy_back), str(proxy_root)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.3)
    start_nginx(pconf, nginx_proxy)
    ng_proxy = bench_runs(
        f"http://127.0.0.1:{nginx_proxy}/",
        runs=args.runs,
        threads=args.threads,
        conn=args.connections,
        duration=args.duration,
        pipeline=1,
    )
    subprocess.run(["nginx", "-s", "stop", "-c", str(pconf)], check=False)
    kill_port(proxy_back)
    rows.append(
        row(
            benchmark="proxy_loopback",
            lang="nginx",
            value=ng_proxy,
            sha=sha,
            cpu=cpu,
            flags="wrk proxy_loopback",
            threads=args.threads,
        )
    )
    print(f"proxy_loopback li={li_proxy:.0f} li_c={li_proxy_c:.0f} nginx={ng_proxy:.0f}")

    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in CSV_HEADER})
    print(f"tier5-http-bench: wrote {len(rows)} rows -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
