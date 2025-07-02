# Acknowledgements____
# Official docs
#     https://docs.python.org/3/library/csv.html
# Real-Python
#     https://realpython.com/python-csv/
# ChatGPT - Model o3
"""
Hands-on tour of Python's built-in **csv** module
=================================================
This file is meant to be *read like a notebook*: run it top-to-bottom or dip
into the individual functions.  Every feature of the module appears at least
once so you can copy-paste the patterns straight into real projects.

Why use the `csv` module instead of plain `str.split(',')`?
----------------------------------------------------------
* Handles embedded commas, quotes and newlines correctly.
* Works the same way on Windows, macOS and Linux (universal newline
  handling + `newline=''` hint).
* Lets you read rows as dictionaries — ideal for column-oriented data.
* Gives you full control over delimiter, quote-char, escape-char,
  line-terminator & quoting policy.

The file is organised like this::

    ├── quick_demo()        - 10-second intro
    ├── basic_reader_writer()
    ├── dict_reader_writer()
    ├── custom_dialect()
    ├── sniff_dialect()
    ├── large_file_streaming()
    └── main()              - runs everything & cleans up

Run "python csv_module_tutorial.py" directly to see it all in action.
"""

from __future__ import annotations

import csv
import io
import itertools
import os
from pathlib import Path
from pprint import pprint
from textwrap import dedent

# ──────────────────────────────────────────────────────────────────────
# Set-up helpers
# ──────────────────────────────────────────────────────────────────────

TMP_DIR = Path(__file__).with_suffix("").name + "_tmp"
TMP_DIR_PATH = Path.cwd() / TMP_DIR
TMP_DIR_PATH.mkdir(exist_ok=True)


def _tmpfile(name: str) -> Path:
    """Return a Path inside the scratch directory so we don't litter PWD."""
    return TMP_DIR_PATH / name

# ──────────────────────────────────────────────────────────────────────
# 0. Quick taste – read and write a tiny CSV from memory
# ──────────────────────────────────────────────────────────────────────


def quick_demo() -> None:
    """The absolute minimum usage pattern."""
    print("\n[ quick_demo ]\n" + "-" * 60)
    in_memory = io.StringIO("""name,score\nAda,98\nGrace,97\n""")
    reader = csv.reader(in_memory)
    header = next(reader)          # ['name', 'score']
    rows = list(reader)            # [['Ada', '98'], ['Grace', '97']]

    print("Header:", header)
    print("Data rows:")
    pprint(rows)

    # Now write the same data back out (also to memory so we stay self-contained)
    out_memory = io.StringIO()
    writer = csv.writer(out_memory)
    writer.writerow(header)
    writer.writerows(rows)

    print("\nRound-tripped CSV string:")
    print(out_memory.getvalue())

# ──────────────────────────────────────────────────────────────────────
# 1. Basic reader / writer on disk
# ──────────────────────────────────────────────────────────────────────


def basic_reader_writer() -> None:
    """Read & write lists of lists with custom delimiter and quoting."""
    print("\n[ basic_reader_writer ]\n" + "-" * 60)
    data = [
        ["id", "city", "pop"],
        [1, "New York", 8_336_817],    # note the non-breaking space between words
        [2, "Los Angeles", 3_979_576],
        [3, "Chicago", 2_693_976],
    ]

    path = _tmpfile("cities.csv")
    # Always open with newline='' → lets csv module manage universal newlines.
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(
            f,
            delimiter=",",            # default – shown explicitly
            quoting=csv.QUOTE_MINIMAL,  # only quote fields containing special chars
            lineterminator="\n",      # explicit just to show where you set it
        )
        writer.writerows(data)
    print(f"Wrote {path.relative_to(Path.cwd())}")

    # Read it back – csv.reader returns each row as a list of strings
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

# ──────────────────────────────────────────────────────────────────────
# 2. DictReader / DictWriter – column oriented I/O
# ──────────────────────────────────────────────────────────────────────


def dict_reader_writer() -> None:
    """Work with rows as dicts; demonstrate restval & extrasaction."""
    print("\n[ dict_reader_writer ]\n" + "-" * 60)

    raw_csv = dedent(
        """
        song,artist,year,length
        The Pretender,Foo Fighters,2007,4:29
        Smells Like Teen Spirit,Nirvana,1991,5:01,extra_col
        Bittersweet Symphony,The Verve,1997
        """
    ).strip()

    path = _tmpfile("songs.csv")
    path.write_text(raw_csv, encoding="utf-8")

    # Reading
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(
            f,
            restkey="EXTRA",      # surplus columns go to this key
            restval="MISSING",    # missing columns get this default value
        )
        rows = list(reader)
    pprint(rows)

    # Writing – we'll drop the EXTRA column on purpose.
    out_path = _tmpfile("songs_out.csv")
    with out_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["song", "artist", "year", "length"]
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore",  # silently skip unknown keys
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Cleaned CSV saved to {out_path.relative_to(Path.cwd())}")

# ─────────────────────────────────────────────────────────────────────-
# 3. Defining & registering a custom dialect
# ─────────────────────────────────────────────────────────────────────-


def custom_dialect() -> None:
    """Create a semicolon-delimited dialect with quoting disabled."""
    print("\n[ custom_dialect ]\n" + "-" * 60)

    class SemiNoQuote(csv.Dialect):
        delimiter = ";"
        quotechar = "\0"        # impossible char => quoting disabled
        lineterminator = "\n"
        doublequote = False
        skipinitialspace = True
        quoting = csv.QUOTE_NONE

    csv.register_dialect("semi_no_quote", SemiNoQuote)

    path = _tmpfile("fruits.csv")
    path.write_text(
        """id; name; color\n1; apple; red\n2; banana; yellow\n""", encoding="utf-8")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, dialect="semi_no_quote")
        pprint(list(reader))

# ─────────────────────────────────────────────────────────────────────-
# 4. Let the Sniffer figure it out
# ──────────────────────────────────────────────────────────────────────


def sniff_dialect() -> None:
    """Use csv.Sniffer to auto-detect delimiter & quoting style."""
    print("\n[ sniff_dialect ]\n" + "-" * 60)

    messy = dedent(
        """
    name|age|city
    Ada|36|Zürich
    Grace|47|New York
    """
    ).strip()
    path = _tmpfile("messy.csv")
    path.write_text(messy, encoding="utf-8")

    with path.open(encoding="utf-8") as f:
        sample = f.read(1024)
        dialect = csv.Sniffer().sniff(sample)
        f.seek(0)
        reader = csv.reader(f, dialect=dialect)
        pprint(list(reader))
    print("Detected delimiter:", repr(dialect.delimiter))

# ──────────────────────────────────────────────────────────────────────
# 5. Streaming a large file row-by-row (constant memory)
# ─────────────────────────────────────────────────────────────────────-


def large_file_streaming() -> None:
    """Pretend to handle a huge file – we generate on the fly via StringIO."""

    print("\n[ large_file_streaming ]\n" + "-" * 60)
    row_template = "{idx},value_{idx}\n"
    fake_big = io.StringIO(
        "id,val\n" + "".join(row_template.format(idx=i) for i in range(1_000_000)))

    reader = csv.reader(fake_big)
    header = next(reader)
    total = 0
    for _ in itertools.islice(reader, 10):   # show first 10 lines only
        total += 1
    print(
        f"Read {total} rows without loading entire file into RAM (thanks to lazy iteration).")

# ──────────────────────────────────────────────────────────────────────
# 6. main – run all demos & tidy up
# ──────────────────────────────────────────────────────────────────────


def main() -> None:
    quick_demo()
    basic_reader_writer()
    dict_reader_writer()
    custom_dialect()
    sniff_dialect()
    large_file_streaming()

    # Clean-up tmp files
    for p in TMP_DIR_PATH.glob("*.*"):
        p.unlink()
    TMP_DIR_PATH.rmdir()
    print("\nTemporary files removed – spotless!")


if __name__ == "__main__":
    main()
