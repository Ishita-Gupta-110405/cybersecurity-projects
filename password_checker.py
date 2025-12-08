import re
import logging

# Configure logging
logging.basicConfig(
    filename="password_checker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def check_password_strength(password):
    score = 0
    suggestions = []

    # Rules
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add at least one lowercase letter.")

    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Add at least one number.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("Add at least one special character.")

    # Evaluate strength
    if score == 5:
        strength = "Very Strong"
    elif score == 4:
        strength = "Strong"
    elif score == 3:
        strength = "Medium"
    else:
        strength = "Weak"

    logging.info(f"Password checked. Strength: {strength}")

    return strength, suggestions


if __name__ == "__main__":
    pwd = input("Enter password to check: ")
    strength, suggestions = check_password_strength(pwd)

    print(f"\nPassword Strength: {strength}")
    if suggestions:
        print("\nSuggestions:")
        for s in suggestions:
            print("-", s)

