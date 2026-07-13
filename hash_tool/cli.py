# Jeffar - Hash Tool CLI
# Description - Combines hash generator and compare tool into one script.
# Created - 2026-07-04
# Last updated - 2026-07-13

# Modules
# note: KEEP __init__.py
from hash_tool import generator     # for hash generator
from hash_tool import compare       # for hash compare

# Main function
def main():
    user_input = ""

    while True:
        print("\nHASH TOOL")
        print("(1) Generate a hash")
        print("(2) Compare two hashes")
        print("(0) Exit")
        
        user_input = input("Select option: ").strip()

        if user_input == '1':
            generator.main()
        elif user_input == '2':
            compare.main()
        elif user_input == '0':
            return
        else:
            print("\033[31mINVALID INPUT\033[0m")

# dunder name guard
if __name__ == "__main__":
    main()