# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/shutil.html
# Real Python – "Practical `shutil`" guide
#     https://realpython.com/shutil-copy-move-delete-files/#
# ChatGPT - model o3

"""
Hands‑on, *runnable* tour of Python’s **shutil** standard‑library module
========================================================================
`shutil` bundles high‑level file operations—copy/move/delete, directory trees,
archives, disk‑usage, even terminal progress bars.  It builds atop `os`, so you
get robust, cross‑platform helpers with far less code.

How `shutil` sits among siblings
--------------------------------
| Task                     | os            | shutil        | pathlib  |
|--------------------------|---------------|---------------|----------|
| Copy file w/ metadata    | ⚠️ many steps | ✅ `copy2`    | ❌ |
| Recursive copy dir       | manual walk   | ✅ `copytree` | ✅ (`Path.rglob` + copy) |
| Remove dir tree          | manual walk   | ✅ `rmtree`   | ❌ |
| Make/extract archive     | ❌            | ✅ `make_archive`, `unpack_archive` | ❌ |
| Disk usage               | ❌            | ✅ `disk_usage` | ❌ |

Sections
--------
1.  make_sandbox()              – build a temp tree with files & sub‑dirs
2.  simple_copy_move()          – `copy`, `copy2`, `move`, metadata notes
3.  copytree_variants()         – `dirs_exist_ok`, `ignore_patterns`, `copy_function`
4.  removing()                  – `rmtree` with onerror, `which`, `chown`
5.  archiving()                 – `make_archive`, `get_archive_formats`, `unpack_archive`
6.  disk_usage_and_terminal()   – `disk_usage`, `get_terminal_size`
7.  high_perf_copyfileobj()     – stream copy with buffer size tweak
8.  pitfalls()                  – symlink dereference, Windows readonly, large trees
9.  cleanup()
10. main()

Run directly:

```bash
python shutil_module_tutorial.py
```
"""

from __future__ import annotations

import os
import platform
import shutil
import stat
import sys
import tarfile
import tempfile
from hashlib import md5
from pathlib import Path
from pprint import pprint

BASE = Path(tempfile.gettempdir()) / (Path(__file__).stem + "_sandbox")
ARCHIVE_DIR = BASE / "archives"


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# ──────────────────────────────────────────────────────────────────────────────
# 1. Construct demo tree
# ──────────────────────────────────────────────────────────────────────────────


def make_sandbox():
    if BASE.exists():
        shutil.rmtree(BASE)
    (BASE / "src/sub").mkdir(parents=True)
    (BASE / "src/file1.txt").write_text("alpha")
    (BASE / "src/file2.txt").write_text("beta")
    (BASE / "src/sub/file3.txt").write_text("gamma")
    ARCHIVE_DIR.mkdir()
    print("Sandbox created at", BASE)

# ──────────────────────────────────────────────────────────────────────────────
# 2. Copy / move basics
# ──────────────────────────────────────────────────────────────────────────────


def simple_copy_move():
    h("simple_copy_move")
    src_file = BASE / "src/file1.txt"
    dst_file = BASE / "copy.txt"
    shutil.copy(src_file, dst_file)
    print("copy →", dst_file.read_text())

    dst_meta = BASE / "copy_meta.txt"
    shutil.copy2(src_file, dst_meta)  # preserves mtime/atime/perm
    print("copy2 mtime preserved?", src_file.stat(
    ).st_mtime == dst_meta.stat().st_mtime)

    moved = BASE / "moved.txt"
    shutil.move(dst_file, moved)
    print("moved exists?", moved.exists(),
          "original missing?", not dst_file.exists())

# ──────────────────────────────────────────────────────────────────────────────
# 3. copytree variants
# ──────────────────────────────────────────────────────────────────────────────


def copytree_variants():
    h("copytree_variants")
    dest = BASE / "dest_tree"
    shutil.copytree(BASE / "src", dest)
    print("standard copytree files →", [p.name for p in dest.rglob("*.txt")])

    # dirs_exist_ok=True (3.8+) allows merge‑style copy
    shutil.copytree(BASE / "src", dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("*2.txt"))
    print("after second copy (ignored *2.txt) →",
          [p.name for p in dest.rglob("*.txt")])

# ──────────────────────────────────────────────────────────────────────────────
# 4. Removing and utility helpers
# ──────────────────────────────────────────────────────────────────────────────


def removing():
    h("removing")
    # work inside a *sub* directory so we don't delete the whole sandbox
    trash_dir = BASE / "to_delete"
    trash_dir.mkdir(exist_ok=True)
    trash = trash_dir / "trash.txt"
    trash.write_text("bye")
    os.chmod(trash, stat.S_IREAD)  # make read‑only

    def on_rm_error(func, path, exc):
        print("onerror → chmod + retry", path)
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(trash_dir, onerror=on_rm_error)
    print("trash_dir removed?", not trash_dir.exists())

    print("which('python') →", shutil.which("python"))
    if hasattr(shutil, "chown") and os.name != "nt":
        print("chown available (not executed) →", shutil.chown)

# ──────────────────────────────────────────────────────────────────────────────
# 5. Archiving helpers
# ──────────────────────────────────────────────────────────────────────────────


def archiving():
    h("archiving")
    archive_path = shutil.make_archive(
        str(ARCHIVE_DIR / "src_backup"), "zip", BASE / "src")
    print("made archive →", archive_path)

    print("available formats →", shutil.get_archive_formats())
    extract_dir = ARCHIVE_DIR / "extracted"
    shutil.unpack_archive(archive_path, extract_dir)
    print("extracted names →", [p.name for p in extract_dir.rglob("*.txt")])

# ──────────────────────────────────────────────────────────────────────────────
# 6. Disk usage & terminal size
# ──────────────────────────────────────────────────────────────────────────────


def disk_usage_and_terminal():
    h("disk_usage_and_terminal")
    usage = shutil.disk_usage("/")
    print("disk free GiB →", round(usage.free / 1024 ** 3, 2))
    cols, rows = shutil.get_terminal_size((80, 24))
    print("terminal size fallback 80×24 →", cols, rows)

# ──────────────────────────────────────────────────────────────────────────────
# 7. copyfileobj for streaming
# ──────────────────────────────────────────────────────────────────────────────


def high_perf_copyfileobj():
    h("high_perf_copyfileobj")
    src = BASE / "src/file2.txt"
    dst = BASE / "file2_copy.bin"
    with src.open("rb") as fsrc, dst.open("wb") as fdst:
        shutil.copyfileobj(fsrc, fdst, length=8)  # small buf for demo
    print("MD5 equal?", md5(src.read_bytes()).digest()
          == md5(dst.read_bytes()).digest())

# ──────────────────────────────────────────────────────────────────────────────
# 8. Pitfalls
# ──────────────────────────────────────────────────────────────────────────────


def pitfalls():
    h("pitfalls")
    print("* copytree duplicates *contents*; attrs of root dir not copied unless copystat() done later")
    print("* symlinks are dereferenced by default – use symlinks=True to copy links themselves")
    print("* On Windows, read‑only files make rmtree fail unless onerror handler fixes perms")
    print("* Large trees: copytree uses linear recursion → long paths may hit MAX_PATH on Win <3.6")

# ──────────────────────────────────────────────────────────────────────────────
# 9. Cleanup
# ──────────────────────────────────────────────────────────────────────────────


def cleanup():
    shutil.rmtree(BASE)
    print("Removed sandbox", BASE)

# ──────────────────────────────────────────────────────────────────────────────
# 10. main orchestrator
# ──────────────────────────────────────────────────────────────────────────────


def main():
    make_sandbox()
    simple_copy_move()
    copytree_variants()
    archiving()
    removing()  # now safe after archive step
    disk_usage_and_terminal()
    high_perf_copyfileobj()
    pitfalls()
    cleanup()


if __name__ == "__main__":
    main()
