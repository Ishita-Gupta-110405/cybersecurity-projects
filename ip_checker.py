import requests
import json
import re
import datetime

API_KEY = "https://api.ipinfo.io/lite/8.8.8.8?token=e7829fc1e3642d"
BASE_URL = "https://ipinfo.io/"

# Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


def validate_ip(ip):
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(ip_pattern, ip)


def get_ip_info(ip):
    url = f"{BASE_URL}{ip}/json?token={API_KEY}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


def score_ip(info):
    score = 0
    reasons = []

    # 1. Hosting provider?
    if "org" in info and any(x in info["org"].lower() for x in ["amazon", "google", "digitalocean", "ovh", "azure", "linode"]):
        score += 20
        reasons.append("Hosting/Cloud Provider")

    # 2. Country risk indicator
    risky_countries = ["RU", "CN", "IR", "KP"]
    if info.get("country") in risky_countries:
        score += 20
        reasons.append("High-risk country")

    # 3. If "privacy" field exists → VPN / proxy
    if info.get("privacy"):
        p = info["privacy"]
        if p.get("vpn"):
            score += 30
            reasons.append("VPN detected")
        if p.get("proxy"):
            score += 25
            reasons.append("Proxy detected")
        if p.get("tor"):
            score += 40
            reasons.append("Tor exit node detected")

    return score, reasons


def color_for_score(score):
    if score < 20:
        return GREEN, "Low Risk"
    elif score < 50:
        return YELLOW, "Medium Risk"
    else:
        return RED, "High Risk"


def save_report(ip, data):
    filename = f"ip_report_{ip}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\nReport saved as: {filename}")


def main():
    ip = input("Enter IP address: ")

    if not validate_ip(ip):
        print(RED + "Invalid IP format." + RESET)
        return

    print("\nFetching data...")

    info = get_ip_info(ip)

    if "error" in info:
        print(RED + "Error: " + info["error"] + RESET)
        return

    print("\n--- IP Information ---")
    for key, value in info.items():
        print(f"{key}: {value}")

    # Calculate score
    score, reasons = score_ip(info)
    color, label = color_for_score(score)

    print("\n--- Reputation Score ---")
    print(color + f"Score: {score} / 100  →  {label}" + RESET)

    if reasons:
        print("Reasons:")
        for r in reasons:
            print(" -", r)
    else:
        print("No suspicious indicators found.")

    save_report(ip, {**info, "score": score, "risk_label": label, "reasons": reasons})


if __name__ == "__main__":
    main()

