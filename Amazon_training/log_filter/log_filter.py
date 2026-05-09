# Drill 2 — Log Filter by Time Window
# Difficulty: Easy-Medium · Target time: 15 min
# Problem: Given a log file with lines like 2026-05-08T14:23:11Z INFO ..., print only entries between
# two ISO timestamps passed as arguments. Inclusive on both ends.
import argparse, sys, re
from pathlib import Path
from datetime import datetime, timezone

TS_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)")

def parse_iso(s: str) -> datetime:
    # Tolerate trailing Z (Python <3.11 doesn't accept it natively)
    s = s.replace("Z", "+00:00")
    return datetime.fromisoformat(s).astimezone(timezone.utc)

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path)
    ap.add_argument("start")
    ap.add_argument("end")
    args = ap.parse_args()

    try:
        start = parse_iso(args.start)
        end = parse_iso(args.end)
    except ValueError as e:
        print(f"bad timestamp: {e}", file=sys.stderr)
        return 2


    with open(args.path, mode="r", encoding="utf8", errors="replace") as f:

        for line in f:
            if not line.strip():
                continue
            m = TS_RE.match(line)
            if not m:
                print(f"ERROR: Malformed line {line}", file=sys.stderr, end="")
                continue
            try:
                ts = parse_iso(m.group(1))
            except ValueError:
                print(f"ERROR: Malformed time {line}", file=sys.stderr, end="")
                continue
            if start <= ts <= end:
                print(line, end="")

    return 0




if __name__ == "__main__":
    main()