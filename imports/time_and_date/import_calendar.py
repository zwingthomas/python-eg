# Acknowledgements__________________________________________________________
# Official docs
#     https://docs.python.org/3/library/calendar.html
# Real Python – "Working With Calendars in Python"
# ChatGPT - model o3

"""
Executable tour of Python’s **calendar** module
==============================================
Corrected version: avoids masking the `datetime` *module* (which broke
`calendar` internals) and swaps to the instance method `Calendar.monthdays2calendar`.
"""

from __future__ import annotations

import calendar
import datetime as dt
import locale
import sys
from pathlib import Path
from textwrap import indent

YEAR, MONTH = (int(sys.argv[1]), int(sys.argv[2])
               ) if len(sys.argv) >= 3 else (2025, 6)


def h(title: str):
    print(f"\n[ {title} ]\n" + "-" * 60)

# 1. Text calendar -----------------------------------------------------------


def text_calendar_cli():
    h("text_calendar_cli")
    cal = calendar.TextCalendar(firstweekday=6)
    print(cal.formatmonth(YEAR, MONTH))
    print("snippet →")
    print(indent(cal.formatyear(YEAR)[:150], "  "))

# 2. Locale demo -------------------------------------------------------------


def locale_and_firstweekday():
    h("locale_and_firstweekday")
    try:
        locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
    except locale.Error:
        print("de_DE locale missing – skip")
        return
    loc_cal = calendar.LocaleTextCalendar(
        firstweekday=0, locale=locale.getlocale()[0])
    print(loc_cal.formatmonth(YEAR, MONTH))
    locale.setlocale(locale.LC_ALL, "C")

# 3. Iterables ---------------------------------------------------------------


def iter_monthdays_and_weeks():
    h("iter_monthdays_and_weeks")
    grid = calendar.monthcalendar(YEAR, MONTH)
    print("rows →", len(grid), "week1 →", grid[0])
    md2 = calendar.Calendar().monthdays2calendar(YEAR, MONTH)
    d, wd = md2[1][0]
    print("monthdays2calendar sample →", (d, wd))

# 4. Weekday queries ---------------------------------------------------------


def weekday_queries():
    h("weekday_queries")
    first_wd, days = calendar.monthrange(YEAR, MONTH)
    print("first weekday", first_wd, "days", days)
    print("weekday 2025‑06‑28 →", calendar.weekday(2025, 6, 28))

# 5. Custom holiday cal ------------------------------------------------------


def custom_business_calendar():
    h("custom_business_calendar")

    class HolidayCal(calendar.Calendar):
        HOLIDAYS = {dt.date(2025, 6, 19), dt.date(2025, 7, 4)}

        def itermonthdays(self, y, m):
            for d in super().itermonthdays(y, m):
                if d and dt.date(y, m, d) in self.HOLIDAYS:
                    yield -d
                else:
                    yield d
    hc = HolidayCal()
    for wk in hc.monthdayscalendar(YEAR, MONTH):
        print(" ".join(f"{d:>3}" for d in wk))

# main ----------------------------------------------------------------------


def main():
    text_calendar_cli()
    locale_and_firstweekday()
    iter_monthdays_and_weeks()
    weekday_queries()
    custom_business_calendar()


if __name__ == "__main__":
    main()
