# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/random.html
# Raymond Hettinger – "Modern Random Number Generators" (PyBay 2020)
#     https://youtu.be/sKazYCqsA24
# Real‑Python – "The Random Module in Python"
#     https://realpython.com/python-random/
# ChatGPT - model o3

"""
Hands-on tour of Python's **random** module
==========================================
Each section is a self-contained demo.  Run the file top-to-bottom or cherry-pick
what you need.  ⚠️ markers highlight classic gotchas.

Sections
--------
1.  seed_vs_randobj()          - global seeding vs independent RNG objects
2.  basic_numbers()            - rand.rand.random(), randint, randrange, uniform
3.  sequence_ops()             - choice, choices, sample, shuffle
4.  weighted_sampling()        - weights vs cum_weights pitfalls
5.  distributions_demo()       - gauss, normalvariate, expovariate …
6.  secrets_vs_rnd.random()    - cryptographic randomness
7.  reprod_threading()         - why per-thread Random() matters
8.  subclass_custom_rng()      - plug your own bit generator
9.  reproducibility_limits()   - "don't rely on bit-exact streams across versions"
10. main()                     - run everything in order

Run directly:

```bash
python random_module_tutorial.py
```
"""

from __future__ import annotations

import secrets
import threading
import time
from collections import Counter
from pprint import pprint
import random as rnd  # full module for seeding etc.
from random import (
    Random,
    choice,
    choices,
    expovariate,
    gauss,
    normalvariate,
    randrange,
    sample,
    shuffle,
    uniform,
)

# ──────────────────────────────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────────────────────────────


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# ──────────────────────────────────────────────────────────────────────
# 1. Seeding the global RNG vs independent Random objects
# ──────────────────────────────────────────────────────────────────────


def seed_vs_randobj():
    h("seed_vs_randobj")

    rnd.seed(42)
    print("global rnd.random() →", rnd.random())

    rng1 = Random(42)
    rng2 = Random(42)
    print("rng1.random() →", rng1.random())
    # same as rng1 – isolated streams
    print("rng2.random() →", rng2.random())

    # ⚠️ reseeding the *global* RNG affects *all* later calls using module funcs
    rnd.seed(99)
    print("global after reseed →", rnd.random())

# ──────────────────────────────────────────────────────────────────────
# 2. Basic numeric generators & off‑by‑one traps
# ──────────────────────────────────────────────────────────────────────


def basic_numbers():
    h("basic_numbers")

    print("rnd.random() in [0,1)  →", rnd.random())
    # TODO: randint is INCLUSIVE on both ends (⚠️ easy to forget)
    for _ in range(20):
        print("inclusive on both ends: randint(1,6) →", rnd.randint(1, 6))
    print("uniform(1,3)   →", uniform(1, 3))
    # randrange stop is exclusive, like range()
    print("exclusive like range(): randrange(10) →", randrange(10))

# ──────────────────────────────────────────────────────────────────────
# 3. Sequence helpers – beware mutable shuffle side‑effects
# ──────────────────────────────────────────────────────────────────────

# TODO: This is very, very cool


def sequence_ops():
    h("sequence_ops")
    deck = list(range(1, 53))
    shuffle(deck)  # in‑place; returns None
    print("Top 5 cards after shuffle:", deck[:5])

    print("choice(deck)      →", choice(deck))
    print("sample(deck, 5)   →", sample(deck, 5))

# ──────────────────────────────────────────────────────────────────────
# 4. Weighted sampling – common pitfalls
# ──────────────────────────────────────────────────────────────────────


def weighted_sampling():
    h("weighted_sampling")
    population = ["red", "green", "blue"]
    pulls = choices(population, weights=[0.6, 0.3, 0.1], k=20)
    print("20 pulls with weights 0.6/0.3/0.1 ->")
    pprint(Counter(pulls))

    # ⚠️ weights *and* cum_weights are mutually exclusive; passing both raises
    # TODO: How to use cumulative weights?
    try:
        choices(population, weights=[1, 1, 1], cum_weights=[1, 2, 3])
    except TypeError as exc:
        print("weights + cum_weights error →", exc)

# ──────────────────────────────────────────────────────────────────────
# 5. Continuous distributions
# ──────────────────────────────────────────────────────────────────────


def distributions_demo():
    h("distributions_demo")
    print("normalvariate(μ=0,σ=1) →", normalvariate(0, 1))
    print("gauss(0,1) (≈normalvariate) →", gauss(0, 1))
    print("expovariate(λ=1/10) →", expovariate(1 / 10))

# ─────────────────────────────────────────────────────────────────────-
# 6. Cryptographically strong randomness vs PRNG
# ──────────────────────────────────────────────────────────────────────


def secrets_vs_rnd_random():
    h("secrets_vs_random")
    token = secrets.token_hex(8)
    print("secrets.token_hex(8) →", token)

    print("random.getrandbits(32) →", Random().getrandbits(32))

# ──────────────────────────────────────────────────────────────────────
# 7. Thread safety & per‑thread RNGs
# ──────────────────────────────────────────────────────────────────────


def reprod_threading():
    h("reprod_threading")

    results: list[float] = []

    def worker(seed):
        r = Random(seed)
        results.append(r.random())

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("Independent per-thread numbers:", results)

# ──────────────────────────────────────────────────────────────────────
# 8. Custom RNG by subclassing Random
# ──────────────────────────────────────────────────────────────────────


def subclass_custom_rng():
    h("subclass_custom_rng")

    class XorShift(Random):
        """Very small XORShift demo - *not* for real use."""

        def __init__(self, seed):
            super().__init__()
            self.state = seed & 0xFFFFFFFF

        def random(self):  # returns float in [0,1)
            x = self.state
            x ^= (x << 13) & 0xFFFFFFFF
            x ^= (x >> 17)
            x ^= (x << 5) & 0xFFFFFFFF
            self.state = x & 0xFFFFFFFF
            return x / 2**32

    xs = XorShift(123456)
    print("XorShift rnd.random() →", [xs.random() for _ in range(3)])

# ──────────────────────────────────────────────────────────────────────
# 9. Reproducibility caveats across Python versions
# ──────────────────────────────────────────────────────────────────────


def reproducibility_limits():
    h("reproducibility_limits")
    Random(0).seed(0)
    v = Random(0).random()
    print("First rnd.random() w/seed 0 on this interpreter →", v)
    print("⚠️  The exact bit stream is *not* guaranteed across major Python versions.")

# ──────────────────────────────────────────────────────────────────────
# 10. main
# ──────────────────────────────────────────────────────────────────────


def main():
    seed_vs_randobj()
    basic_numbers()
    sequence_ops()
    weighted_sampling()
    distributions_demo()
    secrets_vs_rnd_random()
    reprod_threading()
    subclass_custom_rng()
    reproducibility_limits()


if __name__ == "__main__":
    main()
