import re
from collections import Counter

failed_ips = Counter()

with open("sample_logs.txt", "r") as f:
     for line in f:
        if "failed" in line:
           ip = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
           if ip:
             failed_ips[ip[0]] += 1

print("Failed login attempts by IP:")
for ip, count in failed_ips.items():
      print(f"{ip} -> {count} attempts")

print("\nSuspicious IPs (>=3 failed attempts):")
for ip, count in failed_ips.items():
   if count >= 3:
     print(f"{ip} is suspicious")

