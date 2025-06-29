# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/socket.html
# selectors docs (efficient I/O multiplexing)
#     https://docs.python.org/3/library/selectors.html
# ___________________________________________________________________________
"""
Executable tour of Python’s **socket** standard‑library module
==============================================================
`socket` is the foundation layer beneath high‑level HTTP packages such as
**requests** and **httpx**.  Here you’ll build a tiny TCP echo service, fire a
UDP datagram, and peek at non‑blocking I/O with **selectors**.

Compared with requests / httpx
------------------------------
| Feature                       | socket      | requests  | httpx |
|-------------------------------|-------------|-----------|--------|
| Raw TCP / UDP access          | ✅          | ❌        | ❌ |
| Automatic HTTP handling       | ❌          | ✅        | ✅ |
| Async API (high‑level)        | ❌ (low‑level only) | ❌ | ✅ |
| SSL convenience               | ⚠️ via `ssl.wrap_socket` | ✅ | ✅ |

Sections
--------
1.  tcp_echo_server()          –  threaded echo server on localhost
2.  tcp_client()               –  connect, send, recv
3.  udp_demo()                 –  fire‑and‑forget datagram
4.  nonblocking_select()       –  chatty client using selectors
5.  common_pitfalls()          –  address family, bytes vs str, lingering sockets
6.  main()                     –  orchestrate demos & tidy up

Run directly:

```bash
python socket_module_tutorial.py
```
"""

from __future__ import annotations

import selectors
import socket
import threading
import time
from pathlib import Path

TMP_DIR = Path(__file__).with_suffix(
    "").with_name(Path(__file__).stem + "_tmp")
TMP_DIR.mkdir(exist_ok=True)

HOST = "127.0.0.1"  # loop-back only
"127.0.0.1"  # loop‑back only

# ──────────────────────────────────────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────────────────────────────────────


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# ──────────────────────────────────────────────────────────────────────────────
# 1. Minimal threaded TCP echo server
# ──────────────────────────────────────────────────────────────────────────────


def tcp_echo_server():
    h("tcp_echo_server (start)")

    def handler(conn: socket.socket, addr):
        with conn:
            while data := conn.recv(1024):
                conn.sendall(data)  # echo straight back

    def server_thread(sock: socket.socket):
        with sock:
            while True:
                try:
                    conn, addr = sock.accept()
                except OSError:  # socket closed
                    break
                threading.Thread(target=handler, args=(
                    conn, addr), daemon=True).start()

    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.bind((HOST, 0))  # 0 → random free port
    srv_sock.listen()
    port = srv_sock.getsockname()[1]
    threading.Thread(target=server_thread, args=(
        srv_sock,), daemon=True).start()
    print("echo server listening on", port)
    return port, srv_sock  # caller will close sock on shutdown

# ──────────────────────────────────────────────────────────────────────────────
# 2. TCP client: connect, send, recv
# ──────────────────────────────────────────────────────────────────────────────


def tcp_client(port: int):
    h("tcp_client")
    with socket.create_connection((HOST, port), timeout=5) as sock:
        msg = b"Hello, echo!"
        sock.sendall(msg)
        data = sock.recv(1024)
        print("sent:", msg, "received:", data)

# ──────────────────────────────────────────────────────────────────────────────
# 3. UDP one‑way demo
# ──────────────────────────────────────────────────────────────────────────────


def udp_demo():
    h("udp_demo")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # DNS port, packet will be dropped but demo stands
        s.sendto(b"ping", ("1.1.1.1", 53))
        print("udp packet length 4 sent to 1.1.1.1:53 (fire‑and‑forget)")

# ──────────────────────────────────────────────────────────────────────────────
# 4. Non‑blocking I/O with selectors (simple chatty client)
# ──────────────────────────────────────────────────────────────────────────────


def nonblocking_select(port: int):
    h("nonblocking_select")
    sel = selectors.DefaultSelector()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    try:
        sock.connect_ex((HOST, port))  # non‑blocking connect
        sel.register(sock, selectors.EVENT_WRITE)
        while True:
            for key, events in sel.select(timeout=1):
                if events & selectors.EVENT_WRITE:
                    sock.sendall(b"NB hello\n")
                    sel.modify(sock, selectors.EVENT_READ)
                elif events & selectors.EVENT_READ:
                    data = sock.recv(1024)
                    print("got:", data)
                    return
    finally:
        sel.unregister(sock)
        sock.close()

# ──────────────────────────────────────────────────────────────────────────────
# 5. Common pitfalls & advice
# ──────────────────────────────────────────────────────────────────────────────


def common_pitfalls():
    h("common_pitfalls")
    print("* socket.send wants bytes, NOT str (encode first)")
    print("* .recv may return less than requested; loop until all data read")
    print("* AF_INET6 vs AF_INET mismatch causes connection errors")
    print("* Always close() or use `with` so sockets release ports quickly")
    print("* TCP handshake is blocking by default – use setblocking(False) + selectors for high concurrency")

# ──────────────────────────────────────────────────────────────────────────────
# 6. main orchestrator
# ──────────────────────────────────────────────────────────────────────────────


def main():
    port, srv_sock = tcp_echo_server()
    time.sleep(0.2)  # tiny pause to ensure server listening
    try:
        tcp_client(port)
        udp_demo()
        nonblocking_select(port)
        common_pitfalls()
    finally:
        srv_sock.close()
        time.sleep(0.2)
        for p in TMP_DIR.iterdir():
            p.unlink()
        TMP_DIR.rmdir()


if __name__ == "__main__":
    main()
