import argparse, logging, sys, subprocess, csv, re
from pathlib import Path
from email.utils import parseaddr
logging.basicConfig(level=logging.INFO,format="")
log = logging.getLogger("batch_users")

USERNAME_RE = re.compile(r"^[a-z_][a-z0-9_-]{0,31}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ALLOWED_GROUPS = {"developers", "ops", "admin"}
ALLOWED_ACTIONS = {"create", "disable", "delete"}

def run_subprocess(cmd: list[str]) -> bool:
    """Run cmd. Log failures with stderr. Return True on success."""
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error("subprocess failed: %s | exit=%d | stderr=%s",
                      " ".join(cmd), e.returncode,
                      e.stderr.decode("utf-8", "replace").strip())
        return False
    except FileNotFoundError:
        logging.error("command not found: %s", cmd[0])
        return False

def useradd(user, group, dry_run):    return run_subprocess(["useradd", "-m", "-G", group, user], dry_run)
def userdel(user, dry_run):           return run_subprocess(["userdel", "-r", user], dry_run)
def user_disable(user, dry_run):      return run_subprocess(["usermod", "-L", user], dry_run)

def validate(row, lineno):
    """Return (ok, error_msg)."""
    user = row.get("username", "").strip()
    email = row.get("email", "").strip()
    group = row.get("group", "").strip()
    action = row.get("action", "").strip()
    if not USERNAME_RE.match(user):
        return False, f"line {lineno}: invalid username '{user}'"
    if not EMAIL_RE.match(email):
        return False, f"line {lineno}: invalid email '{email}'"
    if group not in ALLOWED_GROUPS:
        return False, f"line {lineno}: invalid group '{group}'"
    if action not in ALLOWED_ACTIONS:
        return False, f"line {lineno}: invalid action '{action}'"
    return True, None

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.file.is_file():
        log.error("file not found: %s", args.file); return 2

    total = ok = failed = 0
    with open(args.file, encoding="utf8") as f:
        # Strip comment lines BEFORE handing to csv module
        clean = (l for l in f if not l.lstrip().startswith("#") and l.strip())
        reader = csv.DictReader(clean)
        for lineno, row in enumerate(reader, start=2):
            total += 1
            valid, err = validate(row, lineno)
            if not valid:
                log.error(err); failed += 1; continue

            user = row["username"].strip()
            group = row["group"].strip()
            action = row["action"].strip()

            if action == "create":
                success = useradd(user, group, args.dry_run)
            elif action == "disable":
                success = user_disable(user, args.dry_run)
            elif action == "delete":
                success = userdel(user, args.dry_run)

            if success:
                ok += 1
                log.info("line=%d user=%s action=%s result=ok", lineno, user, action)
            else:
                failed += 1

    log.info("done: total=%d ok=%d failed=%d", total, ok, failed)
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())