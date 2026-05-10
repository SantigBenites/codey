import re
from pathlib import Path

log_pattern = re.compile(
    r'(?P<ip>\S+) - (?P<user>\S+) \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d+) (?P<size>\d+) '
    r'"(?P<referrer>[^"]*)" "(?P<agent>[^"]*)"'
)

file_path = Path("./acess_log")

with open(file_path) as df:
    for line in df:
        match = log_pattern.match(line)
        if match:
            data = match.groupdict()

            ip = data["ip"]
            time = data["time"]
            browser = data["agent"]

            print("IP:", ip)
            print("Time:", time)
            print("Browser:", browser)
            print("---")