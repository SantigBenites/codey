from pathlib import Path
import time

with open(Path("test.log")) as f:    
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.5)
            continue
        print(line)