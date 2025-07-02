# Acknowledgements__________________________________________________________
# requests docs
#     https://docs.python-requests.org/
# urllib3 docs (under‑the‑hood pool‑manager)
#     https://urllib3.readthedocs.io/
# ___________________________________________________________________________
"""
Executable guide to **requests** - Python's defacto HTTP client
================================================================
Requests is *sync-only* but extremely ergonomic, sitting between the stdlib
`http.client` (very low-level) and **httpx** (sync *and* async, HTTP/2).  This
script demonstrates the most useful patterns and highlights what requests does
—or doesn't—give you compared with those libraries.

Feature comparison
------------------
| Feature                       | http.client | requests | httpx |
|-------------------------------|-------------|----------|--------|
| High-level API (Sessions)     | ❌          | ✅       | ✅ |
| Automatic JSON encode/decode  | ❌          | ✅       | ✅ |
| Cookie persistence            | ❌          | ✅       | ✅ |
| Async/await support           | ❌          | ❌       | ✅ |
| HTTP/2 out-of-box             | ❌          | ❌       | ✅ |
| Built-in retries              | ❌          | ⚠️ *     | ⚠️ |
| File upload helpers           | ❌          | ✅       | ✅ |
* via urllib3 `Retry`
** via custom transport

Sections
--------
1.  quick_get()                 - hello world
2.  session_reuse()             - why `requests.Session()` matters
3.  post_json()                 - auto JSON & headers
4.  upload_file()               - multipart/form-data
5.  stream_large_download()     - chunked read with progress
6.  timeout_and_retry()         - urllib3 Retry with back-off
7.  auth_and_cookies()          - Basic Auth & persisting cookies
8.  main()                      - run demos & clean up

> Requires `requests>=2.31` (but any 2.x likely okay).  Install: `pip install requests`.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from pprint import pprint

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

API = "https://httpbin.org"
TMP = Path(__file__).with_suffix("").name + "_tmp"
Path(TMP).mkdir(exist_ok=True)


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# ──────────────────────────────────────────────────────────────────────
# 1. Quick GET
# ──────────────────────────────────────────────────────────────────────


def quick_get():
    # TODO
    h("quick_get")
    r = requests.get(f"{API}/get", params={"lib": "requests"}, timeout=5)
    print(r.status_code, r.url)
    print("JSON args →", r.json()["args"])

# ──────────────────────────────────────────────────────────────────────
# 2. Session reuse & connection pooling
# ──────────────────────────────────────────────────────────────────────


def session_reuse():
    # TODO
    h("session_reuse")
    with requests.Session() as s:
        for _ in range(3):
            print(s.get(f"{API}/uuid").json()["uuid"])
        # cookies persist across calls automatically

# ──────────────────────────────────────────────────────────────────────
# 3. POST JSON (headers auto-set)
# ──────────────────────────────────────────────────────────────────────


def post_json():
    h("post_json")
    payload = {"hello": "world"}
    r = requests.post(f"{API}/post", json=payload, timeout=5)
    pprint(r.json()["json"])

# ──────────────────────────────────────────────────────────────────────
# 4. File upload (multipart/form-data)
# ──────────────────────────────────────────────────────────────────────


def upload_file():
    h("upload_file")
    tmp_file = Path(TMP) / "demo.txt"
    tmp_file.write_text("upload demo")
    with tmp_file.open("rb") as f:
        r = requests.post(f"{API}/post", files={"file": f})
    print("server saw →", r.json()["files"])  # base64‑encoded by httpbin

# ──────────────────────────────────────────────────────────────────────
# 5. Streaming download with progress bar
# ──────────────────────────────────────────────────────────────────────


def stream_large_download():
    h("stream_large_download")
    dest = Path(TMP) / "bytes.bin"
    with requests.get(f"{API}/stream-bytes/20480", stream=True) as r:
        r.raise_for_status()
        with dest.open("wb") as f:
            for chunk in r.iter_content(chunk_size=4096):
                f.write(chunk)
    print("wrote", dest, "bytes", dest.stat().st_size)

# ──────────────────────────────────────────────────────────────────────
# 6. Timeouts + robust retry logic via urllib3
# ──────────────────────────────────────────────────────────────────────


def timeout_and_retry():
    h("timeout_and_retry")
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,  # return final Response instead of raising
    )
    adapter = HTTPAdapter(max_retries=retry)
    with requests.Session() as s:
        s.mount("https://", adapter)
        r = s.get(f"{API}/status/503")  # httpbin cycles status each call
        print("final status after retries:", r.status_code)

# ──────────────────────────────────────────────────────────────────────
# 7. Auth & cookie persistence
# ──────────────────────────────────────────────────────────────────────


def auth_and_cookies():
    h("auth_and_cookies")
    # Basic auth endpoint echoes credentials on success
    r = requests.get(f"{API}/basic-auth/user/passwd", auth=("user", "passwd"))
    print("auth ok?", r.json()["authenticated"])

    with requests.Session() as s:
        s.get(f"{API}/cookies/set?flavor=choc")
        jars = s.cookies.get_dict()
        print("session cookies →", jars)

# ──────────────────────────────────────────────────────────────────────
# 8. main
# ──────────────────────────────────────────────────────────────────────


def main():
    quick_get()
    session_reuse()
    post_json()
    upload_file()
    stream_large_download()
    timeout_and_retry()
    auth_and_cookies()

    for p in Path(TMP).iterdir():
        p.unlink()
    Path(TMP).rmdir()


if __name__ == "__main__":
    if tuple(int(x) for x in requests.__version__.split(".")[:2]) < (2, 20):
        print("requests ≥2.20 recommended", file=sys.stderr)
    main()
