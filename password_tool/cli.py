# Jeffar - Password Tool CLI
# Description - Combines all password checker and generator tool into one script.
# Created - 2026-06-30
# Last updated - 2026-07-02

# Modules
# note: KEEP __init__.py
from password_tool import checker       # for password checker
from password_tool import generator     # for password generator

import sys          # for sys.exit()

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
            sys.exit(0)
        else:
            print("\033[31mINVALID INPUT\033[0m")

# dunder name guard
if __name__ == "__main__":
    main()