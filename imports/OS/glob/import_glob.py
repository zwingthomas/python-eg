# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/glob.html
# pathlib docs (Path.glob)
#     https://docs.python.org/3/library/pathlib.html
# ChatGPT - model o3
"""
Practical tour of Python’s **glob** module (and `Path.glob`)
===========================================================
`glob` provides Unix‑style pathname expansion—`*.py`, `foo/**/bar*.txt`, etc.
It’s a concise way to find groups of files without writing manual directory
walks.

Key differences vs `os.listdir()` / `os.walk()`
----------------------------------------------
* **Pattern matching** – wildcards interpreted for you.
* **Recursive `**`** – one call replaces a nested `os.walk()` loop.
* **Sorted output**   – results are returned in lexicographic order.
* **Shell‑like but not exactly** – character classes `[abc]` supported; brace
  expansion `{a,b}` is **not**.

Sections
--------
1.  setup_demo_tree()          – create sample files in tmp dir
2.  basic_patterns()           – `*.py`, `data?.csv`
3.  recursive_glob()           – `**/*.txt`, `recursive=True`
4.  character_class()          – `[0-9]` ranges, negation `[!ab]`
5.  dotfiles_and_case()        – hidden files & `casefold`
6.  pathlib_equivalent()       – `Path('dir').rglob('*.md')`
7.  cleanup()
8.  main()

Run directly:

```bash
python glob_module_tutorial.py
```
"""

from __future__ import annotations

import glob
import shutil
import sys
from pathlib import Path
from pprint import pprint

BASE = Path(__file__).with_suffix("").with_name(Path(__file__).stem + "_tmp")

# ──────────────────────────────────────────────────────────────────────────────
# 0. Helper
# ──────────────────────────────────────────────────────────────────────────────


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# ──────────────────────────────────────────────────────────────────────────────
# 1. Create a sample directory tree
# ──────────────────────────────────────────────────────────────────────────────


def setup_demo_tree():
    if BASE.exists():
        shutil.rmtree(BASE)
    (BASE / "sub1/sub2").mkdir(parents=True)
    (BASE / "sub1").mkdir(exist_ok=True)

    files = [
        "main.py",
        "script.sh",
        "data1.csv",
        "data2.csv",
        "notes.txt",
        "sub1/readme.md",
        "sub1/image.png",
        "sub1/sub2/log_01.txt",
        "sub1/sub2/log_02.txt",
        ".hidden",
    ]
    for f in files:
        (BASE / f).write_text(f"demo {f}")
    print("Created demo tree at", BASE)

# ──────────────────────────────────────────────────────────────────────────────
# 2. Simple patterns
# ──────────────────────────────────────────────────────────────────────────────


def basic_patterns():
    h("basic_patterns")
    print("*.py →", glob.glob(str(BASE / "*.py")))
    print("data?.csv →", glob.glob(str(BASE / "data?.csv")))

# ──────────────────────────────────────────────────────────────────────────────
# 3. Recursive glob with **
# ──────────────────────────────────────────────────────────────────────────────


def recursive_glob():
    h("recursive_glob")
    txts = glob.glob(str(BASE / "**/*.txt"), recursive=True)
    pprint(txts)

# ──────────────────────────────────────────────────────────────────────────────
# 4. Character classes & negation
# ──────────────────────────────────────────────────────────────────────────────


def character_class():
    h("character_class")
    logs = glob.glob(str(BASE / "sub1/sub2/log_[0-1][0-9].txt"))
    print("log_[0-1][0-9].txt →", logs)
    not_csv = glob.glob(str(BASE / "*.[!c][!s][!v]"))
    print("files not ending csv →", not_csv)

# ──────────────────────────────────────────────────────────────────────────────
# 5. Dot‑files & case sensitivity
# ──────────────────────────────────────────────────────────────────────────────


def dotfiles_and_case():
    h("dotfiles_and_case")
    print("default ignores dotfiles →", glob.glob(str(BASE / "*")))
    print("explicit .* pattern →", glob.glob(str(BASE / ".*")))

    try:
        ci = glob.glob(str(BASE / "*.CSV"),
                       case_sensitive=False)  # Python ≥3.11
    except TypeError:
        ci = "(case_sensitive flag unsupported on this Python)"
    print("case‑insensitive flag →", ci)

# ──────────────────────────────────────────────────────────────────────────────
# 6. Pathlib equivalent API
# ──────────────────────────────────────────────────────────────────────────────


def pathlib_equivalent():
    h("pathlib_equivalent")
    md_files = list((BASE / "sub1").rglob("*.md"))
    pprint([str(p) for p in md_files])

# ──────────────────────────────────────────────────────────────────────────────
# 7. Cleanup helper
# ──────────────────────────────────────────────────────────────────────────────


def cleanup():
    shutil.rmtree(BASE)
    print("Removed demo tree", BASE)

# ──────────────────────────────────────────────────────────────────────────────
# 8. main
# ──────────────────────────────────────────────────────────────────────────────


def main():
    setup_demo_tree()
    basic_patterns()
    recursive_glob()
    character_class()
    dotfiles_and_case()
    pathlib_equivalent()
    cleanup()


if __name__ == "__main__":
    main()
