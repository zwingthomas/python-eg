# Acknowledgements____
# Official docs
#     https://docs.python.org/3/library/pickle.html
# pickletools (disassembler)
#     https://docs.python.org/3/library/pickletools.html
# Real-Python guide
#     https://realpython.com/python-pickle/
# ChatGPT - model o3

"""
Comprehensive tour of Python’s **pickle** module
================================================
This script demonstrates the most common—and a few advanced—features of
`pickle`, along with **clear warnings** about its security pitfalls.

⚠️  **Never unpickle data you didn’t create yourself**.  A crafted pickle can
execute arbitrary code when it’s deserialised.

Sections
--------
1.  quick_demo()              – bytes round-trip without touching disk
2.  file_pickle_unpickle()    – save/load to a file, highest protocol
3.  protocol_sizes()          – size & speed across protocols 0…7
4.  custom_state()            – `__getstate__` & `__setstate__`
5.  copyreg_lambda()          – serialising a module‑level lambda with `copyreg`
6.  deep_copy_with_pickle()   – pickle as a cheap deep-copy hack
7.  peek_inside()             – disassemble protocol 0 stream with `pickletools`
8.  main()                    – run demos & clean up tmp files

Run it directly:

```bash
python pickle_module_tutorial.py
```
"""

from __future__ import annotations
import copyreg  # after adder so the reducer sees it

import datetime as _dt
import marshal
import pickle
import pickletools
import sys
import tempfile
import time
import types
from pathlib import Path
from typing import Any

TMP_DIR = Path(tempfile.gettempdir()) / (Path(__file__).stem + "_tmp")
TMP_DIR.mkdir(exist_ok=True)


def _tmpfile(name: str) -> Path:
    return TMP_DIR / name

# ──────────────────────────────────────────────────────────────────────────────
# Helper class used across demos (must be module-level for pickling)
# ──────────────────────────────────────────────────────────────────────────────


class Cache:
    """Pretend this hits a DB; we don’t want the connection in the pickle."""

    def __init__(self, url: str):
        self.url = url
        self._conn = f"<connected {url}>"  # non-picklable handle
        self._hits = 0

    def lookup(self, key: str) -> str:
        self._hits += 1
        return f"value_for_{key}"

    # — pickling hooks ————————————————————————————
    def __getstate__(self):
        state = self.__dict__.copy()
        state["_conn"] = None  # drop live connection
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # lazily recreate connection
        self._conn = f"<reconnected {self.url}>"

# ──────────────────────────────────────────────────────────────────────────────
# Module‑level lambda + copyreg helper so it *is* picklable (demo only!)
# ──────────────────────────────────────────────────────────────────────────────


def adder(x, y): return x + y  # noqa: E731  – must live at module scope


def _reduce_lambda(func: types.FunctionType):
    """Serialize a lambda by marshaling its bytecode.  ⚠️  Demo‑only, unsafe."""
    code_bytes = marshal.dumps(func.__code__)
    return _rebuild_lambda, (code_bytes,)


def _rebuild_lambda(code_bytes: bytes):
    code = marshal.loads(code_bytes)
    return types.FunctionType(code, globals())


# Register reducer for *all* function objects – good enough for demo
copyreg.pickle(types.FunctionType, _reduce_lambda)

# ──────────────────────────────────────────────────────────────────────────────
# 1. quick demo – immediate round‑trip
# ──────────────────────────────────────────────────────────────────────────────


def quick_demo() -> None:
    print("\n[ quick_demo ]\n" + "-" * 60)
    data = {"now": _dt.datetime.now(), "nums": list(range(5)),
            "greeting": "hi"}

    blob = pickle.dumps(data)              # object → bytes
    print("Pickle size:", len(blob), "bytes")

    back = pickle.loads(blob)              # bytes → object
    print("Round-tripped equal?", back == data)

# ──────────────────────────────────────────────────────────────────────────────
# 2. Pickle to / from a file with highest protocol
# ──────────────────────────────────────────────────────────────────────────────


def file_pickle_unpickle() -> None:
    print("\n[ file_pickle_unpickle ]\n" + "-" * 60)
    inventory = [
        {"sku": 101, "name": "widget", "price": 9.99},
        {"sku": 102, "name": "gadget", "price": 14.99},
    ]

    path = _tmpfile("inventory.pkl")
    with path.open("wb") as f:
        pickle.dump(inventory, f, protocol=pickle.HIGHEST_PROTOCOL)
    print("Wrote", path)

    with path.open("rb") as f:
        loaded = pickle.load(f)
    print("Loaded == original?", loaded == inventory)

# ──────────────────────────────────────────────────────────────────────────────
# 3. Protocol comparison – size & timing
# ──────────────────────────────────────────────────────────────────────────────


def protocol_sizes() -> None:
    print("\n[ protocol_sizes ]\n" + "-" * 60)
    sample = {"numbers": list(range(10_000)), "msg": "benchmark"}

    fastest: int | None = None
    fastest_time: float = float("inf")
    for proto in range(pickle.HIGHEST_PROTOCOL + 1):
        start = time.perf_counter()
        blob = pickle.dumps(sample, protocol=proto)
        elapsed = (time.perf_counter() - start) * 1e3  # ms
        print(f"proto {proto}: {len(blob)/1024:.1f} KiB, {elapsed:.2f} ms")
        if elapsed < fastest_time:
            fastest_time = elapsed
            fastest = proto
    print("Fastest observed → protocol", fastest)

# ──────────────────────────────────────────────────────────────────────────────
# 4. Customising with __getstate__ / __setstate__
# ──────────────────────────────────────────────────────────────────────────────


def custom_state() -> None:
    print("\n[ custom_state ]\n" + "-" * 60)

    c = Cache("redis://localhost")
    c.lookup("answer")  # bump hits to 1

    blob = pickle.dumps(c)
    resurrected: Cache = pickle.loads(blob)
    print("Hits after restore:", resurrected._hits)
    print("Connection after restore:", resurrected._conn)

# ──────────────────────────────────────────────────────────────────────────────
# 5. copyreg_lambda – pickling the module‑level lambda
# ──────────────────────────────────────────────────────────────────────────────


def copyreg_lambda() -> None:
    print("\n[ copyreg_lambda ]\n" + "-" * 60)

    try:
        restored = pickle.loads(pickle.dumps(adder))
        print("adder(2, 3) ->", restored(2, 3))
    except Exception as exc:
        print("Lambda pickling failed:", exc)

# ──────────────────────────────────────────────────────────────────────────────
# 6. Deep copy via pickle
# ──────────────────────────────────────────────────────────────────────────────


def deep_copy_with_pickle() -> None:
    print("\n[ deep_copy_with_pickle ]\n" + "-" * 60)
    orig = {"a": [1, 2, 3], "b": {"x": 9}}
    clone = pickle.loads(pickle.dumps(orig))
    clone["a"].append(4)
    print("Original →", orig)
    print("Clone    →", clone)

# ──────────────────────────────────────────────────────────────────────────────
# 7. Inspect pickle opcodes with pickletools.dis
# ──────────────────────────────────────────────────────────────────────────────


def peek_inside() -> None:
    print("\n[ peek_inside ]\n" + "-" * 60)

    obj = {"pi": 3.14159, "ts": _dt.datetime(2025, 1, 1)}
    blob = pickle.dumps(obj, protocol=0)  # protocol 0 = printable ASCII subset

    print("Raw pickle bytes →", blob.decode("latin-1"))
    print("\nDisassembly:")
    pickletools.dis(blob)

# ──────────────────────────────────────────────────────────────────────────────
# 8. main & cleanup
# ──────────────────────────────────────────────────────────────────────────────


def main() -> None:
    quick_demo()
    file_pickle_unpickle()
    protocol_sizes()
    custom_state()
    copyreg_lambda()
    deep_copy_with_pickle()
    peek_inside()

    for p in TMP_DIR.iterdir():
        p.unlink()
    TMP_DIR.rmdir()
    print("\nTemporary files removed – done!")


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    main()
