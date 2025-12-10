from colorama import Fore, Style, init
init(autoreset=True)
import socket
from datetime import datetime
import logging

# Log configuration
logging.basicConfig(
    filename="scanner.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def scan_port(ip, port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False

def main():
    print(Fore.CYAN + "\n=== Advanced Port Scanner ===" + Style.RESET_ALL)
    ip = input("Enter Target IP: ")
    start_port = int(input("Start Port: "))
    end_port = int(input("End Port: "))

    print(Fore.YELLOW + f"\nScanning {ip} from {start_port} to {end_port}...\n" + Style.RESET_ALL)
    start_time = datetime.now()

    for port in range(start_port, end_port + 1):
        if scan_port(ip, port):
            print(Fore.GREEN + f"[OPEN] Port {port}" + Style.RESET_ALL)
            logging.info(f"OPEN PORT : {port}")
        else:
            print(Fore.RED + f"[CLOSED] Port {port}" + Style.RESET_ALL)

    end_time = datetime.now()
    duration = end_time - start_time
    print(Fore.CYAN + f"\nScan complete in: {duration}" + Style.RESET_ALL)
    logging.info(f"Scan completed in {duration}")

if __name__ == "__main__":
    main()
