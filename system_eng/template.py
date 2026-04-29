#! /usr/bin/env python3

"""
Comments

"""

import argparse
import logging
import sys
from pathlib import Path


log = logging.getlogger(__name__)


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("-v","--verbose", action="store_true")
    return ap.parse_args()

def work():
    # return 0 on sucess, non-zero on failure
    return

def main() -> int:
    args = parse_args()
    logging.basicConfig(
                level=logging.DEBUG if args.verbose else logging.INFO,
                format="%(asctime)s %(levelname)s %(message)s",
                stream=sys.stderr,
        )

    if not args:
        print("input not found")
        return 2
    
    return work()