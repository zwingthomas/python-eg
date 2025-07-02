# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/pathlib.html
# Brett Cannon – "Pathlib: Filesystem Paths as First‑Class Objects"
#     https://youtu.be/T6kt7UmmjC8
# Real Python – "Python Pathlib: Object‑Oriented File System Paths"
#     https://realpython.com/python-pathlib/
# ChatGPT - model o3

"""
End‑to‑end, runnable guide to **pathlib** – object‑oriented file paths
=====================================================================
`pathlib.Path` supersedes many `os.path`, `glob`, and low‑level I/O calls with
an intuitive, chainable API.  This script is a buffet of idioms—feel free to
run it top‑to‑bottom or copy snippets.

Why pathlib over os / glob?
---------------------------
* Operator `/` overload for `join` – *no more* `os.path.join`.
* Methods return **Path** objects, so calls chain naturally.
* Cross‑platform: auto‑handles `/` vs `\`, drive letters, etc.
* Integrated with `open()`, `rglob`, `chmod`, `stat`, `touch`, `symlink`, …

Sections
--------
1.  make_demo_tree()           – build a sandbox under tmp dir
2.  creation_and_basic_ops()   – join, stem, suffix, rename, touch
3.  reading_and_writing()      – read_text, write_bytes, open as ctx mgr
4.  traversal_glob()           – iterdir, glob, rglob, matching patterns
5.  path_queries()             – exists, is_file, is_symlink, stat, resolved
6.  relative_vs_absolute()     – cwd(), home(), relative_to()
7.  symlinks_and_hardlinks()   – symlink_to, link_to
8.  permissions_and_ownership()– chmod, chown (Posix)
9.  temp_dirs_context()        – TemporaryDirectory + Path magic
10. pitfalls()                 – gotchas converting to str, performance
11. cleanup()                  – tidy sandbox
12. main()

Run directly:

```bash
python pathlib_module_tutorial.py
```
"""

from __future__ import annotations

import os
import platform
import secrets
import shutil
import stat
import tempfile
from pathlib import Path, PurePosixPath, PureWindowsPath
from pprint import pprint

BASE = Path(tempfile.gettempdir()) / (Path(__file__).stem + "_sandbox")


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# ──────────────────────────────────────────────────────────────────────────────
# 1. Build demo tree
# ──────────────────────────────────────────────────────────────────────────────


def make_demo_tree():
    if BASE.exists():
        shutil.rmtree(BASE)
    (BASE / "pkg/mod").mkdir(parents=True)
    (BASE / "pkg" / "__init__.py").touch()
    (BASE / "data.csv").write_text("id,val\n1,42\n")
    (BASE / "README.md").write_text("# Demo\n")
    (BASE / "pkg" / "mod" / "sub.txt").write_text("nested")
    print("Created sandbox at", BASE)

# ──────────────────────────────────────────────────────────────────────────────
# 2. Path creation & basic properties
# ──────────────────────────────────────────────────────────────────────────────


def creation_and_basic_ops():
    h("creation_and_basic_ops")
    p = BASE / "pkg" / "mod" / "file.py"
    print("new path →", p)
    print("parent →", p.parent)
    print("stem   →", p.stem)
    print("suffix →", p.suffix)
    p.touch()
    print("exists after touch?", p.exists())
    p.rename(p.with_suffix(".pyc"))
    print("renamed to .pyc →", p.with_suffix(".pyc"))

# ──────────────────────────────────────────────────────────────────────────────
# 3. Reading & writing helpers
# ──────────────────────────────────────────────────────────────────────────────


def reading_and_writing():
    h("reading_and_writing")
    cfg = BASE / "config.ini"
    cfg.write_text("[opts]\nsecret=" + secrets.token_hex(4))
    print("config contents →", cfg.read_text().strip())
    with cfg.open("a") as f:
        f.write("\nmore=true\n")
    print("appended line →", cfg.read_text().splitlines()[-1])

# ──────────────────────────────────────────────────────────────────────────────
# 4. Traversal & globbing
# ──────────────────────────────────────────────────────────────────────────────


def traversal_glob():
    h("traversal_glob")
    print("* immediate children →", [c.name for c in BASE.iterdir()])
    txts = list(BASE.rglob("*.txt"))
    print("*.txt recursively →", [str(t.relative_to(BASE)) for t in txts])
    md = list((BASE / "pkg").glob("*.md"))
    print("*.md under pkg →", md)

# ──────────────────────────────────────────────────────────────────────────────
# 5. Query methods
# ──────────────────────────────────────────────────────────────────────────────


def path_queries():
    h("path_queries")
    f = BASE / "data.csv"
    print("is_file?", f.is_file())
    print("size bytes →", f.stat().st_size)
    print("resolved (absolute) →", f.resolve())

# ──────────────────────────────────────────────────────────────────────────────
# 6. Relative vs absolute paths
# ──────────────────────────────────────────────────────────────────────────────


def relative_vs_absolute():
    h("relative_vs_absolute")
    print("cwd() →", Path.cwd())
    print("home() →", Path.home())
    rel = (BASE / "pkg/mod").relative_to(BASE)
    print("relative_to(BASE) →", rel)

# ──────────────────────────────────────────────────────────────────────────────
# 7. Symlinks & hard links
# ──────────────────────────────────────────────────────────────────────────────


def symlinks_and_hardlinks():
    if platform.system() == "Windows" and not os.getenv("CI"):
        # Requires admin or developer mode on Windows; skip otherwise
        return
    h("symlinks_and_hardlinks")
    target = BASE / "README.md"
    symlink = BASE / "readme_link.md"
    if not symlink.exists():
        symlink.symlink_to(target)
    print("symlink →", symlink, "→", symlink.resolve())

    hard = BASE / "data.hardcopy"
    if not hard.exists():
        try:
            # Python 3.12+: prefer hardlink_to
            hard.hardlink_to(target)
        except AttributeError:
            # <=3.11 fallback
            os.link(target, hard)
    print("hard link inode equal?", hard.stat().st_ino == target.stat().st_ino)

# ──────────────────────────────────────────────────────────────────────────────
# 8. Permissions & ownership (Posix only)
# ──────────────────────────────────────────────────────────────────────────────


def permissions_and_ownership():
    if os.name == "nt":
        return
    h("permissions_and_ownership")
    f = BASE / "secret.txt"
    f.touch()
    f.chmod(0o600)
    print("chmod 600 set; oct →", oct(f.stat().st_mode & 0o777))

# ──────────────────────────────────────────────────────────────────────────────
# 9. Temporary directories with pathlib
# ──────────────────────────────────────────────────────────────────────────────


def temp_dirs_context():
    h("temp_dirs_context")
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "temp.txt"
        p.write_text("hi")
        print("inside context exists?", p.exists())
    print("after context exists?", p.exists())

# ──────────────────────────────────────────────────────────────────────────────
# 10. Pitfalls & tips
# ──────────────────────────────────────────────────────────────────────────────


def pitfalls():
    h("pitfalls")
    print("* Converting Path to str lazily can help performance when many ops")
    print("* Watch out for Windows reserved names (COM1, NUL, …)")
    print("* PurePath vs Path → PurePath does *no* I/O; great for unit tests")
    print("  Example PurePosixPath →", PurePosixPath("/etc/passwd").parts)
    print("  Example PureWindowsPath →",
          PureWindowsPath("C:/Temp/foo.txt").drive)

# ──────────────────────────────────────────────────────────────────────────────
# 11. Cleanup
# ──────────────────────────────────────────────────────────────────────────────


def cleanup():
    shutil.rmtree(BASE)
    print("Removed sandbox", BASE)

# ──────────────────────────────────────────────────────────────────────────────
# 12. main orchestrator
# ──────────────────────────────────────────────────────────────────────────────


def main():
    make_demo_tree()
    creation_and_basic_ops()
    reading_and_writing()
    traversal_glob()
    path_queries()
    relative_vs_absolute()
    symlinks_and_hardlinks()
    permissions_and_ownership()
    temp_dirs_context()
    pitfalls()
    cleanup()


if __name__ == "__main__":
    main()
