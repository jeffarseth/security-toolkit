# Jeffar - Hash Tool CLI
# Description - Combines hash generator and compare tool into one script.
# Created - 2026-07-04
# Last updated - 2026-07-13

# Modules
# note: KEEP __init__.py
from hash_tool import generator     # for hash generator
from hash_tool import compare       # for hash compare

from rich.console import Console    # for colors
console = Console()                 # create a console

# for clearing terminal
import platform     # for checking os
import sys          # for "Press any key to continue..."
import subprocess   # for executing commands

# Main function
def main():
    user_input = ""

    while True:
        clear_terminal()

        print("HASH TOOL")
        print("(1) Generate a hash")
        print("(2) Compare two hashes")
        print("(0) Exit")
        
        user_input = input("Select option: ").strip()

        if user_input == '1':
            generator.main()
            pause()
        elif user_input == '2':
            compare.main()
            pause()
        elif user_input == '0':
            return
        else:
            console.print("[red]INVALID INPUT[/]")

# Functions
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