# Jeffar - Port Scanner
# Description - Scans a target's tcp/udp ports with multithreading, service detection, and a summary report.
# Created - 2026-07-05
# Last updated - 2026-07-13

# IMPORTANT NOTE!!
# SCOPE: only scan localhost or hosts you are explicitly authorized to test.

# Modules
import port_scanner.services as services            # for ports service lookup
from concurrent.futures import ThreadPoolExecutor   # for multithreading
from pathlib import Path                            # for filepath
import time                                         # for elapsed time
import socket                                       # for sock: networking module
import json                                         # for exporting to json
import csv                                          # for exporting to csv

from rich.console import Console                    # for colors
console = Console()                                 # create a console

# for clearing terminal
import platform                                     # for checking os
import sys                                          # for "Press any key to continue..."
import subprocess                                   # for executing commands

# Constants
BUFFER_SIZE = 1024      # maximum number of bytes to read in one call.
THREAD_LIMIT = 2000     # maximum amount of threads to use

# Main function
def main():
    ip = ""             # target ip
    ports = []          # target port/s
    timeout = 0         # how long to wait (in seconds) for a response before giving up on this port
    max_workers = 0     # amount of threads. how many ports to check concurrently
    start_time = 0      # start time for recording elapsed time during scan: initialized to 0 seconds
    end_time = 0        # end time for recording elapsed time during scan: initialized to 0 seconds
    results = []        # holds port number, service name, and banner
    open_ports = 0      # amount of open ports: initialized to 0

    clear_terminal()
    print("PORT SCANNER")

    ip = get_target()
    ports = get_ports()
    timeout = get_timeout()
    max_workers = get_threads()

    start_time = time.time()        # start recording time
    results = scan(ip, ports, timeout, max_workers)
    open_ports = len(results)
    end_time = time.time()          # stop recording time (ザワールド)

    export(results)
    print_summary(ports, open_ports, start_time, end_time)
    pause()

# Functions
def get_target():
    """
    get_target - prompts the user for target (hostname or IP)
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
            console.print("[red]DNS lookup failed:", err, "[/]")     # print error details
        
def get_ports():
    """
    get_ports - prompts the user for scan mode (quick/full/customr/customs) and returns port collection to scan
    """

    user_input = ""
    lowest = ""         # for custom ports (lowest to highest)
    highest = ""        # for custom ports (lowest to highest)

    port = None                                     # placeholder for adding ports in port selection
    quick_ports = list(services.SERVICE_PORTS)      # list of common port numbers from SERVICE_PORTS
    full_ports = range(0, 65536)                    # list of port numbers from 0-65535
    custom_ports = []                               # list of ports from user's choice

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
                        console.print("[red]INVALID INPUT[/]")
                except ValueError:
                    console.print("[red]INVALID INPUT - enter a whole number![/]")

            if lowest == 65535:                                                         # user doesn't get to choose highest port to scan if there's no space for it
                return [65535]

            while True:
                try:
                    highest = int(input(f"Highest port number ({lowest}-65535): "))
                    if lowest <= highest < 65536:                                       # user gets to choose range from highest port to scan (lowest-65535)
                        break
                    else:
                        console.print("[red]INVALID INPUT[/]")
                except ValueError:
                    console.print("[red]INVALID INPUT - enter a whole number![/]")

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

                            if len(custom_ports) == 65536:                              # all ports selected
                                return custom_ports

                        else:
                            console.print("[red]PORT ALREADY ADDED[/]")
                            continue
                    else:
                        console.print("[red]INVALID INPUT[/]")
                        continue
                except ValueError:
                    console.print("[red]INVALID INPUT - enter a whole number![/]")
                    continue

                while True:
                    user_input = input("Enter another port (Y/n)? ").strip().upper()    # prompt user for another port to enter

                    if user_input == "N":
                        return custom_ports
                    elif user_input == "Y" or user_input == "":                         # repeat until there are no more ports to scan
                        break
                    else:
                        console.print("[red]INVALID INPUT[/]")
        
        else:
            console.print("[red]INVALID INPUT[/]")

def get_timeout():
    """
    get_timeout - prompts the user for timeout
    """

    user_input = ""
    timeout = 1     # how long to wait (in seconds) for a response before giving up on this port: initialized to 1 second for default

    # input validation
    while True:
        try:
            user_input = input("\nTimeout in seconds (leave blank for 1s default): ").strip()

            if user_input == "":                                # default if input is blank
                return timeout

            timeout = float(user_input)                         # convert str to float

            if timeout > 0:                                     # timeout has to be greater than 0 seconds
                return timeout
            else:
                console.print("[red]INVALID INPUT[/]")

        except ValueError:
            console.print("[red]INVALID INPUT - enter a valid number![/]")

def get_threads():
    """
    get_threads - prompts the user for amount of max_workers (not clothes, threads)
    """

    user_input = ""
    max_workers = 200   # amount of threads. how many ports to check concurrently: initialized to 200 threads for default

    # input validation
    while True:
        try:
            user_input = input("Max concurrent threads (leave blank for 200 default): ").strip()

            if user_input == "":                                # default if input is blank
                break

            max_workers = int(user_input)                       # convert str to int

            if 0 < max_workers <= THREAD_LIMIT:                 # threads has to greater than 0
                break
            elif max_workers > THREAD_LIMIT:                    # thread amount: safety net for system stability
                console.print(f"[red]CAPPED AT {THREAD_LIMIT} - enter a number <= {THREAD_LIMIT}[/]")
            else:
                console.print("[red]INVALID INPUT[/]")

        except ValueError:
            console.print("[red]INVALID INPUT - enter a whole number![/]")

def scan(ip, ports, timeout, max_workers):
    """
    get_scan_type - prompts the user to scan in tcp or udp

    ip - target ip

    ports - target port/s

    timeout - how long to wait (in seconds) for a response before giving up on this port

    max_workers - amount of threads: how many ports to check concurrently
    """

    # function lookup table for scan type
    scan_types = {
        "tcp": scan_ipv4_tcp,
        "udp": scan_ipv4_udp
    }

    scan_type = ""
    results = []                                        # holds results list

    # input validation
    while True:
        scan_type = input("Scan type (tcp/udp): ").strip().lower()

        if scan_type in scan_types:                     # only use function if it's a valid scan type
            results = scan_types[scan_type](ip, ports, timeout, max_workers)
            break
        else:
            console.print("[red]INVALID INPUT[/]")
        
    return results

def scan_one_tcp_port(ip, port, timeout):
    """
    scan_one_tcp_port - connects to a single tcp port and returns its result, or None if closed

    ip - target ip

    port - port to check

    timeout - how long to wait (in seconds) for a response before giving up on this port
    """

    result = None   # holds port number, service name, and banner: closed by default

    # create a TCP ipv4 socket object ready to connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # set timeout in seconds
    sock.settimeout(timeout)
    
    try:
        # attempt to connect to a specific IP and port
        success = sock.connect_ex((ip, port))                       # unlike connect(), connect_ex() does not crash on failure

        # if connection was successful
        if success == 0:
            # get banner
            try:
                raw = sock.recv(BUFFER_SIZE)                        # in bytes, or raises on timeout
                banner = raw.decode(errors="replace").strip()       # bytes to clean one-line string
            except (socket.timeout, OSError):                       # silent service or connection issue
                banner = ""                                         # leave it empty

            # get service name
            service_name = services.get_service(port)

            # print port number, service name if in dictionary, and banner if it exists
            print(f"PORT {port}    OPEN    ({service_name})    {banner if banner else 'no banner'}")

            # append to result[]
            result = {"port": port, "state": "OPEN", "service": service_name, "banner": banner}
    except:
        sock.close()                                                # close the socket connection to not leak a resource

    return result

def scan_ipv4_tcp(ip, ports, timeout, max_workers):
    """
    scan_ipv4_tcp - scans multiple tcp ports on an ipv4 target using multiple threads

    ip - target ip

    ports - target port/s

    timeout - how long to wait (in seconds) for a response before giving up on this port

    max_workers - amount of threads: how many ports to check concurrently
    """

    results = []                                                        # list of dictionaries containing open port results

    print("\npress CTRL + C to cancel scan anytime")
    print(f"Scanning {len(ports)} ports on {ip}...\n")

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:   # user-controlled concurrency, capped at THREAD_LIMIT for system stability
            
            # get every port with the same ip and timeout
            all_results = executor.map(lambda port: scan_one_tcp_port(ip, port, timeout), ports)

            for result in all_results:
                if result is not None:                                  # exclude none
                    results.append(result)                              # append result as it arrives

    except KeyboardInterrupt:
        executor.shutdown(wait=False, cancel_futures=True)              # shut down the thread pool and cancel queued scans
        console.print("[red]SCAN CANCELLED[/]")

    return results

def scan_one_udp_port(ip, port, timeout):
    """
    scan_one_udp_port - checks a single udp port and returns its result, or None if closed

    ip - target ip

    port - port to check

    timeout - how long to wait (in seconds) for a response before giving up on this port
    """

    result = None   # holds port number, service name, and banner: closed by default
    state = ""      # tells if udp port is open/open|filtered/closed

    # create a udp ipv4 socket object ready to connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # set timeout in seconds
    sock.settimeout(timeout)

    try:    
        # send an empty udp packet to the target
        sock.sendto(b"", (ip, port))

        # wait for a reply from the target.
        data, addr = sock.recvfrom(BUFFER_SIZE)     # note: data and addr are unused values

        # a reply means the port is open.
        state = "open"
    except socket.timeout:                          # no reply was received before the timeout (port may be open or filtered by a firewall)
        state = "open|filtered"
    except (ConnectionResetError, OSError):         # icmp "Destination Unreachable" message
        state = "closed"
    finally:
        sock.close()                                # close the socket connection to not leak a resource

    # get service name
    service_name = services.get_service(port)

    if state != "closed":                           # report open and open|filtered, skip closed
        print(f"PORT    {port}    {state.upper()}    ({service_name})")
        result = {"port": port, "state": state, "service": service_name, "banner": ""}

    return result

def scan_ipv4_udp(ip, ports, timeout, max_workers):
    """
    scan_ipv4_udp - scans multiple udp ports on an ipv4 target using multiple threads

    ip - target ip

    ports - target port/s

    timeout - how long to wait (in seconds) for a response before giving up on this port

    max_workers - amount of threads: how many ports to check concurrently
    """

    results = []                                                        # list of dictionaries containing open port results

    print("\npress CTRL + C to cancel scan anytime")
    print(f"Scanning {len(ports)} ports on {ip}...\n")

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:   # user-controlled concurrency, capped at THREAD_LIMIT for system stability
            
            # get every port with the same ip and timeout
            all_results = executor.map(lambda port: scan_one_udp_port(ip, port, timeout), ports)

            for result in all_results:
                if result is not None:                                  # exclude none
                    results.append(result)                              # append result as it arrives
            
    except KeyboardInterrupt:
        executor.shutdown(wait=False, cancel_futures=True)              # shut down the thread pool and cancel queued scans
        console.print("[red]SCAN CANCELLED[/]")

    return results

def export(results):
    """
    export - prompts the user save the results to a file (plain text, JSON, or CSV) in a folder of their choosing

    results - list of result dicts (port, state, service, banner)
    """

    # function lookup table for exporting to a file
    export_methods = {
        "txt": export_txt,
        "json": export_json,
        "csv": export_csv
    }

    user_input = ""
    filepath = ""                   # where to save file (dir)
    selected_format = ""            # choose to save as txt, json, or csv
    filename = "port_scan_results"  # saved file name: default to "port_scan"
    savepath = ""                   # saved file with dir and extension

    # input validation
    while True:
        user_input = input("\nExport results (y/N)? ").strip().upper()

        if user_input == "N" or user_input == "":
            return
        elif user_input == "Y":
            break
        else:
            console.print("[red]INVALID INPUT[/]")

    # input validation
    while True:
        user_input = input("Enter filepath: ")                          # get raw string first
        filepath = Path(user_input.strip().strip('"').strip("'"))       # removes leading/trailing whitespace/newlines and surrounding Windows quotes when using "Copy as path"
        filepath = filepath.resolve()                                   # turn it into an absolute path
        
        if filepath.exists() and filepath.is_file():                    # path exists but it's a file
            console.print("[red]Path is a file, not a folder[/]")
        elif filepath.exists() and filepath.is_dir():                   # path exists and it's a folder
            break
        else:
            filepath.mkdir(parents=True, exist_ok=True)                 # make a directory, include parents on a nested dir, and ignore "Folder already there" warnings
            break

    
    user_input = input("Enter filename: ").strip()                      # prompt user for file's name
    if user_input != "":                                                # use user_input if not left default
        filename = user_input

    # input validation
    while True:
        selected_format = input("Format (txt/json/csv): ").strip().lower()
        
        if selected_format in export_methods:                           # only use function if it's a valid exporting method
            savepath = filepath / f"{filename}.{selected_format}"       # combine folder, filename, extension
            export_methods[selected_format](results, savepath)
            break
        else:
            console.print("[red]INVALID INPUT[/]")
        
def export_txt(results, savepath):
    """
    export_txt - writes the results list to a text file

    results - list of result dicts (port, state, service, banner)

    savepath - saved file with dir and extension
    """

    with open(savepath, "w", encoding="utf-8") as file:                 # writes to savepath in utf-8 and create object file
        for result in results:                                          # iterate every result inside results
            # get the port state
            state = result.get("state", "unknown")

            # get the banner
            banner = result.get("banner", "")

            # write the output line
            line = f"PORT    {result['port']}    {state.upper()}    ({result['service']})"

            # add the banner only if it exists
            if banner:
                line += f"    {banner}"

            # write the completed line to the file separated by newlines
            file.write(line + "\n")

def export_json(results, savepath):
    """
    export_json - writes the results list to a JSON file

    results - list of result dicts (port, state, service, banner)

    savepath - saved file with dir and extension
    """

    with open(savepath, "w", encoding="utf-8") as file:                 # writes to savepath in utf-8 and create object file
        json.dump(results, file, indent=4)                              # write results to file with most used tab indentation

def export_csv(results, savepath):
    """
    export_csv - writes the results list to a CSV file
    
    results - list of result dicts (port, state, service, banner)

    savepath - saved file with dir and extension
    """

    with open(savepath, "w", newline="", encoding="utf-8") as file:     # writes to savepath in utf-8 without automatic \n and create object file
        writer = csv.DictWriter(
            file,                                                       # write to file object
            fieldnames=["port", "state", "service", "banner"]           # CSV column order
        )

        # write port, service, and banner
        writer.writeheader()
        writer.writerows(results)

def print_summary(ports, open_ports, start_time, end_time):
    """
    print_summary - prints the total number of ports scanned, number of open ports, number of closed ports, and total scan duration.

    ports - target port/s

    open_ports - amount of open ports

    start_time - start time for recording elapsed time during scan

    end_time - end time for recording elapsed time during scan
    """

    print("\nScan complete.")
    print(f"Total ports: {len(ports)}")
    print(f"Open: {open_ports}")
    print(f"Closed: {len(ports) - open_ports}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")   # rounded to hundredths

def clear_terminal():
    """
    clear_terminal - clears all visible text from the terminal
    """

    if platform.system() == "Windows":      # cls for Windows
        subprocess.run("cls", shell=True)
    else:                                   # clear for macOS, Linux, Unix
        subprocess.run(["clear"])

def pause():
    """
    pause - display a message asking the user to press a key before continuing
    """
    print("Press any key to continue...", end="", flush=True)

    # Windows provides a built-in module for reading a single key press
    if platform.system() == "Windows":
        import msvcrt

        # wait for one key press and return immediately
        msvcrt.getch()
    # macOS and Linux terminals handle key input differently
    else:
        # termios controls terminal settings, and tty allows reading individual characters
        import termios
        import tty

        # get the file descriptor for standard input (the keyboard)
        fd = sys.stdin.fileno()

        # save the current terminal settings so they can be restored later
        old_settings = termios.tcgetattr(fd)

        try:
            # switch the terminal into raw mode where characters are read immediately and enter is not required
            tty.setraw(fd)

            # read exactly one character from the keyboard
            sys.stdin.read(1)

        finally:
            # restore the original terminal settings to avoid leaving the user's terminal in an altered state
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# dunder name guard
if __name__ == "__main__":
    main()