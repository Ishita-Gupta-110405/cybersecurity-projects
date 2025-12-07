import requests
import json
import re
import datetime
import csv
from termcolor import colored

API_KEY = "YOUR_API_KEY"   # replace this with your IPinfo token
BASE_URL = "https://ipinfo.io/"

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

def score_ip(data):
    score = 0

    if "bogon" in data:
        score += 50
    if data.get("country") in ["CN", "RU", "IR", "KP"]:
        score += 10
    if data.get("privacy", {}).get("vpn"):
        score += 20
    if data.get("privacy", {}).get("proxy"):
        score += 20

    if score < 20:
        return score, colored("LOW RISK", "green")
    elif score < 50:
        return score, colored("MEDIUM RISK", "yellow")
    else:
        return score, colored("HIGH RISK", "red")

def save_csv(results):
    filename = f"ip_report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IP", "City", "Region", "Country", "Org", "Score", "Risk"])
        for r in results:
            writer.writerow(r)
    print(colored(f"\nCSV Export saved as {filename}", "cyan"))

def scan_single():
    ip = input("Enter IP: ")
    if not validate_ip(ip):
        print(colored("Invalid IP!", "red"))
        return

    info = get_ip_info(ip)
    score, risk = score_ip(info)

    print("\n--- IP REPORT ---")
    print("IP:", ip)
    print("Location:", info.get("city"), info.get("country"))
    print("Org:", info.get("org"))
    print("Risk Score:", score)
    print("Risk Level:", risk)

def scan_bulk():
    file_path = input("Enter file path: ")
    try:
        with open(file_path, "r") as f:
            ips = [line.strip() for line in f.readlines()]
    except:
        print(colored("File not found!", "red"))
        return

    results = []

    for ip in ips:
        if not validate_ip(ip):
            print(colored(f"Skipping invalid IP: {ip}", "yellow"))
            continue

        info = get_ip_info(ip)
        score, risk = score_ip(info)

        results.append([
            ip,
            info.get("city"),
            info.get("region"),
            info.get("country"),
            info.get("org"),
            score,
            risk,
        ])

        print(colored(f"Scanned: {ip} | Score: {score}", "green"))

    save_csv(results)

if __name__ == "__main__":
    print("\n1. Single IP Scan")
    print("2. Bulk Scan (from file)")
    choice = input("Choose: ")

    if choice == "1":
        scan_single()
    elif choice == "2":
        scan_bulk()
    else:
        print(colored("Invalid choice", "red"))
