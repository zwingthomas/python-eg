# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/datetime.html
# IANA tzdata via zoneinfo (PEP 615)
#     https://peps.python.org/pep-0615/
# Real Python – "Mastering Date and Time in Python"
# ChatGPT - model o3

"""
Executable, in‑depth guide to Python’s **datetime** module (with `zoneinfo`)
============================================================================
Covers naive vs aware objects, arithmetic, parsing/formatting, Unix timestamps,
`zoneinfo` time‑zones, daylight‑saving transitions, ISO‑8601, `timedelta`
basics, performance tips, and common pitfalls.

Sections
--------
1.  now_and_today()               – naive vs aware `datetime.now()`
2.  custom_timezone()             – fixed offset vs IANA zone
3.  arithmetic_and_relativedelta  – `timedelta` math, weeks, microseconds
4.  from_timestamp_iso()          – epoch ↔ dt, `fromisoformat`, `datetime.strptime`
5.  daylight_saving_transition★   – fold vs gap handling (PEP 495)
6.  utc_conversion_roundtrip()    – `astimezone`, UTC offsets
7.  formatting_strftime()         – common directives table
8.  dateutil_style_parser()★      – graceful fallback if dateutil available
9.  performance_tips()            – tzinfo cache, timestamp int
10. pitfalls()                    – naive mixing, leap seconds, microsecond loss
11. main()

Run directly:
```bash
python datetime_module_tutorial.py
```
"""

from __future__ import annotations

import datetime as dt
import math
import sys
from pprint import pprint

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except ImportError:
    ZoneInfo = None  # type: ignore


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# 1. now(), today() -----------------------------------------------------------


def now_and_today():
    h("now_and_today")
    naive = dt.datetime.now()
    aware = dt.datetime.now(dt.timezone.utc)
    print("naive now     →", naive)
    print("aware UTC now →", aware)
    print("today() date  →", dt.date.today())

# 2. tzinfo: fixed vs IANA ----------------------------------------------------


def custom_timezone():
    h("custom_timezone")
    est = dt.timezone(dt.timedelta(hours=-5), name="EST")
    t_est = dt.datetime(2025, 6, 29, 12, 0, tzinfo=est)
    print("EST aware →", t_est.isoformat())
    if ZoneInfo:
        ny = ZoneInfo("America/New_York")
        t_ny = t_est.astimezone(ny)
        print("NY w/ zoneinfo →", t_ny.tzname())
    else:
        print("zoneinfo not available – skip IANA demo")

# 3. timedelta math -----------------------------------------------------------


def arithmetic_and_relativedelta():
    h("arithmetic_and_relativedelta")
    delta = dt.timedelta(days=10, hours=5, microseconds=250)
    print("timedelta →", delta)
    start = dt.datetime(2025, 1, 1)
    end = start + delta
    print("start + delta →", end)
    diff = end - start
    print("diff days →", diff.days, "seconds →", diff.seconds)

# 4. Timestamp & ISO parsing --------------------------------------------------


def from_timestamp_iso():
    h("from_timestamp_iso")
    ts = 1_752_000_000  # ~2025‑07‑05
    dtu = dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)
    print("fromtimestamp UTC →", dtu)
    iso = "2025-06-29T14:55:00-04:00"
    parsed = dt.datetime.fromisoformat(iso)
    print("fromisoformat →", parsed)
    fmt = dt.datetime.strptime("06/29/25 02-55PM", "%m/%d/%y %I-%M%p")
    print("strptime custom →", fmt)

# 5. DST transition fold/gap --------------------------------------------------


def daylight_saving_transition():
    if not ZoneInfo:
        return
    h("daylight_saving_transition")
    ny = ZoneInfo("America/New_York")
    wall = dt.datetime(2025, 11, 2, 1, 30, tzinfo=ny)  # ambiguous fall-back
    print("wall clock →", wall, "fold=", wall.fold)
    fold1 = wall.replace(fold=1)
    print("fold=1 represents second 1:30 →", fold1.utcoffset())

# 6. UTC round‑trip -----------------------------------------------------------


def utc_conversion_roundtrip():
    h("utc_conversion_roundtrip")
    local = dt.datetime.now().astimezone()
    utc = local.astimezone(dt.timezone.utc)
    back = utc.astimezone(local.tzinfo)
    print("local  →", local)
    print("UTC    →", utc)
    print("roundtrip diff seconds →", (back - local).total_seconds())

# 7. strftime formatting ------------------------------------------------------


def formatting_strftime():
    h("formatting_strftime")
    sample = dt.datetime(2025, 6, 29, 16, 45)
    print(sample.strftime("%Y-%m-%d %H:%M"))
    table = {
        "%d": "day 01‑31",
        "%b": "locale short month",
        "%A": "weekday full",
        "%j": "day of year",
        "%z": "+hhmm offset",
        "%I": "12‑h clock",
    }
    for k, v in table.items():
        print(f"{k} → {sample.strftime(k)} ({v})")

# 8. dateutil parser fallback -------------------------------------------------


def dateutil_style_parser():
    h("dateutil_style_parser")
    try:
        from dateutil import parser
        loose = parser.parse("29 Jun 25 4:45pm")
        print("dateutil parse →", loose)
    except ImportError:
        print("python‑dateutil not installed – skip")

# 9. Performance notes --------------------------------------------------------


def performance_tips():
    h("performance_tips")
    utc_now = dt.datetime.utcnow  # local ref
    loops = 1_000_00
    t0 = dt.datetime.now()
    for _ in range(loops):
        utc_now()
    dt_total = (dt.datetime.now() - t0).total_seconds()
    print(f"{loops:,} utcnow() avg → {dt_total/loops*1e6:.1f} µs")

# 10. Pitfalls ---------------------------------------------------------------


def pitfalls():
    h("pitfalls")
    print("* Mixing naive + aware raises TypeError – convert first.")
    print("* No leap‑second support – UTC 2016‑12‑31 23:59:60 invalid.")
    print("* Beware of daylight‑saving gaps when adding hours; use `zoneinfo` + normalize pattern.")

# main -----------------------------------------------------------------------


def main():
    now_and_today()
    custom_timezone()
    arithmetic_and_relativedelta()
    from_timestamp_iso()
    daylight_saving_transition()
    utc_conversion_roundtrip()
    formatting_strftime()
    dateutil_style_parser()
    performance_tips()
    pitfalls()


if __name__ == "__main__":
    main()
