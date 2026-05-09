import os,sys
import logging
from pathlib import Path 

PROC = Path("/proc")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(message)s")
log = logging.getLogger("pid_logger")

def cmdline(pid: str) -> str:
    try:
        raw = (PROC / pid / "cmdline").read_bytes()
        # cmdline uses NUL separators; first token is the binary
        parts = raw.split(b"\x00")
        return (parts[0].decode("utf-8", "replace")
        if parts else "?") or "?"
    except (OSError, IndexError):
        return "?"

def scan_pid(pid:str):
    """Return list of {fd, path, size} for deleted files held by pid."""
    fd_dir = PROC / pid / "fd"
    found = []
    try:
        fds = os.listdir(fd_dir)
    except (PermissionError, FileNotFoundError):
        return found
    
    for fd in fds:
        link = fd_dir / fd
        try:
            target = os.readlink(link)
        except (FileNotFoundError, OSError) as e:
            continue

        try:
            st = os.stat(link)
        except (FileNotFoundError, PermissionError):
            continue
        if not target.endswith(" (deleted)"):
            continue
        found.append({"fd": fd, "path": target[:-len(" (deleted)")], "size": st.st_size})
        return found


def main():

    if not PROC.is_dir():
        log.error("Not running on linux")
        return 2
    
    print(f"{'PID':>7} {'SIZE(MB)':>10} {'CMD':<20} PATH")
    total_bytes = 0

    for entry in PROC.iterdir():
        if not entry.name.isdigit():
            continue
        deleted = scan_pid(entry.name)
        if not deleted:
            continue
        cmd = cmdline(entry.name)

        for d in scan_pid(entry.name):

            print(f"{entry.name:>7} "
                  f"{d['size']/1e6:>10.1f} "
                  f"{cmd[:20]:<20} "
                  f"{d['path']}")
            total_bytes += d["size"]

    print(f"\n# total reclaimable if owners restarted: {total_bytes/1e9:.2f} GB")
    return 0


if __name__ == "__main__":
    sys.exit(main())