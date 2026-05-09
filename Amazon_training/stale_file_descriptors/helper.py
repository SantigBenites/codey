#!/usr/bin/env python3
"""
Drill 5 testware — spawn processes that hold deleted files open.

Run this in one terminal:
    python setup_drill5_test.py

It will create several helper processes, each holding a deleted file open
with a known size. Leave it running. In another terminal, run your drill
script. You should see entries for the helper PIDs printed below.

Press Ctrl-C here to clean everything up.
"""

import os
import sys
import time
import signal
import tempfile
import subprocess
from pathlib import Path

# Sizes chosen to be distinctive — easy to spot in your output.
HELPERS = [
    ("tiny",   1024),               # 1 KB
    ("small",  64 * 1024),          # 64 KB
    ("medium", 5 * 1024 * 1024),    # 5 MB
    ("large",  50 * 1024 * 1024),   # 50 MB
]

# Helper script: creates a file, opens it, deletes the path, then sleeps.
# The file is gone from the filesystem but the inode lives on as long as
# this process holds the fd open.
HELPER_SOURCE = r'''
import os, sys, time, signal
path, size = sys.argv[1], int(sys.argv[2])
# Create and fill the file
with open(path, "wb") as f:
    f.write(b"X" * size)
# Open it again and KEEP this handle
fd = os.open(path, os.O_RDONLY)
# Now unlink — file is "deleted" from the filesystem but our fd is still alive
os.unlink(path)
# Ignore SIGTERM gracefully so the parent can clean us up
def quit(*a):
    os.close(fd)
    sys.exit(0)
signal.signal(signal.SIGTERM, quit)
signal.signal(signal.SIGINT, quit)
# Hang forever (or until killed)
while True:
    time.sleep(60)
'''

def main():
    tmpdir = Path(tempfile.mkdtemp(prefix="drill5_"))
    helper_script = tmpdir / "helper.py"
    helper_script.write_text(HELPER_SOURCE)

    procs = []
    print(f"Spawning {len(HELPERS)} helpers, each holding a deleted file open.")
    print(f"Working dir: {tmpdir}")
    print()

    for name, size in HELPERS:
        target = tmpdir / f"{name}.dat"
        p = subprocess.Popen(
            [sys.executable, str(helper_script), str(target), str(size)]
        )
        procs.append((p, name, size, target))
        time.sleep(0.2)  # let it create+unlink before we report

    print(f"{'PID':<8}{'NAME':<10}{'SIZE':>12}  ORIGINAL PATH (now deleted)")
    print("-" * 70)
    for p, name, size, target in procs:
        print(f"{p.pid:<8}{name:<10}{size:>12,}  {target}")
    print()
    print("Your drill script should find ALL of these PIDs with matching sizes.")
    print("Press Ctrl-C to clean up.")
    print()

    def cleanup(*_):
        print("\nCleaning up helpers...")
        for p, *_ in procs:
            try:
                p.terminate()
            except Exception:
                pass
        for p, *_ in procs:
            try:
                p.wait(timeout=2)
            except Exception:
                p.kill()
        try:
            helper_script.unlink()
            tmpdir.rmdir()
        except Exception:
            pass
        print("Done.")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # Idle until killed
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()