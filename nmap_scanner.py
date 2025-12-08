import os
import subprocess
import datetime
import re

# ----------------------------------
# Terminal Colors (ANSI Escape Codes)
# ----------------------------------
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# -------------------------
# Create log directory
# -------------------------
LOG_DIR = "scan_logs"
os.makedirs(LOG_DIR, exist_ok=True)

# -------------------------
# Extract open ports
# -------------------------
def extract_open_ports(nmap_output):
    open_ports = re.findall(r"(\d+/tcp)\s+open\s+([\w-]+)", nmap_output)
    return open_ports

# -------------------------
# Save results to log file
# -------------------------
def save_log(target, command, output):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{LOG_DIR}/scan_{timestamp}.txt"

    open_ports = extract_open_ports(output)

    with open(filename, "w") as f:
        f.write("=== NMAP SCAN REPORT ===\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Target: {target}\n")
        f.write(f"Nmap Command: {' '.join(command)}\n\n")

        f.write("=== RAW NMAP OUTPUT ===\n")
        f.write(output + "\n\n")

        f.write("=== SUMMARY ===\n")
        if open_ports:
            f.write("Open Ports:\n")
            for port, service in open_ports:
                f.write(f" - {port} ({service})\n")
        else:
            f.write("No open ports found.\n")

    print(f"\n📁 Log saved to: {filename}")

# -------------------------
# Pretty print results (with colors)
# -------------------------
def print_colored_results(output):
    lines = output.split("\n")

    for line in lines:
        if "open" in line:
            print(GREEN + line + RESET)  # Open ports = green
        elif "/tcp" in line:
            print(BLUE + line + RESET)   # TCP service lines = blue
        elif "warning" in line.lower():
            print(YELLOW + line + RESET)
        elif "error" in line.lower():
            print(RED + line + RESET)
        else:
            print(line)

# -------------------------
# Run Nmap scan
# -------------------------
def run_nmap_scan(target):
    command = ["nmap", "-sV", target]

    print(f"\n{BLUE}Running: {' '.join(command)}{RESET}\n")

    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout

    # Print results with color
    print_colored_results(output)

    # Save log
    save_log(target, command, output)


# -------------------------
# Main entry
# -------------------------
if __name__ == "__main__":
    target = input("Enter target IP or domain: ")

    print(f"\n{YELLOW}🔍 Starting Nmap scan...{RESET}\n")
    run_nmap_scan(target)

