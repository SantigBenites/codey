import time

log_path = "test.log"

i = 0
while True:
    i += 1
    with open(log_path, "a") as f:
        f.write(f"2026-04-22 12:00:{10+i:02d} INFO New log line {i}\n")
    time.sleep(1)
