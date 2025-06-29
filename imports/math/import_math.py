# Acknowledgements____
# Official docs
#     https://docs.python.org/3/library/math.html
# Raymond Hettinger – "Floating‑Point Math" (PyCon 2019)
#     https://youtu.be/-gd_BKbt3Kk
# Real‑Python – "Using the Python math Module"
#     https://realpython.com/python-math-module/
# ChatGPT - Model o3

"""
Walk‑through of Python’s **math** standard‑library module
=======================================================
The goal is to *run & read* this file to see how each function behaves and
where surprises lurk.

Common tripping points called out with ⛔ or ⚠️ markers.

Sections
--------
1.  constants_demo()            – e, pi, tau, inf, nan
2.  basic_ops()                 – sqrt vs **½, pow vs **, fmod vs %, remainder()
3.  int_and_fraction()          – ceil, floor, trunc, modf, frexp, ldexp
4.  trig_radians()              – sin/cos/tan: beware *degrees*!
5.  degrees_conversion()        – radians(), degrees(), isclose() pitfalls
6.  combinatorics()             – factorial, comb, perm (int‑only!)
7.  special_functions()         – log varieties, expm1, erf, gamma, hypot
8.  float_edge_cases()          – nan/inf propagation, copysign, isnan, isfinite
9.  math_vs_cmath()             – domain errors & complex fallback
10. main()                      – run all demos

Run directly:

```bash
python math_module_tutorial.py
```
"""

from __future__ import annotations

import cmath  # for comparison
import math
import sys
from pprint import pprint

# ──────────────────────────────────────────────────────────────────────
# Pretty helpers
# ──────────────────────────────────────────────────────────────────────


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# ──────────────────────────────────────────────────────────────────────
# 1. Constants
# ──────────────────────────────────────────────────────────────────────


def constants_demo():
    h("constants_demo")
    print("pi  :", math.pi)
    print("tau :", math.tau)  # 2π – handy for full‑circle maths
    print("e   :", math.e)
    print("inf :", math.inf)
    print("-inf:", -math.inf)
    print("nan :", math.nan)
    print("nan == nan?", math.nan == math.nan)  # always False!

# ──────────────────────────────────────────────────────────────────────
# 2. Basic arithmetic helpers & gotchas
# ──────────────────────────────────────────────────────────────────────


def basic_ops():
    h("basic_ops")

    # sqrt vs exponent
    print("sqrt(2)", math.sqrt(2))
    print("2 ** 0.5", 2 ** 0.5)  # same but sqrt is clearer

    # pow ⚠️  math.pow promotes to float, ** keeps int→int when possible
    print("math.pow(2, 3) ->", math.pow(2, 3))  # always float 8.0
    print("2 ** 3        ->", 2 ** 3)           # int 8

    # ⛔ fmod vs %  – different sign rules for negatives
    print("-3 % 2   ->", -3 % 2)           # 1 (Python’s mod wraps toward +∞)
    print("fmod(-3,2)->", math.fmod(-3, 2))  # -1 (wraps toward 0 like C)

    # New in 3.7: remainder – IEEE 754 style, ties to even
    print("remainder(7, 4) ->", math.remainder(7, 4))

# ──────────────────────────────────────────────────────────────────────
# 3. Integer & fractional splitting
# ──────────────────────────────────────────────────────────────────────


def int_and_fraction():
    h("int_and_fraction")
    x = 3.14159
    print("ceil", math.ceil(x))
    print("floor", math.floor(x))
    print("trunc", math.trunc(x))

    frac, intpart = math.modf(x)
    print("modf -> frac, int:", frac, intpart)

    # frexp/ldexp: break into mantissa+exp  ; recombine
    m, e = math.frexp(x)   # x == m * 2**e, 0.5<=|m|<1
    print("frexp", m, e)
    print("ldexp(m,e)", math.ldexp(m, e))

# ──────────────────────────────────────────────────────────────────────
# 4. Trigonometry (radians!)
# ──────────────────────────────────────────────────────────────────────


def trig_radians():
    h("trig_radians")
    angle_deg = 30
    angle_rad = math.radians(angle_deg)
    print("sin(30°)   ->", math.sin(angle_rad))
    print("cos(30°)   ->", math.cos(angle_rad))
    print("tan(30°)   ->", math.tan(angle_rad))

    # ⛔ Passing degrees directly is wrong!
    wrong = math.sin(30)
    print("sin(30) assuming radians ->", wrong)

# ──────────────────────────────────────────────────────────────────────
# 5. Conversion helpers + isclose issues
# ──────────────────────────────────────────────────────────────────────


def degrees_conversion():
    h("degrees_conversion")
    print("degrees(pi)  ->", math.degrees(math.pi))
    print("radians(180)->", math.radians(180))

    # float inexactness & isclose()
    a = 0.1 + 0.2
    b = 0.3
    print("0.1+0.2 == 0.3?", a == b)
    print("isclose?", math.isclose(a, b))  # default tolerances
    print("isclose strict tol?", math.isclose(a, b, rel_tol=0, abs_tol=0))

# ──────────────────────────────────────────────────────────────────────
# 6. Combinatorics – ints only!
# ──────────────────────────────────────────────────────────────────────


def combinatorics():
    h("combinatorics")
    print("factorial(5)", math.factorial(5))
    # ⛔ factorial requires *integers ≥ 0* – floats raise TypeError
    try:
        math.factorial(3.2)
    except (TypeError, ValueError) as exc:
        print("factorial(3.2) error ->", exc)

    print("comb(5,2)", math.comb(5, 2))
    print("perm(5,2)", math.perm(5, 2))

# ──────────────────────────────────────────────────────────────────────
# 7. Special functions & hypot
# ──────────────────────────────────────────────────────────────────────


def special_functions():
    h("special_functions")
    print("exp(1)->", math.exp(1))
    print("expm1(1e-8) high precision ->", math.expm1(1e-8))

    print("log(8,2) ->", math.log(8, 2))
    print("log2(8)  ->", math.log2(8))
    print("log10(1000) ->", math.log10(1000))

    print("gamma(5)", math.gamma(5))  # (n-1)!
    print("erf(1)  ", math.erf(1))

    print("hypot(3,4,12)", math.hypot(3, 4, 12))  # √(3²+4²+12²)

# ──────────────────────────────────────────────────────────────────────
# 8. NaN / Inf quirks
# ──────────────────────────────────────────────────────────────────────


def float_edge_cases():
    h("float_edge_cases")
    nan = math.nan
    inf = math.inf
    print("isnan(nan)", math.isnan(nan))
    print("isfinite(inf)", math.isfinite(inf))
    print("copysign(3,-0.0)", math.copysign(3, -0.0))

    print("nan+1 ->", nan + 1)
    print("inf/inf ->", inf / inf)

# ──────────────────────────────────────────────────────────────────────
# 9. math vs cmath domain errors
# ──────────────────────────────────────────────────────────────────────


def math_vs_cmath():
    h("math_vs_cmath")
    try:
        math.sqrt(-1)
    except ValueError as exc:
        print("math.sqrt(-1) ValueError ->", exc)

    print("cmath.sqrt(-1) ->", cmath.sqrt(-1))

# ──────────────────────────────────────────────────────────────────────
# 10. main
# ──────────────────────────────────────────────────────────────────────


def main():
    constants_demo()
    basic_ops()
    int_and_fraction()
    trig_radians()
    degrees_conversion()
    combinatorics()
    special_functions()
    float_edge_cases()
    math_vs_cmath()


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    main()
