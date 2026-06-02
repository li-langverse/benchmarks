#!/usr/bin/env python3
from __future__ import annotations

import tempfile
from pathlib import Path

from bench_http import openssl_https_rps, openssl_s_client_handshake_rps
from http_oracles import pick_port, start_lighttpd_https_bench, stop_lighttpd_proxy_bench
from tls_certs import TlsCertSpec, generate_tls_material


def main() -> None:
    port = pick_port()
    doc = Path(tempfile.mkdtemp())
    (doc / "index.html").write_text("x" * 900 + "\n")
    tmp = tempfile.TemporaryDirectory()
    mat = generate_tls_material(Path(tmp.name), TlsCertSpec(id="rsa2048-leaf"))
    assert mat is not None
    ctx = start_lighttpd_https_bench(port, doc, mat.cert, mat.key)
    try:
        print(f"lighttpd s_client hs: {openssl_s_client_handshake_rps(port, 3):.2f} conn/s")
        print(f"lighttpd s_time hs: {openssl_https_rps(port, 3):.2f} conn/s")
    finally:
        stop_lighttpd_proxy_bench(ctx)


if __name__ == "__main__":
    main()
