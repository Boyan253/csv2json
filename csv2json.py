#!/usr/bin/env python3
"""Convert a CSV file to JSON or JSONL, optionally inferring value types."""

import argparse
import csv
import json
import sys

__version__ = "0.1.0"


def infer(value):
    """Turn a CSV string into an int/float/bool/None when it clearly is one."""
    if value == "":
        return None
    low = value.strip().lower()
    if low in ("true", "false"):
        return low == "true"
    if low in ("null", "none", "nil"):
        return None
    try:
        if value.strip().lstrip("+-").isdigit():
            return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def read_rows(path, delimiter, encoding):
    handle = sys.stdin if path == "-" else open(path, newline="", encoding=encoding)
    try:
        for row in csv.DictReader(handle, delimiter=delimiter):
            yield row
    finally:
        if handle is not sys.stdin:
            handle.close()


def convert(path, delimiter=",", encoding="utf-8", do_infer=False):
    for row in read_rows(path, delimiter, encoding):
        if do_infer:
            row = {k: infer(v) if v is not None else None for k, v in row.items()}
        yield row


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + __version__)
    ap.add_argument("csv_file", help="path to the CSV file, or - for stdin")
    ap.add_argument("-d", "--delimiter", default=",", help="field delimiter (default ,)")
    ap.add_argument("-e", "--encoding", default="utf-8", help="input encoding")
    ap.add_argument("--infer", action="store_true", help="parse numbers, booleans and empties")
    ap.add_argument("--lines", action="store_true", help="emit JSONL (one object per line)")
    ap.add_argument("--indent", type=int, default=2, help="indent for JSON output")
    args = ap.parse_args(argv)

    rows = convert(args.csv_file, args.delimiter, args.encoding, args.infer)
    if args.lines:
        for row in rows:
            print(json.dumps(row, ensure_ascii=False))
    else:
        json.dump(list(rows), sys.stdout, ensure_ascii=False, indent=args.indent)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
