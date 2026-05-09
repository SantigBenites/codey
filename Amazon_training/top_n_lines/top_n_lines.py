# Drill 1 — Warm-up: Top N Lines by Frequency
# Difficulty: Easy · Target time: 10 min
# Problem: Given a text file (one entry per line, e.g. usernames), print the top N most-frequent lines and
# their counts, sorted descending. Default N=10
import argparse
from collections import Counter
from pathlib import Path


def top_n_lines(path:Path,n:int = 10):

    if not path.is_file():
        raise FileNotFoundError(path)
    count = Counter()

    if not path.is_file():   
        raise FileNotFoundError
    
    with open(path, "r", errors="replace") as f:
        for line in f:
            count[line.rstrip("\n")] += 1

    
    return count.most_common(n)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path)
    ap.add_argument("-n", type=int, default=10)
    args = ap.parse_args()
    for line, c in top_n_lines(args.path, args.n):
        print(f"{c}\t{line}")
