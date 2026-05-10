import argparse, logging, sys, yaml,subprocess
from pathlib import Path
from collections import defaultdict


logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("coordinator")

def load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text()) or {}

def restart_service(service_name:str):

    cmd = ["systectl", "restart", service_name]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        log.error(f"Failed to run command: {' '.join(cmd)}")
        return False

    return True


def main():


    ap = argparse.ArgumentParser()
    ap.add_argument("file",type=Path)
    ap.add_argument("service",type=str)


    args = ap.parse_args()

    try:
        data = load_yaml(args.file)
    except (FileNotFoundError, yaml.YAMLError, OSError):
        log.error(f"Failure parsing yaml file {args.file}")
        return 2
    
    dependacies = defaultdict(list)
    data = data["services"]
    for service in data.keys():

        depends_on = data[service]["depends_on"]
        for dep in depends_on:
            dependacies[dep].append(service)

    # Step 1: find which services need to restart (reachable from target via reverse-dep graph)
    reachable = set()
    stack = [args.service]
    while stack:
        s = stack.pop()
        if s in reachable:
            continue
        reachable.add(s)
        stack.extend(dependacies[s])    # dependents


    # Step 2: topo sort restricted to `reachable`
    # Build forward deps for sorting (we need "X depends on Y" to know order)
    forward = {s: [d for d in data[s]["depends_on"] if d in reachable] for s in reachable}

    order = []
    ready = [s for s in reachable if not forward[s]]   # nodes with no remaining deps
    while ready:
        s = ready.pop(0)
        order.append(s)
        for other in reachable:
            if s in forward[other]:
                forward[other].remove(s)
                if not forward[other]:
                    ready.append(other)
    
    if len(order) != len(reachable):
        log.error("circular dependency detected")
        return 2


if __name__ == "__main__":
    sys.exit(main())