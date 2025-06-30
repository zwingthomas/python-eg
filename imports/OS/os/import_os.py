# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/os.html
# Advanced uses – Real Python
#     https://realpython.com/python-os-module/
# ChatGPT - model o3
"""
Comprehensive, runnable tour of Python’s **os** standard‑library module
======================================================================
`os` is the Swiss‑army knife for *operating‑system* interfaces: environment
variables, process management, files, permissions, and more.  This script is
split into focused demos you can run top‑to‑bottom or cherry‑pick.

Where `os` sits relative to other std‑lib modules
------------------------------------------------
| Task                         | os            | pathlib     | subprocess | shutil  |
|------------------------------|---------------|-------------|------------|---------|
| Path string ops              | ✅ (`os.path`) | ✅ OO       | ❌         | ❌ |
| High‑level file operations   | ⚠️ basic (`remove`, `rename`) | ✅ (`Path.unlink`) | ❌ | ✅ (`shutil.rmtree`) |
| Walking directory tree       | ✅ (`os.walk`) | ✅ (`Path.rglob`) | ❌ | ❌ |
| Process spawn/exec           | ✅ (`spawn*`, `fork/exec`) | ❌ | ✅ | ❌ |
| Environment variables        | ✅            | ❌          | inherit    | ❌ |
| Signals / pids               | ✅ (`kill`)   | ❌          | ❌         | ❌ |

Sections
--------
1.  env_vars()                 – read/set, default fallback
2.  path_ops()                 – join, split, normpath, realpath
3.  dir_walk_vs_pathlib()      – `os.walk` vs `Path.rglob`
4.  permissions_and_stat()     – chmod, stat, octal masks
5.  process_spawn_exec()       – spawn* vs `subprocess.run`
6.  fork_and_pipe()            – Unix‑only demo w/ IPC
7.  signals_demo()             – send SIGTERM to a child
8.  random_bytes()             – `os.urandom` vs `secrets`
9.  temp_dirs_files()          – `mkdtemp`, NamedTemporaryFile comparison
10. pitfalls()                 – cross‑platform path sep, inherited fds…
11. cleanup()
12. main()

Run directly:

```bash
python os_module_tutorial.py
```
"""

from __future__ import annotations

import os
import platform
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from pprint import pprint

BASE = Path(__file__).with_suffix("").with_name(Path(__file__).stem + "_tmp")
BASE.mkdir(exist_ok=True)


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# ──────────────────────────────────────────────────────────────────────────────
# 1. Environment variables
# ──────────────────────────────────────────────────────────────────────────────


def env_vars():
    h("env_vars")
    print("HOME →", os.getenv("HOME"))
    print("FOO (unset) with fallback →", os.getenv("FOO", "default"))
    os.environ["DEMO_VAR"] = "123"
    print("DEMO_VAR just set →", os.environ.get("DEMO_VAR"))

# ──────────────────────────────────────────────────────────────────────────────
# 2. Path operations (`os.path`)
# ──────────────────────────────────────────────────────────────────────────────


def path_ops():
    h("path_ops")
    sample = BASE / "../foo//bar/../baz.txt"
    print("join →", os.path.join("a", "b", "c.txt"))
    print("normpath →", os.path.normpath(sample))
    print("abspath  →", os.path.abspath("./"))
    print("splitext →", os.path.splitext("archive.tar.gz"))

# ──────────────────────────────────────────────────────────────────────────────
# 3. Directory walk vs pathlib
# ──────────────────────────────────────────────────────────────────────────────


def dir_walk_vs_pathlib():
    h("dir_walk_vs_pathlib")
    # build tiny tree
    (BASE / "d1/d2").mkdir(parents=True, exist_ok=True)
    for p in [BASE / "a.txt", BASE / "d1/b.txt", BASE / "d1/d2/c.md"]:
        p.write_text("demo")

    txts = [os.path.join(root, f) for root, _, files in os.walk(BASE)
            for f in files if f.endswith(".txt")]
    print("os.walk txts →", txts)

    md = list((BASE).rglob("*.md"))
    print("Path.rglob('*.md') →", [str(p) for p in md])

# ──────────────────────────────────────────────────────────────────────────────
# 4. Permissions & stat
# ──────────────────────────────────────────────────────────────────────────────


def permissions_and_stat():
    h("permissions_and_stat")
    f = BASE / "perm_demo.txt"
    f.write_text("hi")
    os.chmod(f, 0o640)  # rw-r-----
    st = os.stat(f)
    print("mode octal →", oct(st.st_mode & 0o777))
    print("size bytes →", st.st_size)

# ──────────────────────────────────────────────────────────────────────────────
# 5. Spawn vs subprocess
# ──────────────────────────────────────────────────────────────────────────────


def process_spawn_exec():
    h("process_spawn_exec")
    if platform.system() == "Windows":
        print("spawn demo skipped on Windows (uses /bin/echo)")
        return
    pid = os.spawnlp(os.P_WAIT, "echo", "echo", "hello spawn")
    print("spawn returned exit status", pid)
    cp = subprocess.run(["echo", "hello subprocess"],
                        capture_output=True, text=True)
    print("subprocess output →", cp.stdout.strip())

# ──────────────────────────────────────────────────────────────────────────────
# 6. fork + pipe (Unix‑only)
# ──────────────────────────────────────────────────────────────────────────────


def fork_and_pipe():
    if os.name == "nt":
        return
    h("fork_and_pipe")
    rfd, wfd = os.pipe()
    pid = os.fork()
    if pid == 0:  # child
        os.close(rfd)
        os.write(wfd, b"fork hello")
        os._exit(0)
    else:
        os.close(wfd)
        msg = os.read(rfd, 128)
        os.waitpid(pid, 0)
        print("parent got →", msg)

# ──────────────────────────────────────────────────────────────────────────────
# 7. Signal demo – send SIGTERM to child
# ──────────────────────────────────────────────────────────────────────────────


def signals_demo():
    if os.name == "nt":
        return
    h("signals_demo")
    pid = os.fork()
    if pid == 0:
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
        while True:
            time.sleep(1)
    else:
        time.sleep(0.5)
        os.kill(pid, signal.SIGTERM)
        _, status = os.waitpid(pid, 0)
        print("child exit status →", status)

# ──────────────────────────────────────────────────────────────────────────────
# 8. Secure random bytes
# ──────────────────────────────────────────────────────────────────────────────


def random_bytes():
    h("random_bytes")
    print("os.urandom 16 →", os.urandom(16).hex())
    print("secrets.token_hex(16) →", secrets.token_hex(16))

# ──────────────────────────────────────────────────────────────────────────────
# 9. Temporary dirs & files
# ──────────────────────────────────────────────────────────────────────────────


def temp_dirs_files():
    h("temp_dirs_files")
    tmpd = tempfile.mkdtemp()
    print("mkdtemp →", tmpd)
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(b"tmp")
        print("NamedTemporaryFile →", tf.name)
    shutil.rmtree(tmpd)
    os.remove(tf.name)

# ──────────────────────────────────────────────────────────────────────────────
# 10. Common pitfalls quick‑fire
# ──────────────────────────────────────────────────────────────────────────────


def pitfalls():
    h("pitfalls")
    print("* Never concatenate paths with '+' – use os.path.join")
    print("* Windows vs Posix path separators – prefer pathlib for portability")
    print("* Remember to close/cleanup temp files or they linger")
    print("* Child inherits env & fds; use close_fds=True in subprocess on Unix <3.9")

# ──────────────────────────────────────────────────────────────────────────────
# 11. Cleanup
# ──────────────────────────────────────────────────────────────────────────────


def cleanup():
    shutil.rmtree(BASE)
    print("Removed", BASE)

# ──────────────────────────────────────────────────────────────────────────────
# 12. main
# ──────────────────────────────────────────────────────────────────────────────


def main():
    env_vars()
    path_ops()
    dir_walk_vs_pathlib()
    permissions_and_stat()
    process_spawn_exec()
    fork_and_pipe()
    signals_demo()
    random_bytes()
    temp_dirs_files()
    pitfalls()
    cleanup()


if __name__ == "__main__":
    main()
