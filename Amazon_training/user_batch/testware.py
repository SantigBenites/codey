#!/usr/bin/env python3
"""
Mock user-management harness for Drill 11.

There are two ways to use this:

  (A) DRY-RUN MODE in your own script
      Pass --dry-run and have your script print what it WOULD do
      instead of calling subprocess. Cleanest for an interview answer.
      No state file needed.

  (B) FAKE-COMMAND MODE for end-to-end testing
      Run this harness once: it creates fake `useradd`, `usermod`, `userdel`
      shims in ./fake_bin/ that update a JSON state file instead of touching
      the system. Then run your script with PATH=./fake_bin:$PATH so the
      shims intercept the calls.

      $ python mock_user_harness.py setup
      $ PATH=./fake_bin:$PATH python batch_users.py users.csv
      $ python mock_user_harness.py show     # see resulting state
      $ python mock_user_harness.py reset    # reset for re-run

This harness exists because you cannot test user-management scripts against
a real system safely — and "I tested it on production" is the wrong answer
in an interview about ops work.
"""

import json
import os
import shutil
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FAKE_BIN = ROOT / "fake_bin"
STATE_FILE = ROOT / "fake_users_state.json"

SHIM_TEMPLATE = """\
#!/usr/bin/env python3
# Fake {cmd} — updates {state} instead of the real system.
import json, sys
from pathlib import Path

STATE = Path({state!r})

def load():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {{"users": {{}}}}

def save(s):
    STATE.write_text(json.dumps(s, indent=2, sort_keys=True))

def main():
    state = load()
    args = sys.argv[1:]
    cmd = {cmd!r}

    # Real {cmd} has many flags; we parse only what the drill needs.
    # Username is the LAST positional argument.
    user = args[-1] if args else None
    if not user or user.startswith("-"):
        print(f"{{cmd}}: missing username", file=sys.stderr)
        sys.exit(2)

    if cmd == "useradd":
        if user in state["users"]:
            print(f"useradd: user '{{user}}' already exists", file=sys.stderr)
            sys.exit(9)  # real useradd exit code for "user already exists"
        # Pull -G group if present
        group = None
        for i, a in enumerate(args[:-1]):
            if a == "-G" and i + 1 < len(args) - 1:
                group = args[i+1]
        state["users"][user] = {{"group": group, "disabled": False}}

    elif cmd == "usermod":
        if user not in state["users"]:
            print(f"usermod: user '{{user}}' does not exist", file=sys.stderr)
            sys.exit(6)
        # Detect -L (lock = disable) and -U (unlock)
        if "-L" in args:
            state["users"][user]["disabled"] = True
        if "-U" in args:
            state["users"][user]["disabled"] = False

    elif cmd == "userdel":
        if user not in state["users"]:
            print(f"userdel: user '{{user}}' does not exist", file=sys.stderr)
            sys.exit(6)
        del state["users"][user]

    save(state)
    sys.exit(0)

if __name__ == "__main__":
    main()
"""


def setup():
    FAKE_BIN.mkdir(exist_ok=True)
    for cmd in ("useradd", "usermod", "userdel"):
        path = FAKE_BIN / cmd
        path.write_text(SHIM_TEMPLATE.format(cmd=cmd, state=str(STATE_FILE)))
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    if not STATE_FILE.exists():
        STATE_FILE.write_text(json.dumps({"users": {
            # Pre-populate users that the CSV's `disable` and `delete` rows
            # expect to already exist. This makes idempotency testing realistic.
            "ed":    {"group": "developers", "disabled": False},
            "fiona": {"group": "ops",        "disabled": False},
            "greg":  {"group": "developers", "disabled": False},
            "hank":  {"group": "ops",        "disabled": False},
        }}, indent=2, sort_keys=True))
    print(f"Fake commands installed in: {FAKE_BIN}")
    print(f"State file: {STATE_FILE}")
    print()
    print("Run your script with:")
    print(f"  PATH={FAKE_BIN}:$PATH python batch_users.py users.csv")
    print()
    print("Then check the result with:")
    print("  python mock_user_harness.py show")


def show():
    if not STATE_FILE.exists():
        print("No state file. Run `setup` first.")
        return
    print(STATE_FILE.read_text())


def reset():
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    if FAKE_BIN.exists():
        shutil.rmtree(FAKE_BIN)
    print("Cleaned up fake_bin/ and state file.")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("setup", "show", "reset"):
        print(__doc__)
        sys.exit(1)
    {"setup": setup, "show": show, "reset": reset}[sys.argv[1]]()


if __name__ == "__main__":
    main()