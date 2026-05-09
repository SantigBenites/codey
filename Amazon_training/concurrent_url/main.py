import argparse, sys, time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from socket import timeout as SocketTimeout
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

TIMEOUT = 10
MAX_THREADS = 10

def check(url:str):
    start = time.monotonic()

    req = Request(url=url,method="HEAD",headers={"User-Agent": "health-check/1.0"})
    try: 
        with urlopen(req,timeout=TIMEOUT) as r:
            status, err = r.status , None
    except HTTPError as e:
        status, err = e.code, None
    except (URLError, SocketTimeout, ConnectionError) as e:
        status, err = None, type(e).__name__
    except Exception as e:
        status, err = None, f"unexpected:{type(e).__name__}"
    
    elapsed_ms = (time.monotonic() - start) * 1000
    return {"url": url, "status": status,"ms": elapsed_ms, "err": err}

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("max_threads",type=int)
    ap.add_argument("input_file",type=Path)

    args = ap.parse_args()

    with open(args.input_file,"r",encoding="utf8") as f :

        urls = []
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)

    failed = 0
    with ThreadPoolExecutor(max_workers=args.max_threads) as pool:

        futures = {pool.submit(check,u): u for u in urls}

        for fut in as_completed(futures):
            
            r = fut.result()
            shown = r["status"] if r["status"] else r["err"]
            print(f"{str(shown):<8}{r['ms']:<10.0f}{r['url']}")
            if r["status"] is None or r["status"] >= 400:
                failed += 1

    
    return 0 if failed == 0 else 2

if __name__ == "__main__":
    sys.exit(main())