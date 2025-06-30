# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/hashlib.html
# Real Python – "Secure Hashes and Passwords With Python"
#     https://realpython.com/python-hashlib/
# NIST SP 800-132 recommendations (PBKDF2 parameters)
# ChatGPT - model o3

"""
Executable guide to Python’s **hashlib** (plus PBKDF2, scrypt, BLAKE2)
=====================================================================
This expanded version adds a quick “cheat-sheet” mapping of algorithms → best
use-cases so you immediately see which hash to pick.

Sections
--------
1.  list_algorithms() ★         – names **plus** guidance table
2.  basic_hashes()              – SHA-256, incremental update
3.  file_stream_hash()          – chunked hashing of big file
4.  constant_time_compare()     – `hmac.compare_digest`
5.  salts_and_pbkdf2()          – password hashing with PBKDF2-HMAC
6.  blake2_demo()               – keyed hashing, personalization
7.  sha3_and_shake()            – variable-length SHAKE
8.  scrypt_kdf()               – memory-hard KDF
9.  pitfalls()                  – MD5 collision, timing attacks, salt reuse
10. cleanup()
11. main()
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import tempfile
from pathlib import Path
from pprint import pprint

TMP = Path(tempfile.gettempdir()) / (Path(__file__).stem + "_tmp")
TMP.mkdir(exist_ok=True)


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# 1. List algorithms + guidance ----------------------------------------------


def list_algorithms():
    h("list_algorithms")
    print("guaranteed →", hashlib.algorithms_guaranteed)
    print("first 12 available →", sorted(hashlib.algorithms_available)[:12])

    guidance = {
        "SHA-256 / SHA-512": "General-purpose cryptographic hash (signatures, file integrity)",
        "SHA-3 family": "Post-2015 standard, slower but resistant to length-extension",
        "BLAKE2b/BLAKE2s": "Fast, keyed MAC-like option, file dedup, data integrity",
        "MD5 / SHA-1": "Legacy, collision-prone – *avoid* for new designs",
        "PBKDF2-HMAC": "Password hashing (tunable work factor)",
        "scrypt / Argon2": "Password hashing – memory-hard (resists GPU cracking)",
        "SHAKE128/256": "Extendable-output for variable-length digests",
    }
    print("\nAlgorithm cheat-sheet:")
    for algo, use in guidance.items():
        print(f"• {algo:<15} → {use}")

# 2. Basic hashes -------------------------------------------------------------


def basic_hashes():
    h("basic_hashes")
    data = b"hello hashlib"
    sha = hashlib.sha256(data)
    print("sha256 →", sha.hexdigest())
    inc = hashlib.sha256()
    inc.update(b"hello ")
    inc.update(b"hashlib")
    print("incremental match?", inc.digest() == sha.digest())

# 3. File streaming ----------------------------------------------------------


def file_stream_hash():
    h("file_stream_hash")
    big = TMP / "big.bin"
    big.write_bytes(os.urandom(1_000_000))
    m = hashlib.md5()
    with big.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            m.update(chunk)
    print("MD5(big) →", m.hexdigest())

# 4. Constant-time compare ----------------------------------------------------


def constant_time_compare():
    h("constant_time_compare")
    good = hashlib.sha256(b"secret").digest()
    bad = hashlib.sha256(b"secreT").digest()
    print("==", good == bad, "compare_digest", hmac.compare_digest(good, bad))

# 5. PBKDF2 ------------------------------------------------------------------


def salts_and_pbkdf2():
    h("salts_and_pbkdf2")
    pw = b"hunter2"
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", pw, salt, 100_000, 32)
    print("PBKDF2 dk first 16 hex →", dk.hex()[:16], "…")

# 6. BLAKE2 ------------------------------------------------------------------


def blake2_demo():
    h("blake2_demo")
    hsh = hashlib.blake2b(b"data", key=b"k", digest_size=16, person=b"demo")
    print("blake2b keyed 128-bit →", hsh.hexdigest())

# 7. SHA-3 / SHAKE -----------------------------------------------------------


def sha3_and_shake():
    h("sha3_and_shake")
    print("sha3_256 →", hashlib.sha3_256(b"msg").hexdigest())
    sh = hashlib.shake_128(b"msg").hexdigest(20)
    print("shake128 20-byte →", sh)

# 8. scrypt ------------------------------------------------------------------


def scrypt_kdf():
    if not hasattr(hashlib, "scrypt"):
        return
    h("scrypt_kdf")
    key = hashlib.scrypt(b"pwd", salt=os.urandom(16),
                         n=2**14, r=8, p=1, dklen=32)
    print("scrypt key first 16 →", key.hex()[:16], "…")

# 9. Pitfalls ----------------------------------------------------------------


def pitfalls():
    h("pitfalls")
    print("* MD5/SHA-1 considered broken – collisions found.")
    print("* Re-using salt lets rainbow-tables target many users.")
    print("* HMAC still preferred over raw keyed hash in many protocols.")

# 10. Cleanup ----------------------------------------------------------------


def cleanup():
    for p in TMP.iterdir():
        p.unlink()
        TMP.rmdir()

# 11. main -------------------------------------------------------------------


def main():
    list_algorithms()
    basic_hashes()
    file_stream_hash()
    constant_time_compare()
    salts_and_pbkdf2()
    blake2_demo()
    sha3_and_shake()
    scrypt_kdf()
    pitfalls()
    cleanup()


if __name__ == "__main__":
    main()
