# Jeffar - Password Tool CLI
# Description - Combines password checker and generator tool into one script.
# Created - 2026-06-30
# Last updated - 2026-07-13

# Modules
# note: KEEP __init__.py
from password_tool import checker       # for password checker
from password_tool import generator     # for password generator

from rich.console import Console        # for colors
console = Console()                     # create a console

# Main function
def main():
    user_input = ""

    while True:
        print("\nPASSWORD TOOL")
        print("(1) Check a password")
        print("(2) Generate a password")
        print("(0) Exit")
        
        user_input = input("Select option: ").strip()

        if user_input == '1':
            checker.main()
        elif user_input == '2':
            generator.main()
        elif user_input == '0':
            return
        else:
            console.print("[red]INVALID INPUT[/]")

# dunder name guard
if __name__ == "__main__":
    main()