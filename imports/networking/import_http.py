# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/http.client.html
#     https://docs.python.org/3/library/http.server.html
#     https://docs.python.org/3/library/urllib.parse.html
# Other libraries for comparison
#     https://docs.python-requests.org/
#     https://www.python-httpx.org/
# ChatGPT - model o3

"""
Python's built-in **http** stack: `http.client`, `http.server`, `urllib.parse`
============================================================================
This tutorial contrasts the low-level std-lib approach with higher-level
packages like **requests** and **httpx** while providing runnable examples.
No third-party dependencies are required.

TL;DR differences #TODO: Mezmorize this
-----------------
* **http.client** - very low level; you create a connection, craft headers &
  send bytes.  No JSON helpers, no automatic redirects, no connection pooling.
* **requests** - sync, high-level, batteries-included; automatic JSON,
  sessions, cookies, retry, redirects, file uploads.
* **httpx** - requests-style API *plus* first-class **async** support and
  HTTP/2.  Extra dependency but extremely feature-rich.

Sections
--------
1.  parse_url()               - dissect URLs with `urllib.parse`
2.  simple_get()              - blocking GET with http.client
3.  post_json()               - send JSON, read JSON manually
4.  chunked_download()        - stream & write to file
5.  tiny_http_server()        - 5-line "Hello" server with `http.server`
6.  requests_vs_httpx()       - side-by-side (only if packages available)
7.  main()                    - run all demos

Run directly:

```bash
python import_http.py
```
"""

from __future__ import annotations

import json
import os
import sys
import threading
import time
from http import client, server
from pathlib import Path
from pprint import pprint
from urllib import parse

TMP_DIR = Path(__file__).with_suffix("").name + "_tmp"
Path(TMP_DIR).mkdir(exist_ok=True)

# ————————————————————————————————————————————————————————————————
# Helpers
# ————————————————————————————————————————————————————————————————


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)


API_HOST = "httpbin.org"

# ————————————————————————————————————————————————————————————————
# 1. URL parsing with urllib.parse
# ————————————————————————————————————————————————————————————————


def parse_url():
    # urllib
    h("parse_url")
    url = "https://example.com:8443/path/to?q=pythøn#frag"
    parts = parse.urlsplit(url)
    pprint(parts._asdict())
    rebuilt = parse.urlunsplit(parts)
    print("round-trip ->", rebuilt)

# ————————————————————————————————————————————————————————————————
# 2. Low-level GET request
# ————————————————————————————————————————————————————————————————


def simple_get():
    # TODO: Mezmorize
    h("simple_get")
    conn = client.HTTPSConnection(API_HOST, timeout=5)
    conn.request("GET", "/get?demo=stdlib")
    resp = conn.getresponse()
    print("status:", resp.status, resp.reason)
    print("hdrs  :", dict(resp.getheaders()))
    body = resp.read()  # bytes
    print("body  → first 80 bytes:", body[:80])
    conn.close()

# ————————————————————————————————————————————————————————————————
# 3. POST JSON (manual encode/decode)
# ————————————————————————————————————————————————————————————————


def post_json():
    h("post_json")
    data = {"msg": "hello http.client"}
    payload = json.dumps(data).encode()

    conn = client.HTTPSConnection(API_HOST)
    conn.request(
        "POST",
        "/post",
        body=payload,
        headers={"Content-Type": "application/json",
                 "Content-Length": str(len(payload))},
    )
    resp = conn.getresponse()
    print("status:", resp.status)
    resp_body = json.loads(resp.read())  # must decode manually
    pprint(resp_body["json"])
    conn.close()

# ————————————————————————————————————————————————————————————————
# 4. Stream large file via chunked reading
# ————————————————————————————————————————————————————————————————


def chunked_download():
    h("chunked_download")
    path = Path(TMP_DIR) / "uuid.json"
    conn = client.HTTPSConnection(API_HOST)
    conn.request("GET", "/uuid")  # tiny JSON but demo stands
    resp = conn.getresponse()
    with path.open("wb") as f:
        while chunk := resp.read(16):  # small chunk size for illustration
            f.write(chunk)
    conn.close()
    print("wrote", path, "→", path.read_text())

# ————————————————————————————————————————————————————————————————
# 5. Tiny HTTP server (blocking)
# ————————————————————————————————————————————————————————————————


def tiny_http_server():
    h("tiny_http_server")

    class Handler(server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Hello from stdlib server!\n")

        def log_message(self, fmt, *args):  # silence console spam
            return

    srv = server.HTTPServer(("localhost", 0), Handler)  # 0 → random free port
    port = srv.server_port
    print("serving on", port)

    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()

    # simple client fetch via http.client
    conn = client.HTTPConnection("localhost", port)
    conn.request("GET", "/")
    resp = conn.getresponse()
    print("client got:", resp.read().decode().strip())
    conn.close()

    srv.shutdown()
    thread.join()

# ————————————————————————————————————————————————————————————————
# 6. Quick comparison: requests & httpx (if installed)
# ————————————————————————————————————————————————————————————————


def requests_vs_httpx():
    # TODO: Mezmorize
    h("requests_vs_httpx")
    try:
        import requests

        r = requests.get(f"https://{API_HOST}/get", params={"lib": "requests"})
        print("requests status:", r.status_code,
              "auto-json:", r.json()["args"])
    except ImportError:
        print("requests not installed → skip demo")

    try:
        import httpx

        with httpx.Client() as client_httpx:
            r = client_httpx.get(
                f"https://{API_HOST}/get", params={"lib": "httpx"})
            print("httpx status:", r.status_code,
                  "auto-json:", r.json()["args"])
    except ImportError:
        print("httpx not installed → skip demo")

    print("Note how both high-level libs auto-decode JSON, manage redirects, etc.")

# ————————————————————————————————————————————————————————————————
# 7. main
# ————————————————————————————————————————————————————————————————


def main():
    parse_url()
    simple_get()
    post_json()
    chunked_download()
    tiny_http_server()
    requests_vs_httpx()

    # clean files
    for p in Path(TMP_DIR).iterdir():
        p.unlink()
    Path(TMP_DIR).rmdir()


if __name__ == "__main__":
    main()
