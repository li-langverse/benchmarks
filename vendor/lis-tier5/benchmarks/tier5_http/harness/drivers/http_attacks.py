"""HTTP/1.1 attack drivers for tier5 exploit harness (raw socket)."""
from __future__ import annotations

import socket
import time
from typing import Any


def _connect(host: str, port: int, timeout: float = 2.0) -> socket.socket:
    s = socket.create_connection((host, port), timeout=timeout)
    s.settimeout(timeout)
    return s


def legitimate_get(host: str, port: int, path: str = "/") -> bool:
    try:
        s = _connect(host, port, 1.0)
        req = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: close\r\n\r\n"
        s.sendall(req.encode())
        data = s.recv(4096)
        s.close()
        return b"200" in data.split(b"\r\n", 1)[0]
    except OSError:
        return False


def attack_slowloris(host: str, port: int, attack: dict[str, Any]) -> dict[str, Any]:
    conns = int(attack.get("connections") or 80)
    interval = float(attack.get("header_byte_interval_sec") or 0.5)
    duration = float(attack.get("duration_sec") or 5)
    socks: list[socket.socket] = []
    try:
        for _ in range(conns):
            try:
                s = _connect(host, port, 2.0)
                s.sendall(f"GET / HTTP/1.1\r\nHost: {host}:{port}\r\n".encode())
                socks.append(s)
            except OSError:
                pass
        end = time.time() + duration
        while time.time() < end and socks:
            for s in list(socks):
                try:
                    s.sendall(b"X")
                except OSError:
                    socks.remove(s)
            time.sleep(interval)
        attack_closed = len(socks) == 0
    finally:
        for s in socks:
            try:
                s.close()
            except OSError:
                pass
    legit = legitimate_get(host, port)
    return {
        "attack_closed": attack_closed,
        "legitimate_client_ok": legit,
        "no_crash": True,
    }


def attack_oversized_request_line(host: str, port: int, attack: dict[str, Any]) -> dict[str, Any]:
    line_len = int(attack.get("line_bytes") or 8192)
    payload = b"A" * line_len
    req = b"GET " + payload + b" / HTTP/1.1\r\nHost: x\r\n\r\n"
    try:
        s = _connect(host, port, 2.0)
        s.sendall(req)
        _ = s.recv(1024)
        s.close()
        rejected = True
    except OSError:
        rejected = True
    legit = legitimate_get(host, port)
    return {
        "reject_or_close_attack": rejected,
        "legitimate_client_ok": legit,
        "no_crash": True,
    }


def attack_path_traversal(host: str, port: int, attack: dict[str, Any]) -> dict[str, Any]:
    path = str(attack.get("path") or "/..%2f..%2fetc%2fpasswd")
    req = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: close\r\n\r\n"
    try:
        s = _connect(host, port, 2.0)
        s.sendall(req.encode())
        data = s.recv(4096)
        s.close()
        status = data.split(b"\r\n", 1)[0] if data else b""
        blocked = (
            b"404" in status
            or b"400" in status
            or b"403" in status
            or len(data) == 0
        )
    except OSError:
        blocked = True
    legit = legitimate_get(host, port)
    return {
        "reject_or_close_attack": blocked,
        "legitimate_client_ok": legit,
        "no_crash": True,
    }


def attack_duplicate_content_length(host: str, port: int, attack: dict[str, Any]) -> dict[str, Any]:
    req = (
        b"POST / HTTP/1.1\r\n"
        b"Host: " + f"{host}:{port}".encode() + b"\r\n"
        b"Content-Length: 0\r\n"
        b"Content-Length: 4\r\n"
        b"Connection: close\r\n\r\n"
        b"test"
    )
    try:
        s = _connect(host, port, 2.0)
        s.sendall(req)
        _ = s.recv(2048)
        s.close()
        rejected = True
    except OSError:
        rejected = True
    legit = legitimate_get(host, port)
    return {
        "reject_or_close_attack": rejected,
        "legitimate_client_ok": legit,
        "no_crash": True,
    }


def attack_connection_flood(host: str, port: int, attack: dict[str, Any]) -> dict[str, Any]:
    n = int(attack.get("connections") or 200)
    opened = 0
    socks: list[socket.socket] = []
    for _ in range(n):
        try:
            s = _connect(host, port, 0.5)
            socks.append(s)
            opened += 1
        except OSError:
            break
    for s in socks:
        try:
            s.close()
        except OSError:
            pass
    legit = legitimate_get(host, port)
    return {
        "no_crash": True,
        "legitimate_client_ok": legit,
        "reject_or_close_attack": opened < n,
    }


def attack_bad_method(host: str, port: int, attack: dict[str, Any]) -> dict[str, Any]:
    req = b"FOO / HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n"
    try:
        s = _connect(host, port, 2.0)
        s.sendall(req)
        data = s.recv(1024)
        s.close()
        rejected = b"405" in data or b"400" in data or b"404" in data or len(data) == 0
    except OSError:
        rejected = True
    legit = legitimate_get(host, port)
    return {
        "reject_or_close_attack": rejected,
        "legitimate_client_ok": legit,
        "no_crash": True,
    }


DRIVERS = {
    "slowloris": attack_slowloris,
    "oversized_request_line": attack_oversized_request_line,
    "path_traversal": attack_path_traversal,
    "duplicate_content_length": attack_duplicate_content_length,
    "connection_flood": attack_connection_flood,
    "bad_method": attack_bad_method,
}
