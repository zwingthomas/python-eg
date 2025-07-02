# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/sys.html
# Ned Batchelder – "Inside the CPython Interpreter"
#     https://youtu.be/uTBqKdi3PUE
# ChatGPT - model o3

"""
Ultra-comprehensive, executable tour of Python’s **sys** module
==============================================================
Expands on the previous version with *import hooks, profiling, tracing, async
hooks, GIL tuning,* and platform-specific nuggets.  Feel free to skim—each
section is self-contained.

Sections (new / updated ★)
--------------------------
1.  argv_demo()                    – argv, executable
2.  exit_and_excepthook()          – custom excepthook, thread_excepthook ★
3.  path_import_control()          – mutate sys.path, meta_path finder ★
4.  stdout_stderr_swap()           – redirect prints
5.  recursion_and_sizeof()         – recursionlimit, int_max_str_digits ★
6.  modules_cache()                – live module patching
7.  refcount_and_getallocatedblocks() ★ – memory insight (CPython)
8.  gil_switch_interval() ★        – get/set switch interval
9.  profiler_and_tracer() ★        – sys.setprofile / sys.settrace
10. asyncgen_hooks() ★             – GC for async generators
11. dlopenflags_demo() ★           – control RTLD flags (Posix)
12. platform_runtime_info()        – extended
13. introspection_getframe()       – call-stack peek
14. pitfalls()                     – extended caveats
15. main()

Run with:
```bash
python sys_module_tutorial.py arg1 arg2
```
"""

from __future__ import annotations

import builtins
import importlib.abc
import importlib.machinery
import io
import os
import sys
import textwrap
import types
from pprint import pprint
from types import FrameType, ModuleType


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# 1. argv ---------------------------------------------------------------------


def argv_demo():
    h("argv_demo")
    print("argv →", sys.argv)
    print("executable →", sys.executable)

# 2. exit / excepthook --------------------------------------------------------


def exit_and_excepthook():
    h("exit_and_excepthook")

    def hook(exc_type, exc, tb):
        print("custom excepthook:", exc_type.__name__, exc)
    old = sys.excepthook
    sys.excepthook = hook
    try:
        try:
            raise RuntimeError("boom")
        except RuntimeError:
            sys.excepthook(*sys.exc_info())
    finally:
        sys.excepthook = old

    if hasattr(sys, "threading_excepthook"):
        def th_hook(args):
            print("threading_excepthook caught:", args.exc_type.__name__)
        sys.threading_excepthook = th_hook
        import threading

        def bad():
            raise ValueError("thread fail")
        t = threading.Thread(target=bad)
        t.start()
        t.join()

# 3. Import path & custom finder ---------------------------------------------


def path_import_control():
    h("path_import_control")
    sys.path.insert(0, "/tmp/fake")
    print("path[0] →", sys.path[0])

    class NullFinder(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path, target=None):
            if fullname == "blockme":
                raise ImportError("blocked by NullFinder")
    sys.meta_path.insert(0, NullFinder())
    try:
        import blockme  # noqa: F401
    except ImportError as e:
        print(e)
    finally:
        sys.meta_path.pop(0)

# 4. stdout redirection -------------------------------------------------------


def stdout_stderr_swap():
    h("stdout_stderr_swap")
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    print("captured")
    sys.stdout = old
    print("buffer →", buf.getvalue().strip())

# 5. Recursion & int digit limit ---------------------------------------------


def recursion_and_sizeof():
    h("recursion_and_sizeof")
    print("recursionlimit →", sys.getrecursionlimit())
    sys.setrecursionlimit(1500)
    print("new limit →", sys.getrecursionlimit())
    if hasattr(sys, "set_int_max_str_digits"):
        cur = sys.get_int_max_str_digits()
        print("int_max_str_digits →", cur)
        sys.set_int_max_str_digits(cur + 100)
        print("raised to", sys.get_int_max_str_digits())

# 6. Modules cache ------------------------------------------------------------


def modules_cache():
    h("modules_cache")
    import math
    sys.modules["math"].tau = 6.28318
    print("math.tau injected →", math.tau)

# 7. CPython refcount & allocated blocks -------------------------------------


def refcount_and_getallocatedblocks():
    if not hasattr(sys, "getrefcount"):
        return
    h("refcount_and_getallocatedblocks")
    obj = []
    print("refcount →", sys.getrefcount(obj))
    if hasattr(sys, "getallocatedblocks"):
        print("allocated blocks →", sys.getallocatedblocks())

# 8. GIL switch interval ------------------------------------------------------


def gil_switch_interval():
    h("gil_switch_interval")
    print("switch interval →", sys.getswitchinterval())
    sys.setswitchinterval(0.005)
    print("new interval 5ms set")

# 9. Profiling & tracing ------------------------------------------------------


def profiler_and_tracer():
    h("profiler_and_tracer")
    events = []

    def profiler(frame, event, arg):
        if event == "call":
            events.append(frame.f_code.co_name)
    sys.setprofile(profiler)

    def foo():
        return 1
    foo()
    sys.setprofile(None)
    print("functions hit →", events)

    def tracer(frame, event, arg):
        if event == "line":
            print("trace line", frame.f_lineno)
        return tracer
    sys.settrace(tracer)
    x = 1
    x += 1  # will trigger trace
    sys.settrace(None)

# 10. Async-gen lifecycle hooks ---------------------------------------------


def asyncgen_hooks():
    h("asyncgen_hooks")

    async def agen():
        yield 1

    async def finalize(agen):
        print("closing asyncgen")
    sys.set_asyncgen_hooks(finalizer=finalize)
    a = agen()
    a.aclose()

# 11. dlopen flags (Posix) ----------------------------------------------------


def dlopenflags_demo():
    if os.name != "posix":
        return
    h("dlopenflags_demo")
    flags = sys.getdlopenflags()
    print("orig flags →", flags)
    sys.setdlopenflags(flags | os.RTLD_GLOBAL)
    print("flags now →", sys.getdlopenflags())
    sys.setdlopenflags(flags)

# 12. Platform info -----------------------------------------------------------


def platform_runtime_info():
    h("platform_runtime_info")
    print("version →", sys.version)
    print("implementation →", sys.implementation.name, sys.implementation.version)
    print("float info mant_dig →", sys.float_info.mant_dig)

# 13. Frame introspection -----------------------------------------------------


def introspection_getframe():
    h("introspection_getframe")

    def inner():
        frm: FrameType = sys._getframe()
        print("func", frm.f_code.co_name, "caller", frm.f_back.f_code.co_name)
    inner()

# 14. Pitfalls ---------------------------------------------------------------


def pitfalls():
    h("pitfalls")
    print("* Avoid monkey-patching sys.modules in libraries — collision risk.")
    print("* Raising recursionlimit too high risks seg-faults.")
    print("* settrace impacts performance drastically; use sparingly.")

# 15. main -------------------------------------------------------------------


def main():
    argv_demo()
    exit_and_excepthook()
    path_import_control()
    stdout_stderr_swap()
    recursion_and_sizeof()
    modules_cache()
    refcount_and_getallocatedblocks()
    gil_switch_interval()
    profiler_and_tracer()
    asyncgen_hooks()
    dlopenflags_demo()
    platform_runtime_info()
    introspection_getframe()
    pitfalls()


if __name__ == "__main__":
    main()
