IP Reputation Scanner (Beginner Security Project)

A Python tool to analyze IP addresses using the IPinfo API.
Supports risk scoring, color-coded CLI output, bulk IP scanning, and CSV reporting.

 Features

Validate IPv4 addresses

Fetch geolocation, ISP, VPN/proxy info

Compute a risk score (0–100)

Categorize results → Low / Medium / High Risk

Bulk scan from file

Export results as CSV

Colorized terminal output

 Example Usage
Single scan:
python3 ip_reputation_pro.py
Choose: 1
Enter IP: 8.8.8.8

Bulk scan:
python3 ip_reputation_pro.py
Choose: 2
Enter file path: ips.txt

Example output:
Scanned: 8.8.8.8 | Score: 10
CSV Export saved as ip_report_2025-01-12_21-18-33.csv

 Requirements
pip install requests termcolor

 CSV Format

| IP | City | Region | Country | Org | Score | Risk |
