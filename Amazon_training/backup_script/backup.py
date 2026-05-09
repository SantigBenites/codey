import argparse, sys, subprocess, gzip, time, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-7s %(message)s")
log = logging.getLogger("backup")

KEEP = 7

def make_archive(src: Path, dst: Path) -> bool:
    """tar -czf with atomic rename. Returns True on success."""
    partial = Path(str(dst) + ".partial")
    cmd = ["tar", "-czf", str(partial) , "-C", str(src.parent), src.name]
    log.info(f"Tar process for dir {src.name}")
    try:
        subprocess.run(cmd,check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        log.error(f"Tar process failed for dir {src.name}")
        partial.unlink(missing_ok=True)
        return False
    partial.rename(dst.name)
    return True
    

def verify_gzip(path: Path) -> bool:
    """Read entire archive — proves CRC and decompression work."""
    log.info(f"Verifying zip {path.name}")
    try:
        with gzip.open(path, "rb") as f:
            while f.read(1024*1024):
                pass
    except (FileNotFoundError, OSError):
        log.error(f"Malformed zip file {path.name}")
        return False
    return True



def prune(dst_dir: Path, keep: int) -> None:
    """Keep the `keep` most-recent backup-*.tar.gz, delete older."""
    sorted_files = sorted(
        dst_dir.glob("backup-*.tar.gz"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for file in sorted_files[keep:]:
        log.info(f"Pruning {file.name}")
        file.unlink()



def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, type=Path)
    ap.add_argument("--dst", required=True, type=Path)
    ap.add_argument("--keep", type=int, default=KEEP)
    args = ap.parse_args()

    if not args.src.is_dir():
        log.error("src is not a directory: %s", args.src)
        return 2
    args.dst.mkdir(parents=True, exist_ok=True)

    # Clean up stale partials from previous crashed runs
    for stale in args.dst.glob("*.partial"):
        log.warning("removing stale partial: %s", stale.name)
        stale.unlink()

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    archive = args.dst / f"backup-{stamp}.tar.gz"

    if not make_archive(args.src, archive):
        return 2
    if not verify_gzip(archive):
        archive.unlink(missing_ok=True)
        return 2

    prune(args.dst, args.keep)
    log.info("OK — %s (%.1f MB)", archive.name,
             archive.stat().st_size / 1e6)
    return 0

if __name__ == "__main__":
    sys.exit(main())