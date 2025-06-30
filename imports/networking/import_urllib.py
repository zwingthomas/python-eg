# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/urllib.html
# urllib in depth – Real Python
#     https://realpython.com/python-urllib-request/
# ___________________________________________________________________________
"""
Hands‑on guide to Python’s **urllib** package
===========================================
The `urllib` family (`urllib.request`, `urllib.parse`, `urllib.error`,
`urllib.robotparser`) offers std‑lib tools for HTTP requests, URL handling and
robots.txt parsing.  It sits between raw `socket`/`http.client` and high‑level
clients like **requests** and **httpx**.

Feature snapshot
----------------
| Feature                         | http.client | urllib   | requests | httpx |
|---------------------------------|-------------|----------|----------|--------|
| High‑level URL opener           | ❌          | ✅       | ✅       | ✅ |
| Automatic JSON helpers          | ❌          | ❌       | ✅       | ✅ |
| Cookie & redirect handling      | ❌          | ⚠️ *      | ✅       | ✅ |
| Async API                       | ❌          | ❌       | ❌       | ✅ |
| HTTP/2                          | ❌          | ❌       | ❌       | ✅ |
| Pluggable auth/proxy handlers   | ❌          | ✅       | ✅       | ✅ |

*via HTTPCookieProcessor

Sections
--------
1.  parse_demo()                 – `urllib.parse` basics
2.  simple_get()                 – `urllib.request.urlopen`
3.  post_form()                  – encode data & custom headers
4.  custom_opener()              – add User‑Agent + redirects off
5.  error_handling()             – HTTPError & URLError
6.  robots_txt_check()           – `urllib.robotparser`
7.  ssl_context()                – validate vs ignore certs
8.  main()                       – run demos & tidy up

Run directly:

```bash
python urllib_module_tutorial.py
```
"""

from __future__ import annotations

import ssl
import sys
import urllib.error
import urllib.parse as up
import urllib.request as ur
import urllib.robotparser as rp
from pathlib import Path
from pprint import pprint

API = "https://httpbin.org"
TMP = Path(__file__).with_suffix("").with_name(Path(__file__).stem + "_tmp")
TMP.mkdir(exist_ok=True)


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# ──────────────────────────────────────────────────────────────────────────────
# 1. URL parsing helpers
# ──────────────────────────────────────────────────────────────────────────────


def parse_demo():
    h("parse_demo")
    url = "https://user:pw@example.com:8443/path;params?x=1&y=2#frag"
    parts = up.urlparse(url)
    pprint(parts._asdict())
    rebuilt = up.urlunparse(parts)
    print("round‑trip →", rebuilt)

# ──────────────────────────────────────────────────────────────────────────────
# 2. Simple GET – urlopen returns bytes
# ──────────────────────────────────────────────────────────────────────────────


def simple_get():
    h("simple_get")
    with ur.urlopen(f"{API}/get?demo=urllib", timeout=5) as resp:
        print("status:", resp.status)
        data = resp.read(80)
        print("first 80 bytes →", data)

# ──────────────────────────────────────────────────────────────────────────────
# 3. POST form data
# ──────────────────────────────────────────────────────────────────────────────


def post_form():
    h("post_form")
    import json
    fields = {"name": "Alice", "city": "Zürich"}
    data = up.urlencode(fields).encode()
    req = ur.Request(f"{API}/post", data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with ur.urlopen(req) as resp:
        print("server responded Content‑Type →",
              resp.headers.get("Content-Type"))
        body = json.loads(resp.read())  # httpbin always returns JSON
        pprint(body["form"])

# ──────────────────────────────────────────────────────────────────────────────
# 4. Custom opener (User-Agent / disable redirects)
# ──────────────────────────────────────────────────────────────────────────────


def custom_opener():
    h("custom_opener")
    opener = ur.build_opener(ur.HTTPRedirectHandler)
    opener.addheaders = [("User-Agent", "urllib-demo/0.1")]
    req = ur.Request(f"{API}/redirect/1")
    req.method = "GET"
    try:
        opener.open(req)
    except urllib.error.HTTPError as exc:
        print("redirect blocked – status", exc.code)

# ──────────────────────────────────────────────────────────────────────────────
# 5. Error handling
# ──────────────────────────────────────────────────────────────────────────────


def error_handling():
    h("error_handling")
    try:
        ur.urlopen("https://nosuch.invalid/", timeout=2)
    except urllib.error.URLError as exc:
        print("URLError reason →", exc.reason)

    try:
        ur.urlopen(f"{API}/status/418")
    except urllib.error.HTTPError as exc:
        print("HTTPError status →", exc.code, exc.reason)

# ──────────────────────────────────────────────────────────────────────────────
# 6. robots.txt parsing
# ──────────────────────────────────────────────────────────────────────────────


def robots_txt_check():
    h("robots_txt_check")
    robot = rp.RobotFileParser()
    robot.set_url("https://www.python.org/robots.txt")
    robot.read()
    print("Allowed /dev?", robot.can_fetch("demo‑bot", "/dev"))

# ──────────────────────────────────────────────────────────────────────────────
# 7. SSL context tweak – ignore invalid certs (⚠️ don’t in prod!)
# ──────────────────────────────────────────────────────────────────────────────


def ssl_context():
    h("ssl_context")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with ur.urlopen("https://self-signed.badssl.com/", context=ctx, timeout=5) as resp:
            print("status ignoring cert →", resp.status)
    except Exception as exc:
        print("SSL demo failed (network?) →", exc)

# ──────────────────────────────────────────────────────────────────────────────
# 8. main
# ──────────────────────────────────────────────────────────────────────────────


def main():
    parse_demo()
    simple_get()
    post_form()
    custom_opener()
    error_handling()
    robots_txt_check()
    ssl_context()

    for p in TMP.iterdir():
        p.unlink()
    TMP.rmdir()


if __name__ == "__main__":
    main()
