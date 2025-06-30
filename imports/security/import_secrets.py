# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/secrets.html
# PyJWT docs (optional dependency)
#     https://pyjwt.readthedocs.io/
# OWASP Password Storage Cheat Sheet
# ChatGPT - model o3

"""
Practical, runnable guide to Python’s **secrets** module
=======================================================
Expanded with JWT-ready key generation (HS256 & RS256) that works even when
`PyJWT` isn’t installed.

Sections
--------
1.  quick_token_generation()    – `token_hex`, `token_urlsafe`
2.  secure_randbelow_choice()   – uniform ints, crypto shuffle
3.  constant_time_compare()     – timing-safe equality
4.  building_passwords()        – human-safe + entropy
5.  salts_and_kdfs()            – 16-byte salt for PBKDF2 / scrypt
6.  jwt_signing_keys() ★        – HS256 secret + optional RSA 2048 bits
7.  secrets_vs_random()         – predictability demo
8.  pool_password_hasher()      – reusable helper
9.  pitfalls()                  – collisions, URL length, padding
10. main()
"""

from __future__ import annotations

import base64
import hmac
import math
import os
import secrets
import subprocess
from hashlib import pbkdf2_hmac
from pathlib import Path
from pprint import pprint
from typing import Optional


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# 1. quick token helpers ------------------------------------------------------


def quick_token_generation():
    h("quick_token_generation")
    print("token_hex 16 →", secrets.token_hex(16))
    print("token_urlsafe 16 →", secrets.token_urlsafe(16))

# 2. randbelow / choice -------------------------------------------------------


def secure_randbelow_choice():
    h("secure_randbelow_choice")
    print("randbelow 6 +1 die →", secrets.randbelow(6) + 1)
    deck = list(range(52))
    secrets.SystemRandom().shuffle(deck)
    print("top 5 cards →", deck[:5])

# 3. constant-time compare ----------------------------------------------------


def constant_time_compare():
    h("constant_time_compare")
    a = secrets.token_bytes(32)
    b = bytearray(a)
    b[-1] ^= 1
    print("==", a == b, "compare_digest", hmac.compare_digest(a, b))

# 4. Password generation ------------------------------------------------------


def building_passwords():
    h("building_passwords")
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789!@#%?"
    pwd = "".join(secrets.choice(alphabet) for _ in range(16))
    entropy = math.log2(len(alphabet)) * 16
    print("password", pwd, "entropy ≈", round(entropy, 1), "bits")

# 5. Salt + KDF ---------------------------------------------------------------


def salts_and_kdfs():
    h("salts_and_kdfs")
    salt = secrets.token_bytes(16)
    dk = pbkdf2_hmac("sha256", b"pass", salt, 200_000, 32)
    print("salt16", salt.hex(), "key first16", dk.hex()[:16])

# 6. JWT signing key helpers --------------------------------------------------


def _generate_rsa_keypair() -> Optional[tuple[Path, Path]]:
    """Generate RSA-2048 keypair via OpenSSL if available."""
    if shutil.which("openssl") is None:
        return None
    tmp_dir = Path(os.getenv("TMPDIR", "/tmp"))
    priv = Path(tmp_dir) / "jwt_priv.pem"
    pub = Path(tmp_dir) / "jwt_pub.pem"
    subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-out", priv,
                   "-pkeyopt", "rsa_keygen_bits:2048"], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["openssl", "rsa", "-pubout", "-in", priv,
                   "-out", pub], check=True, stdout=subprocess.DEVNULL)
    return priv, pub


def jwt_signing_keys():
    h("jwt_signing_keys")
    # HS256 secret (256-bit)
    secret = secrets.token_urlsafe(32)
    print("HS256 secret len", len(secret), "chars →", secret)

    # optional RS256 if OpenSSL present
    pair = _generate_rsa_keypair()
    if pair:
        priv, pub = pair
        print("RSA-2048 private key →", priv)
        print("RSA-2048 public key  →", pub)
    else:
        print("OpenSSL not found – RSA demo skipped")

# 7. Predictability demo ------------------------------------------------------


def secrets_vs_random():
    h("secrets_vs_random")
    import random
    random.seed(42)
    print("random randint 5× →", [random.randint(0, 100) for _ in range(5)])
    print("secrets.randbelow 5× →", [secrets.randbelow(101) for _ in range(5)])

# 8. Reusable password hasher -------------------------------------------------


def pool_password_hasher(pw: str, rounds: int = 200_000):
    salt = secrets.token_bytes(16)
    dk = pbkdf2_hmac("sha256", pw.encode(), salt, rounds, 32)
    return {"salt": base64.b64encode(salt).decode(), "hash": dk.hex(), "r": rounds}


def pool_password_hasher_demo():
    h("pool_password_hasher_demo")
    pprint(pool_password_hasher("s3cr3t"))

# 9. Pitfalls ----------------------------------------------------------------


def pitfalls():
    h("pitfalls")
    print("* token_urlsafe no padding – good for URLs, decode with '=' padding fix.")
    print("* HS256 secrets need ≥256 bits; don't reuse between prod/stage envs.")
    print("* RSA private key generation requires external openssl or cryptography lib.")

# main -----------------------------------------------------------------------


def main():
    quick_token_generation()
    secure_randbelow_choice()
    constant_time_compare()
    building_passwords()
    salts_and_kdfs()
    jwt_signing_keys()
    secrets_vs_random()
    pool_password_hasher_demo()
    pitfalls()


if __name__ == "__main__":
    import shutil
    main()
