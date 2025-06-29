# Acknowledgements____
# Official docs
#     https://docs.python.org/3/library/json.html
# Real-Python Guide
#     https://realpython.com/python-json/
# ChatGPT - Model o3

"""
Deep-dive into Python's built-in **json** module
================================================
This script is structured as a series of bite-sized, runnable demos that cover
almost everything the standard `json` module can do out-of-the-box.

Sections
--------
1. quick_demo()              - 30-second overview of dumps/loads
2. file_read_write()         - pretty-printing, separators, ensure_ascii
3. dict_order_sorting()      - stable key order & `sort_keys`
4. custom_types()            - serialising `datetime`, `Decimal`, custom class
5. custom_deserialise()      - `object_hook` & `object_pairs_hook`
6. stream_parse_large_file() - incremental reading with `json.load` + `ijson` hint
7. dataclass_helper()        - dumping dataclasses via `asdict`
8. main()                    - run all demos then clean tmp dir

Run the file directly: `python json_module_tutorial.py`
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from collections import OrderedDict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from pprint import pprint
from typing import Any

TMP_DIR = Path(tempfile.gettempdir()) / (Path(__file__).stem + "_tmp")
TMP_DIR.mkdir(exist_ok=True)


# ─────────────────────────────────────────────────────────────────────-
# Helper
# ──────────────────────────────────────────────────────────────────────

def _tmpfile(name: str) -> Path:  # guarantee unique test files
    return TMP_DIR / name


# ──────────────────────────────────────────────────────────────────────
# 1. Quick taste – dumps & loads strings
# ──────────────────────────────────────────────────────────────────────

def quick_demo() -> None:
    print("\n[ quick_demo ]\n" + "-" * 60)
    data = {"name": "Ada", "active": True, "score": 98.5}

    json_str = json.dumps(data)  # dict → JSON string
    print("JSON text:", json_str)

    back = json.loads(json_str)  # JSON string → Python object
    print("Back to Python:", back)


# ──────────────────────────────────────────────────────────────────────
# 2. File I/O, pretty printing, ascii vs UTF-8
# ──────────────────────────────────────────────────────────────────────

def file_read_write() -> None:
    print("\n[ file_read_write ]\n" + "-" * 60)

    cities = [
        {"city": "Zürich", "pop": 402762, "country": "Switzerland"},
        {"city": "São Paulo", "pop": 12330000, "country": "Brazil"},
        {"city": "Tokyo", "pop": 13929286, "country": "Japan"},
    ]

    path = _tmpfile("cities.json")
    with path.open("w", encoding="utf-8") as f:
        json.dump(
            cities,
            f,
            indent=2,               # pretty print with two-space indent
            ensure_ascii=False,     # keep the UTF-8 characters readable
            separators=(",", ": "),  # compact but still pretty
        )
    print("Wrote", path)

    # Reading back
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    pprint(data)


# ──────────────────────────────────────────────────────────────────────
# 3. Dict ordering & sort_keys
# ──────────────────────────────────────────────────────────────────────

def dict_order_sorting() -> None:
    print("\n[ dict_order_sorting ]\n" + "-" * 60)

    record = OrderedDict([("b", 2), ("a", 1), ("c", 3)])
    print("Original order preserved →", json.dumps(record))
    print("Sorted keys            →", json.dumps(record, sort_keys=True))


# ──────────────────────────────────────────────────────────────────────
# 4. Serialising non-built-ins via default=
# ──────────────────────────────────────────────────────────────────────

def custom_types() -> None:
    print("\n[ custom_types ]\n" + "-" * 60)

    @dataclass
    class Invoice:
        id: int
        total: Decimal
        issued: datetime

    inv = Invoice(id=42, total=Decimal("199.99"),
                  issued=datetime.now(timezone.utc))

    def encode_special(obj: Any):
        if isinstance(obj, Decimal):
            return {"__decimal__": str(obj)}  # tag to recover later
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Invoice):
            return {"__invoice__": asdict(obj)}
        raise TypeError(f"Type not serialisable: {type(obj).__name__}")

    js = json.dumps(inv, default=encode_special, indent=2)
    print(js)


# ──────────────────────────────────────────────────────────────────────
# 5. Custom deserialise with object_hook / object_pairs_hook
# ──────────────────────────────────────────────────────────────────────

def custom_deserialise() -> None:
    print("\n[ custom_deserialise ]\n" + "-" * 60)

    sample = {
        "when": datetime.now(timezone.utc).isoformat(),
        "price": {"__decimal__": "12.34"},
    }
    js = json.dumps(sample)

    def hook(obj: dict[str, Any]):
        if "__decimal__" in obj:
            return Decimal(obj["__decimal__"])
        if "when" in obj:
            obj["when"] = datetime.fromisoformat(obj["when"])
        return obj

    back = json.loads(js, object_hook=hook)
    pprint(back)


# ──────────────────────────────────────────────────────────────────────
# 6. Streaming/incremental parse (constant memory)
# ──────────────────────────────────────────────────────────────────────

def stream_parse_large_file() -> None:
    """Generate a ~5 MB JSON array on the fly, then stream-parse first 3 items."""
    print("\n[ stream_parse_large_file ]\n" + "-" * 60)

    path = _tmpfile("big.json")
    with path.open("w", encoding="utf-8") as f:
        f.write("[")
        for i in range(1_000_000):
            json.dump({"n": i}, f, separators=(",", ":"))
            f.write("," if i < 999_999 else "]")

    print("Generated large file (~", round(
        path.stat().st_size / 1024 / 1024, 2), "MB)")

    # Built-in json.load reads the whole file, so for truly huge files use ijson.
    # Here we show how to peek at the first few items using simple slicing.
    import itertools
    with path.open(encoding="utf-8") as f:
        all_items = json.load(f)          # demo only – loads entire array
        for item in itertools.islice(all_items, 3):
            print(item)
    print("(Use the third-party 'ijson' library for genuine streaming.)")


# ──────────────────────────────────────────────────────────────────────
# 7. Dataclass helper – dumping complex objects quickly
# ──────────────────────────────────────────────────────────────────────

def dataclass_helper() -> None:
    print("\n[ dataclass_helper ]\n" + "-" * 60)

    @dataclass
    class User:
        id: int
        name: str
        roles: list[str]
        created: datetime = datetime.utcnow()

    u = User(1, "Grace", ["admin", "editor"])
    json_str = json.dumps(asdict(u), indent=2, default=str)
    print(json_str)


# ──────────────────────────────────────────────────────────────────────
# 8. main – run everything then tidy up
# ──────────────────────────────────────────────────────────────────────

def main() -> None:
    quick_demo()
    file_read_write()
    dict_order_sorting()
    custom_types()
    custom_deserialise()
    stream_parse_large_file()
    dataclass_helper()

    # Cleanup temp artefacts
    for p in TMP_DIR.iterdir():
        p.unlink()
    TMP_DIR.rmdir()
    print("\nTemporary files cleaned – done!")


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)  # just in case
    main()
