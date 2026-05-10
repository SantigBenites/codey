import argparse, json, logging, sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("latency_spikes")

def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", type=Path)
    args = ap.parse_args()

    if not args.file.is_file():
        log.error("file not found: %s", args.file)
        return 2

    buckets = defaultdict(list)
    malformed = 0
    with open(args.file) as f:
        for line in f:
            try:
                r = json.loads(line)
                minute = parse_ts(r["timestamp"]).replace(second=0, microsecond=0)
                buckets[(r["endpoint"], minute)].append(r["latency_ms"])
            except (json.JSONDecodeError, KeyError, ValueError):
                malformed += 1

    if not buckets:
        log.error("no usable data (%d malformed lines)", malformed)
        return 2

    window_p95 = {}
    endpoint_p95s = defaultdict(list)
    for (ep, minute), lats in buckets.items():
        p95 = sorted(lats)[int(0.95 * len(lats))]
        window_p95[(ep, minute)] = (p95, len(lats))
        endpoint_p95s[ep].append(p95)

    baselines = {ep: median(p95s) for ep, p95s in endpoint_p95s.items()}

    findings = []
    for (ep, minute), (p95, count) in window_p95.items():
        if count < 10:
            continue
        baseline = baselines[ep]
        if baseline == 0:
            continue
        mult = p95 / baseline
        if mult > 3.0:
            findings.append((ep, minute, count, p95, baseline, mult))

    findings.sort(key=lambda x: -x[5])

    print(f"{'ENDPOINT':<18}{'WINDOW START':<22}{'COUNT':>7}{'P95':>8}{'BASELINE':>10}{'MULT':>7}")
    for ep, minute, count, p95, baseline, mult in findings:
        print(f"{ep:<18}{minute.strftime('%Y-%m-%dT%H:%M:%SZ'):<22}"
              f"{count:>7}{p95:>8}{baseline:>10.1f}{mult:>7.2f}")

    if malformed:
        log.warning("skipped %d malformed lines", malformed)

    return 1 if findings else 0

if __name__ == "__main__":
    sys.exit(main())