# HTTP benchmarks vs nginx (tier-5)

## Oracle

[`catalog.toml`](../../catalog.toml) rows `static_small` and `keepalive_pipelining` use `compare_oracle = "nginx"` and metric **`rps`**. The dashboard shows **`ratio_vs_reference`** only when both **`lang=nginx`** and **`lang=li`** RPS rows exist (threshold `1.0` = match or beat nginx on throughput).

## Repos

| Repo | Role |
|------|------|
| **lis** | `benchmarks/tier5_http/harness/bench_http.py` — stock nginx + wrk → `results/latest.csv` |
| **benchmarks** | Ingest (`ingest-lic.sh`, `merge_lis_http_into_summary.py`), plots (`plot_http_benchmarks.py`), dashboard |
| **lic** | `packages/li-net-httpd` + `runtime/li_rt_net.c` — M0 **`li-httpd`** (`lang=li` rows when `build/li-httpd` exists) |

Until **lis** `main` ships the harness, **benchmarks** vendors a copy under [`vendor/lis-tier5/`](../../vendor/lis-tier5/README.md). Sync with `./scripts/sync-lis-tier5-vendor.sh`.

## Local run

```bash
sudo apt-get install -y nginx wrk
pip install matplotlib  # optional plots

# Bench (vendor or lis checkout)
python3 vendor/lis-tier5/benchmarks/tier5_http/harness/bench_http.py --profile ci

# Merge HTTP into dashboard data without wiping lic rows (when lic CSV absent)
python3 scripts/ingest/merge_lis_http_into_summary.py vendor/lis-tier5/results/latest.csv

# Plots
LIS_ROOT=$PWD/vendor/lis-tier5 ./scripts/run-http-benchmark-report.sh
```

Full ingest when **lic** `benchmarks/results/latest.csv` exists:

```bash
LIC_ROOT=../lic LIS_ROOT=../lis ./scripts/ingest/ingest-lic.sh
```

## CI

- **Benchmarks CI** runs vendored `bench_http.py`, then `ingest-lic.sh` (HTTP merge if no lic CSV).
- **Ingest workflow** accepts `repository_dispatch` types `lic-bench-complete` and `lis-bench-complete`.

## Li vs nginx (M0 static server, local ci profile)

Example measured rows (`bench_http.py --profile ci`, Linux):

| Scenario | nginx RPS | li RPS (`build/li-httpd`) | nginx/li (dashboard `ratio_vs_reference`) |
|----------|-----------|---------------------------|-------------------------------------------|
| `static_small` | ~66k | ~13k | ~5.25 (red until ≤1.0 threshold) |
| `keepalive_pipelining` | ~76k | ~12k | ~6.21 |

M0 **li-httpd** uses trusted POSIX seam [`runtime/li_rt_net.c`](https://github.com/li-langverse/lic/blob/main/runtime/li_rt_net.c) (fork-per-connection, minimal HTTP/1.1). Not yet a proved Li parser/router.

## Why Li is ~5–9× slower (root cause, quantified)

The dashboard **`ratio_vs_reference`** is **nginx RPS ÷ li RPS** (values **> 1.0** are red). The gap is expected for M0: the benchmark stresses **connection handling**, not parsing a large static file (~100-byte `index.html`).

### Measured on this host (`bench_http.py --profile ci`, 3s wrk)

| Scenario | nginx RPS | li RPS | Ratio |
|----------|-----------|--------|-------|
| `static_small` (t2, c4) | ~79k | ~8.6k | **~9.2×** |
| `keepalive_pipelining` (t2, c16, pipeline=8) | ~67k | ~9.5k | **~7.1×** |

Fairness controls (same fixture, nginx config matches harness: `sendfile on`, temp paths under prefix):

| Config | nginx RPS | li RPS | Ratio |
|--------|-----------|--------|-------|
| wrk `-t1 -c1` (single connection) | ~37.6k | ~6.3k | **~6.0×** |
| wrk `-t2 -c4` | ~49.2k | ~8.7k | **~5.7×** |
| pipelined lua depth=8, `-c16` | ~73.3k | ~13.0k | **~5.6×** |

So the gap is **not** only “more wrk connections” — even at **c=1**, nginx is ~**6×** faster because it serves many requests per connection while Li closes after one response.

### Primary causes (in impact order)

1. **`Connection: close` + no keep-alive loop** — every response forces a new TCP connection under load. During `wrk -t2 -c4`, **established connections to the listen port** peaked at **~1175 (li)** vs **~21 (nginx)** on the same 300ms sample: Li pays accept + teardown continuously; nginx reuses a small connection pool.

2. **`fork()` per `accept()`** — child handles one `recv`, then exits; parent runs `waitpid(-1, WNOHANG)` in the accept loop. Micro-bench: **~53 µs/fork+reap**, **~19k processes/s** theoretical ceiling if each request required a new process. At **~8–13k RPS**, fork+process spawn is a large fraction of wall time.

3. **Pipelining mismatch (`keepalive_pipelining`)** — wrk’s lua script sends **8** `GET /` requests per connection with `Connection: keep-alive`. Li does **one** `recv(8192)`, returns **one** `HTTP/1.1` response, then closes. Probe: 8× pipelined GET → **1** response, `Connection: close` (body ~100 bytes total). Nginx drains the pipeline; Li under-serves the workload wrk counts as “requests”.

4. **No `sendfile`** — nginx config enables **`sendfile on`**; Li **`open` → `read` entire file into `malloc` → `send`**. For a tiny file this is secondary to (1–3) but adds copies and allocator traffic per request.

5. **No event reactor / worker pool** — single-threaded accept loop + processes; nginx uses an event-driven worker with **`worker_connections 4096`**.

### What would *not* fix the gap alone

- Faster `GET` parsing on a ~100-byte file (negligible vs fork + connection churn).
- Li codegen / proof work without changing the C server's connection model.

### Fixes that would move the ratio toward ≤1.0

1. **HTTP/1.1 keep-alive** in the same worker (no per-request `fork`).
2. **Pipeline drain** — read/process multiple requests per connection until EOF or timeout.
3. **`sendfile(2)`** (or equivalent zero-copy) for static bodies.
4. **Event loop** (`epoll`/`kqueue`) + fixed thread pool (match nginx architecture class).

Re-bench after each step; expect the largest win from **(1)+(2)** before micro-optimizing reads.

## Next steps

1. Merge **lic** branch `cursor/httpd-serve-m0-54aa` (human push — bot 403).
2. Merge **benchmarks** #45 and **lis** harness PR; drop **vendor/lis-tier5** when upstream has harness.
3. Parser proofs, keep-alive in Li server, async reactor — close gap vs nginx.
