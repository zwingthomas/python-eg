# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/uuid.html
# RFC 4122 – A Universally Unique Identifier (UUID) URN Namespace
# ChatGPT - model o3

"""
Executable guide to Python’s **uuid** module
===========================================
UUIDs are 128‑bit identifiers with well‑defined variants (v1, v4, v5…).  This
script shows how to generate, inspect, and safely use them—including security
notes on MAC leakage and collision probability.

Sections
--------
1.  uuid_versions_overview()    – v1, v4, v5 quick look
2.  uuid1_node_clockseq()       – MAC + timestamp introspection & privacy
3.  uuid4_collision_demo()      – birthday‑paradox math
4.  deterministic_uuid5()       – namespaced IDs (DNS, URL) & salt hack
5.  uuid_bytes_int_fields()     – convert to bytes/int, custom variant bits
6.  uuid_from_random_or_hash()  – build UUID from 16‑byte source
7.  performance_benchmark() ★   – v4 vs secrets.token_hex timing
8.  pitfalls()                  – sort order, truncation, v1 privacy
9.  main()

Run directly:
```bash
python uuid_module_tutorial.py
```
"""

from __future__ import annotations

import math
import secrets
import time
import uuid
from hashlib import sha256
from pprint import pprint
from timeit import timeit


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# 1. Overview -----------------------------------------------------------------


def uuid_versions_overview():
    h("uuid_versions_overview")
    print("v1 (time+MAC) →", uuid.uuid1())
    print("v4 (random)   →", uuid.uuid4())
    ns = uuid.NAMESPACE_DNS
    print("v5 (SHA‑1) www.example.com →", uuid.uuid5(ns, "www.example.com"))

# 2. Inspect v1 internals ------------------------------------------------------


def uuid1_node_clockseq():
    h("uuid1_node_clockseq")
    u = uuid.uuid1()
    ts = (u.time - 0x01B21DD213814000) / 1e7 + 0  # 100‑ns to epoch secs
    print("timestamp     →", time.strftime(
        "%Y‑%m‑%d %H:%M:%S", time.gmtime(ts)))
    print("node (MAC)    →", f"{u.node:012x}")
    print("clock_seq     →", u.clock_seq)

# 3. Collision probability for v4 --------------------------------------------


def uuid4_collision_demo():
    h("uuid4_collision_demo")
    n = 2 ** 24  # 16.7M
    prob = 1 - math.exp(-n * (n - 1) / (2 * 2 ** 122))
    print(f"{n:,} v4 UUIDs → collision prob ≈ {prob:.3e}")

# 4. Deterministic v5 ----------------------------------------------------------


def deterministic_uuid5():
    h("deterministic_uuid5")
    ns_url = uuid.NAMESPACE_URL
    user_id = "user42"
    salt = "2025‑06"  # rotate monthly
    det = uuid.uuid5(ns_url, salt + ":" + user_id)
    print("deterministic ID →", det)

# 5. Raw bytes / int / custom variant ----------------------------------------


def uuid_bytes_int_fields():
    h("uuid_bytes_int_fields")
    u = uuid.uuid4()
    print("bytes →", u.bytes)
    print("int   →", u.int)
    print("fields→", u.fields)

# 6. From 16‑byte source -------------------------------------------------------


def uuid_from_random_or_hash():
    h("uuid_from_random_or_hash")
    rand16 = secrets.token_bytes(16)
    u_rand = uuid.UUID(bytes=rand16, version=4)
    print("from token_bytes →", u_rand)
    hsh = sha256(b"seed").digest()[:16]
    u_hash = uuid.UUID(bytes=hsh, version=4)
    print("from sha256(seed) →", u_hash)

# 7. Timing v4 vs token_hex ----------------------------------------------------


def performance_benchmark():
    h("performance_benchmark")
    v4_time = timeit("uuid.uuid4()", setup="import uuid", number=10000)
    tok_time = timeit("secrets.token_hex(16)",
                      setup="import secrets", number=10000)
    print("uuid4 per call  →", f"{v4_time/1e4*1e6:.1f} µs")
    print("token_hex per call →", f"{tok_time/1e4*1e6:.1f} µs")

# 8. Pitfalls -----------------------------------------------------------------


def pitfalls():
    h("pitfalls")
    print("* v1 leaks MAC + coarse timestamp – avoid in privacy‑sensitive apps.")
    print("* Sorting v4 lexicographically ≠ chronological; consider ULID.")
    print("* Never truncate UUID to 8 chars – collision soars.")

# 9. main ---------------------------------------------------------------------


def main():
    uuid_versions_overview()
    uuid1_node_clockseq()
    uuid4_collision_demo()
    deterministic_uuid5()
    uuid_bytes_int_fields()
    uuid_from_random_or_hash()
    performance_benchmark()
    pitfalls()


if __name__ == "__main__":
    main()
