# Jeffar - Main Menu
# Description - Ties the whole toolkit into an interactive menu.
# Created - 2026-07-13
# Last updated - 2026-07-13

# Modules
import sys

from password_tool import cli as password_cli
from hash_tool import cli as hash_cli
from port_scanner import scanner as scan_cli

from pyfiglet import figlet_format              # for banner
from rich.console import Console                # for colors
console = Console()                             # create a console

def main():
    user_input = ""

    while True:
        # banner
        print(figlet_format("Security Toolkit", font="slant"), end="")
        console.print("[italic]Made by Jeffar[/]")

        # options
        print("(1) Password tool")
        print("(2) Hash tool")
        print("(3) Port scanner")
        print("(0) Exit")
        
        user_input = input("Select option: ").strip()

        if user_input == '1':
            password_cli.main()
        elif user_input == '2':
            hash_cli.main()
        elif user_input == '3':
            scan_cli.main()
        elif user_input == '0':
            sys.exit()
        else:
            console.print("[red]INVALID INPUT[/]")

# dunder name guard
if __name__ == "__main__":
    main()