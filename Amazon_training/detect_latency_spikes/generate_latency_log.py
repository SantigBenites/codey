#!/usr/bin/env python3
"""
Generate a realistic latency log for Drill 17, plus a ground-truth file
listing the anomalies your script should detect.

Run:
    python generate_latency_log.py

Produces:
    requests.log     - one JSON object per line, ~3 hours of traffic
    ground_truth.txt - what your script should find
"""

import json
import random
import statistics
from datetime import datetime, timedelta, timezone
from pathlib import Path

random.seed(42)  # reproducible

START = datetime(2026, 5, 10, 9, 0, 0, tzinfo=timezone.utc)
DURATION_MINUTES = 180  # 3 hours

# Endpoints with their normal characteristics:
#   (rps_mean, latency_mean_ms, latency_stddev_ms)
ENDPOINTS = {
    "/api/health":    (2.0,  5,    1),     # fast and constant
    "/api/checkout":  (0.5,  120,  30),    # slow-ish, real work
    "/api/search":    (1.0,  200,  60),    # slow, naturally variable
    "/api/login":     (0.3,  80,   20),    # moderate
    "/api/rare":      (0.02, 50,   10),    # very low volume — should be ignored
}

# Anomalies to inject: (endpoint, start_minute_offset, duration_min, multiplier)
# These are the windows your script SHOULD find.
ANOMALIES = [
    ("/api/checkout", 45, 3, 5.0),   # 5x spike for 3 minutes around minute 45-48
    ("/api/search",   90, 2, 4.0),   # 4x spike for 2 minutes
    ("/api/login",   140, 1, 6.0),   # brief 6x spike
]

# A subtle distractor: /api/rare gets one slow request at minute 60.
# Should NOT be reported because volume is below threshold (need 10+ req/window).

def in_anomaly_window(endpoint, ts):
    """Return multiplier if ts is in an anomaly window for endpoint, else 1.0."""
    for ep, start_off, dur, mult in ANOMALIES:
        if ep != endpoint:
            continue
        anomaly_start = START + timedelta(minutes=start_off)
        anomaly_end = anomaly_start + timedelta(minutes=dur)
        if anomaly_start <= ts < anomaly_end:
            return mult
    return 1.0

def generate_requests():
    """Yield request dicts in time order."""
    end = START + timedelta(minutes=DURATION_MINUTES)
    for endpoint, (rps, mean, stddev) in ENDPOINTS.items():
        # Generate timestamps via Poisson process: gap = exponential(1/rps)
        t = START
        while t < end:
            gap = random.expovariate(rps)
            t = t + timedelta(seconds=gap)
            if t >= end:
                break
            mult = in_anomaly_window(endpoint, t)
            latency = max(1, int(random.gauss(mean * mult, stddev * mult)))
            status = 200 if random.random() > 0.02 else random.choice([500, 503])
            yield {
                "timestamp": t.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "endpoint": endpoint,
                "latency_ms": latency,
                "status": status,
            }

def main():
    requests = list(generate_requests())
    requests.sort(key=lambda r: r["timestamp"])

    log_path = Path("requests.log")
    with log_path.open("w") as f:
        for i, req in enumerate(requests):
            # Inject a few malformed lines to test error handling
            if i in (137, 4001, 9000):
                f.write("this is not valid json\n")
                continue
            if i == 5500:
                f.write('{"timestamp": "2026-05-10T09:30:00Z", "endpoint": "/api/x"\n')  # truncated
                continue
            f.write(json.dumps(req) + "\n")

    # Compute ground truth: aggregate by (endpoint, minute), find what should fire
    from collections import defaultdict
    buckets = defaultdict(list)
    for r in requests:
        ts = datetime.strptime(r["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        bucket = ts.replace(second=0, tzinfo=timezone.utc)
        buckets[(r["endpoint"], bucket)].append(r["latency_ms"])

    # Per-endpoint p95 history
    endpoint_p95s = defaultdict(list)
    window_p95s = {}
    for (ep, bucket), latencies in buckets.items():
        if not latencies:
            continue
        p95 = sorted(latencies)[int(0.95 * len(latencies))]
        window_p95s[(ep, bucket)] = (p95, len(latencies))
        endpoint_p95s[ep].append(p95)

    baselines = {ep: statistics.median(p95s) for ep, p95s in endpoint_p95s.items()}

    truth_lines = []
    truth_lines.append("Expected anomalies (your script should report these):\n")
    truth_lines.append(f"{'ENDPOINT':<18}{'WINDOW START':<22}{'COUNT':>7}{'P95':>8}{'BASELINE':>10}{'MULT':>7}\n")
    truth_lines.append("-" * 75 + "\n")

    findings = []
    for (ep, bucket), (p95, count) in window_p95s.items():
        baseline = baselines[ep]
        if count < 10:
            continue
        if baseline == 0:
            continue
        mult = p95 / baseline
        if mult > 3.0:
            findings.append((ep, bucket, count, p95, baseline, mult))

    findings.sort(key=lambda x: -x[5])
    for ep, bucket, count, p95, baseline, mult in findings:
        truth_lines.append(
            f"{ep:<18}{bucket.strftime('%Y-%m-%dT%H:%M:%SZ'):<22}"
            f"{count:>7}{p95:>8}{baseline:>10.1f}{mult:>7.2f}\n"
        )

    truth_lines.append("\n")
    truth_lines.append(f"Total log lines written: {len(requests) + 4} (including 4 malformed)\n")
    truth_lines.append(f"Endpoints with computed baselines: {dict((ep, round(b, 1)) for ep, b in baselines.items())}\n")
    truth_lines.append(f"Note: /api/rare should NOT appear (low volume — fewer than 10 req/window).\n")

    Path("ground_truth.txt").write_text("".join(truth_lines))

    print(f"Wrote {log_path} ({log_path.stat().st_size:,} bytes, {len(requests)} valid requests + 4 malformed)")
    print(f"Wrote ground_truth.txt — {len(findings)} anomalies expected")
    print()
    print("First few lines of ground truth:")
    print("".join(truth_lines[:10]))

if __name__ == "__main__":
    main()