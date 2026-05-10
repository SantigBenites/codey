import argparse, configparser, logging, sys, yaml
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("diff_configs")

def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key))
        else:
            out[key] = v
    return out

def diff(a, b):
    a, b = flatten(a), flatten(b)
    only_a = {k: a[k] for k in a.keys() - b.keys()}
    only_b = {k: b[k] for k in b.keys() - a.keys()}
    changed = {k: (a[k], b[k]) for k in a.keys() & b.keys() if a[k] != b[k]}
    return only_a, only_b, changed

def load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text()) or {}

def load_ini(p: Path) -> dict:
    parser = configparser.ConfigParser()
    if not parser.read(p):
        raise OSError(f"could not read {p}")
    return {s: dict(parser[s]) for s in parser.sections()}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file1", type=Path)
    ap.add_argument("file2", type=Path)
    args = ap.parse_args()

    if args.file1.suffix.lower() != args.file2.suffix.lower():
        log.error("file extensions differ: %s vs %s", args.file1.suffix, args.file2.suffix)
        return 2

    suffix = args.file1.suffix.lower()
    try:
        if suffix in (".yml", ".yaml"):
            data_a, data_b = load_yaml(args.file1), load_yaml(args.file2)
        elif suffix == ".ini":
            data_a, data_b = load_ini(args.file1), load_ini(args.file2)
        else:
            log.error("unsupported file type: %s", suffix)
            return 2
    except (yaml.YAMLError, configparser.Error, OSError) as e:
        log.error("parse failure: %s", e)
        return 2

    only_a, only_b, changed = diff(data_a, data_b)
    for k in sorted(only_a):  print(f"- {k}: {only_a[k]}")
    for k in sorted(only_b):  print(f"+ {k}: {only_b[k]}")
    for k in sorted(changed):
        old, new = changed[k]
        print(f"~ {k}: {old} -> {new}")

    return 0 if not (only_a or only_b or changed) else 1

if __name__ == "__main__":
    sys.exit(main())