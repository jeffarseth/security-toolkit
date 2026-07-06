# Jeffar - Port Scanner
# Description - Scans a target's ports with service detection and a summary report.
# Created - 2026-07-05
# Last updated - 2026-07-05

# Modules
from port_scanner.services import get_service   # for port's service lookup
import time                                     # for elapsed time
import socket                                   # for sock: networking module

def main():
    print("\nPORT SCANNER")
    get_target()

# Functions
def get_target():
    """
    get_target - prompt user for target (hostname or IP)
    """

    target = ""     # target to scan
    ip = ""         # resolved ipv4 address
    
    # input validation
    while True:
        target = input("Enter target (hostname or IP): ").strip()   # prompt again if fail

        try:
            ip = socket.gethostbyname(target)                       # query DNS and returns an ipv4 address string
            print("Resolved to:", ip)
            return ip                                               # return target's ipv4 address
        except socket.gaierror as err:                              # get address info error (a.k.a. gaierror)
            print("\033[31mDNS lookup failed:", err, "\033[0m")     # print error details
        

# dunder name guard
if __name__ == "__main__":
    main()