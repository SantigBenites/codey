import argparse
import fcntl
import subprocess
import logging
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

COMPRESS_DAYS = 3
DELETE_DAYS = 30
LOCK_PATH = "/var/run/rotate_logs.lock"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("rotate_logs")


def older_than(path: Path, days:int) -> bool:

    age_seconds = time.time() - path.stat().st_mtime
    return age_seconds > days * 86400


def compress_tar(path: Path) -> bool:
    """tar+gzip path -> path.tar.gz atomically, then remove original."""
    partial = path.parent / (path.name + ".tar.gz.partial")
    final = path.parent / (path.name + ".tar.gz")

    # -C cd's into the parent so the archive stores just "foo.log",
    # not "/var/log/myapp/foo.log". Cleaner on extraction.
    cmd = [
        "tar", "-czf", str(partial),
        "-C", str(path.parent),
        "--", path.name,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        partial.replace(final)   # atomic rename
        path.unlink()            # remove original only after rename succeeds
        log.info(f"Compressed {path.name} -> {final.name}")
        return True
    except subprocess.CalledProcessError as e:
        partial.unlink(missing_ok=True)
        log.error(f"tar failed for {path.name}: {e.stderr.decode().strip()}")
        return False
    except Exception as e:
        partial.unlink(missing_ok=True)
        log.error(f"Failed to compress {path.name}: {e}")
        return False

def compress(path:Path):

    try:
        subprocess.run(
            ["gzip", "-f", "--", str(path)],
            check=True,
            capture_output=True,
        )
        log.info(f"Compressed {path.name}")
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to compress {path.name}: {e.stderr.decode().strip()}")
        return False
        

def rotate(log_dir : Path):

    for log in log_dir.glob("*.log"):

        try:
            if older_than(log, COMPRESS_DAYS):
                compress(log)
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.error(f"Failed to compress {log}: {e}")


    for tar in log_dir.glob("*.tar.gz"):
        try:
            if older_than(tar, DELETE_DAYS):
                tar.unlink()
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.error(f"Failed to delete {tar}: {e}")
            





def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("log_dir", type=str)
    args = ap.parse_args()

    # Acquire exclusive lock; exit cleanly if another run is in progress.
    lock_file = open(LOCK_PATH, "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        logging.info("Another run is in progress; exiting")
        return 0
    
    try:
        rotate(args.log_dir)
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()
    return 0



if __name__== "__main__":
    sys.exit(main())