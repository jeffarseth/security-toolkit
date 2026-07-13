# Jeffar - Main Menu
# Description - Ties the whole toolkit into an interactive menu.
# Created - 2026-07-13
# Last updated - 2026-07-13

# Modules
import sys

# for clearing terminal
import platform     # for checking os
import subprocess   # for executing commands

from password_tool import cli as password_cli
from hash_tool import cli as hash_cli
from port_scanner import scanner as scan_cli

from pyfiglet import figlet_format              # for banner
from rich.console import Console                # for colors
from rich.text import Text                      # for text object
console = Console()                             # create a console

def main():
    user_input = ""
    banner = build_banner()             # builds and stores banner ASCII art

    while True:
        clear_terminal()

        # print banner
        console.print(banner, end="")
        console.print("[italic dim]Made by Jeffar[/]\n")

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
            clear_terminal()
            sys.exit()
        else:
            console.print("[red]INVALID INPUT[/]")

# Functions
def build_banner():
    """
    build_banner - renders the ASCII title with a blue-to-yellow gradient
    """

    banner = figlet_format("Security Toolkit", font="slant")
    banner_text = Text()                                        # create a rich text object to append to

    # process each row of the ASCII banner
    for line in banner.splitlines():

        # process each character in the current row
        # i represents the horizontal position of the character
        for i, char in enumerate(line):

            # convert the character position into a value from 0.0 to 1.0 (linear)
            # 0.0 = start of gradient (blue)
            # 1.0 = end of gradient (yellow)
            # max(..., 1) avoids division by zero on empty or single-character lines
            ratio = i / max(len(line) - 1, 1)

            # blue to yellow gradient calculation
            r = int(0 + (255 * ratio))
            g = int(100 + (155 * ratio))
            b = int(255 * (1 - ratio))

            # add the current character with its calculated gradient color
            banner_text.append(char, style=f"rgb({r},{g},{b})")

        # preserve the original ASCII art line breaks
        banner_text.append("\n")

    return banner_text

def clear_terminal():
    """
    clear_terminal - clears all visible text from the terminal
    """

    if platform.system() == "Windows":      # cls for Windows
        subprocess.run("cls", shell=True)
    else:                                   # clear for macOS, Linux, Unix
        subprocess.run(["clear"])

# dunder name guard
if __name__ == "__main__":
    main()