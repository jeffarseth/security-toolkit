# Jeffar - Port Scanner
# Description - Scans a target's ports with service detection and a summary report.
# Created - 2026-07-05
# Last updated - 2026-07-10

# IMPORTANT NOTE!!
# SCOPE: only scan localhost or hosts you are explicitly authorized to test.

# Modules
import port_scanner.services as services    # for ports service lookup
import time                                 # for elapsed time
import socket                               # for sock: networking module

# Constants
LOADING_BAR_WIDTH = 30                      # how wide the loading bar is
CLEAR_WIDTH = LOADING_BAR_WIDTH + 20        # enough spaces to cover bar + percent + count text (to clear/update bar)
BUFFER_SIZE = 1024                          # the maximum number of bytes to read in one call.

def main():
    user_input = "" # blank user input in str
    ip = ""         # target ip
    ports = []      # target port/s
    timeout = 1     # how long to wait (in seconds) for a response before giving up on this port: initialized to 1 second for default
    start_time = 0  # start time for recording elapsed time during scan: initialized to 0 seconds
    end_time = 0    # end time for recording elapsed time during scan: initialized to 0 seconds
    results = []    # holds port number, service name, and banner
    open_ports = 0  # amount of open ports: initialized to 0

    print("\nPORT SCANNER")
    ip = get_target()
    ports = get_ports()

    # input validation
    while True:
        try:
            user_input = input("\nTimeout in seconds (leave blank for 1s default): ").strip()

            if user_input == "":                                # default if input is blank
                timeout = 1
                break

            timeout = float(user_input)                         # convert str to float

            if timeout > 0:                                     # timeout has to be greater than 0 seconds
                break
            else:
                print("\033[31mINVALID INPUT\033[0m")

        except ValueError:
            print("\033[31mINVALID INPUT - enter a valid number!\033[0m")

    start_time = time.time()
    results = scan_ipv4_tcp(ip, ports, timeout)
    open_ports = len(results)
    end_time = time.time()

    print("\n\nScan complete.")
    print(f"Ports scanned: {len(ports)}")
    print(f"Open: {open_ports}")
    print(f"Closed: {len(ports) - open_ports}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")   # rounded to hundredths

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
        
def get_ports():
    """
    get_ports - prompts user for scan mode (quick/full/customr/customs) and returns port collection to scan
    """

    user_input = ""
    lowest = ""         # for custom ports (lowest to highest)
    highest = ""        # for custom ports (lowest to highest)

    quick_ports = list(services.SERVICE_PORTS)      # list of common port numbers from SERVICE_PORTS
    full_ports = range(0, 65536)                    # list of port numbers from 0-65535
    custom_ports = []                               # list of ports from user's choice
    port = None                                     # placeholder for adding ports in port selection

    # input validation
    while True:
        print("\nScan mode:")
        print("(1) Quick (common ports)")
        print("(2) Full (0-65535)")
        print("(3) Custom range")
        print("(4) Custom selection")
        user_input = input("Select option: ")

        if user_input == '1':
            return list(quick_ports)
        elif user_input == '2':
            return list(full_ports)
        elif user_input == '3':     # custom port range
            
            # input validation
            while True:
                try:
                    lowest = int(input("Lowest port number (0-65535): "))               # str to int
                    if 0 <= lowest < 65536:                                             # user gets to choose range from lowest port to scan (0-65535)
                        break
                    else:
                        print("\033[31mINVALID INPUT\033[0m")
                except ValueError:
                    print("\033[31mINVALID INPUT - enter a whole number!\033[0m")

            if lowest == 65535:                                                         # user doesn't get to choose highest port to scan if there's no space for it
                return [65535]

            while True:
                try:
                    highest = int(input(f"Highest port number ({lowest}-65535): "))
                    if lowest <= highest < 65536:                                       # user gets to choose range from highest port to scan (lowest-65535)
                        break
                    else:
                        print("\033[31mINVALID INPUT\033[0m")
                except ValueError:
                    print("\033[31mINVALID INPUT - enter a whole number!\033[0m")

            custom_ports = list(range(lowest, highest + 1))                             # range() doesn't return highest endpoint (hence +1)

            return custom_ports
        
        elif user_input == '4':     # custom port selection
            
            # input validation
            while True:
                try:
                    port = int(input("Enter port number (0-65535): "))

                    if 0 <= port < 65536:                                               # user gets to select a port to scan (0-65535)
                        if port not in custom_ports:                                    # check if port is in custom_ports already (duplicate checking)
                            custom_ports.append(port)                                   # add port to list
                        else:
                            print("\033[31mPORT ALREADY ADDED\033[0m")
                            continue
                    else:
                        print("\033[31mINVALID INPUT\033[0m")
                        continue
                except ValueError:
                    print("\033[31mINVALID INPUT - enter a whole number!\033[0m")
                    continue

                while True:
                    user_input = input("Enter another port (Y/N)? ").strip().upper()    # prompt user for another port to enter

                    if user_input == "N":
                        return custom_ports
                    elif user_input == "Y":                                             # repeat until there are no more ports to scan
                        break
                    else:
                        print("\033[31mINVALID INPUT\033[0m")
        
        else:
            print("\033[31mINVALID INPUT\033[0m")

def scan_ipv4_tcp(ip, ports, timeout):
    """
    scan_ipv4_tcp - starts scanning the target with given ports and timeout for each port 

    ip - target ip

    ports - target port/s

    timeout - how long to wait (in seconds) for a response before giving up on this port
    """

    success = None          # stores connect_ex() result (0 = successful connection)
    results = []            # holds port number, service name, and banner
    port_count = 0          # amount of ports scanned: initialized to 0
    percent = 0             # amount of percent scanned: initialized to 0
    filled = 0              # amount of filled blocks: initialied to 0
    bar = ""                # bar initialized
    last_shown = -1         # impossible starting value so the first port always draws
    banner = ""             # stores banner str
    service_name = ""       # stores service name str

    print(f"\nScanning {len(ports)} ports on {ip}...\n")

    for port in ports:# iterate through all ports
        port_count += 1     # add 1 to count

        # create a TCP IPv4 socket object ready to connect
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set timeout in seconds
        sock.settimeout(timeout)

        # attempt to connect to a specific IP and port
        success = sock.connect_ex((ip, port))                                   # unlike connect(), connect_ex() does not crash on failure

        # if connection was successful
        if success == 0:
            # get banner
            try:
                raw = sock.recv(BUFFER_SIZE)                                    # in bytes, or raises on timeout
                banner = raw.decode(errors="replace").strip()                   # bytes to clean one-line string
            except (socket.timeout, OSError):                                   # silent service or connection issue
                banner = ""                                                     # leave it empty, keep scanning

            # get service name
            service_name = services.get_service(port)

            print("\r" + " " * CLEAR_WIDTH + "\r", end="")                      # erase the leftover bar text first

            # print port number, service name if in dictionary, and banner if it exists
            print(f"PORT {port}     OPEN    ({service_name})   {banner if banner else 'no banner'}")

            # append to results[]
            results.append({"port": port, "service": service_name, "banner": banner})

        percent = int((port_count / len(ports)) * 100)                          # calculate percentage
        if percent != last_shown:                                               # update the progress bar only when the percentage changes
            # calculate bar state
            filled = (port_count * LOADING_BAR_WIDTH) // len(ports)             # use floor division to calculate how many "█" there is
            bar = "█" * filled + "░" * (LOADING_BAR_WIDTH - filled)             # join the two strings together

            print(f"[{bar}]", end=" ")                                          # print bar
            print(f"{percent}%", end=" ")                                       # print percentage
            print(f"({port_count}/{len(ports)})", end="\r")                     # print raw count. "\r" returns the cursor back so it can overwrite

            last_shown = percent                                                # save the current percentage to compare on the next update

        # close the socket connection to not leak a resource
        sock.close()

    return results

# dunder name guard
if __name__ == "__main__":
    main()