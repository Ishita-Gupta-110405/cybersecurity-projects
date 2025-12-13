import requests
import threading
from queue import Queue
import json
from colorama import Fore, Style, init
import datetime

init(autoreset=True)

q = Queue()
found_subdomains = []
LOG_FILE = "subdomain_scanner.log"

def log(message):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def check_subdomain(domain):
    global q

    while not q.empty():
        sub = q.get()
        url = f"http://{sub}.{domain}"

        try:
            response = requests.get(url, timeout=2)
            if response.status_code < 400:
                print(Fore.GREEN + "[+] Active →", url)
                found_subdomains.append(url)
                log(f"ACTIVE: {url}")
            else:
                print(Fore.RED + "[-] Inactive →", url)
        except:
            print(Fore.YELLOW + "[!] Unreachable →", url)

        q.task_done()

def main():
    domain = input("Enter domain (example: google.com): ").strip()

    wordlist = "subdomains.txt"
    try:
        with open(wordlist, "r") as f:
            subs = f.read().splitlines()
    except FileNotFoundError:
        print(Fore.RED + "subdomains.txt not found!")
        return

    print(Fore.CYAN + f"\nStarting scan for: {domain}\n")

    for sub in subs:
        q.put(sub)

    threads = []
    for _ in range(20):  # 20 threads = fast scanning
        t = threading.Thread(target=check_subdomain, args=(domain,))
        t.daemon = True
        threads.append(t)
        t.start()

    q.join()

    # Save results
    with open("subdomain_results.txt", "w") as f:
        for s in found_subdomains:
            f.write(s + "\n")

    with open("subdomain_results.json", "w") as f:
        json.dump(found_subdomains, f, indent=4)

    print(Fore.GREEN + "\nScan complete!")
    print(Fore.BLUE + f"Results saved in subdomain_results.txt and .json")
    print(Fore.BLUE + f"Logs saved in {LOG_FILE}")

if __name__ == "__main__":
    main()
