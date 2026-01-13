import re

print("=== Password Strength Checker ===")

password = input("Enter a password: ")

score = 0

if len(password) >= 8:
    score += 1

if re.search(r"[0-9]", password):
    score += 1

if re.search(r"[A-Z]", password):
    score += 1

if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
    score += 1

print("\nScore:", score, "/ 4")

if score == 4:
    print("✅ Strong password")
elif score == 3:
    print("🟡 Medium password")
else:
    print("❌ Weak password")

