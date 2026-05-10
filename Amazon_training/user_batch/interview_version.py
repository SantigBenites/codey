import argparse, csv, logging, re, subprocess, sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
USERNAME = re.compile(r"^[a-z_][a-z0-9_-]{0,31}$")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def run(cmd, dry):
    if dry:
        logging.info("would run: %s", " ".join(cmd))
        return True
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error("%s failed: %s", cmd[0], e.stderr.decode().strip())
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    failed = ok = 0
    with open(args.file) as f:
        reader = csv.DictReader(l for l in f if l.strip() and not l.lstrip().startswith("#"))
        for n, row in enumerate(reader, 2):
            user, email, group, action = (row[k].strip() for k in ("username","email","group","action"))
            if not USERNAME.match(user) or not EMAIL.match(email) or action not in {"create","disable","delete"}:
                logging.error("line %d: invalid row %s", n, row); failed += 1; continue

            cmd = {
                "create":  ["useradd", "-m", "-G", group, user],
                "disable": ["usermod", "-L", user],
                "delete":  ["userdel", "-r", user],
            }[action]

            (ok := ok + 1) if run(cmd, args.dry_run) else (failed := failed + 1)

    logging.info("done: %d ok, %d failed", ok, failed)
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())