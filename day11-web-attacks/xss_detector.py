import re
import datetime

XSS_PATTERNS = [
    r"<script>",
    r"</script>",
    r"onerror=",
    r"onload=",
    r"javascript:"
]

def detect_xss(user_input):
    for pattern in XSS_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            return True
    return False

def log_attack(input_data):
    with open("xss_logs.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | XSS Attempt: {input_data}\n")

if __name__ == "__main__":
    user_input = input("Enter comment input: ")

    if detect_xss(user_input):
        print("[!] Possible XSS detected!")
        log_attack(user_input)
    else:
        print("[+] Input seems safe.")
