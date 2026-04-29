#!/usr/bin/env python3
"""script.py — one-line description.
Usage: script.py INPUT [--flag VALUE]
"""
import argparse
import logging
import sys
from pathlib import Path
log = logging.getLogger(__name__)
# root:x:0:0:root:/root:/bin/ash


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path)
    ap.add_argument("--verbose", action="store_true")
    return ap.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )

    with open(args.input) as df:

        lines = [line.rstrip() for line in df][1:]

        for line in lines:

            if not line or line[0] == "#":
                log.warning("commented line")
                continue
            if len(line) < 7:
                log.error("malformed line")  # malformed line
                return -1

            line = line.split(":")
            user = line[0]
            entry_point = line[-1]
            home = line[-2]

            print(f"User:{user} Home:{home} Entry:{entry_point}")

    return 0

if __name__ == "__main__":
    sys.exit(main())