import re
import datetime

SQLI_PATTERNS = [
    r"(?i)or\s+.*=.*",        # OR anything = anything
    r"(?i)'--",               # comment-based bypass
    r"(?i)union\s+select",
    r"(?i)drop\s+table",
    r"(?i)insert\s+into",
    r"(?i)'\s+or\s+'",        # ' OR '
]


def detect_sqli(user_input):
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, user_input):
            return True
    return False

def log_attack(input_data):
    with open("sqli_logs.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | SQLi Attempt: {input_data}\n")

if __name__ == "__main__":
    user_input = input("Enter username/password input: ")

    if detect_sqli(user_input):
        print("[!] Possible SQL Injection detected!")
        log_attack(user_input)
    else:
        print("[+] Input seems safe.")
