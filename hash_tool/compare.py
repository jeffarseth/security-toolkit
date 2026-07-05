# Jeffar - Hash Compare
# Description - Compares two known hashes the user provides and check if it's a match.
# Created - 2026-07-04
# Last Updated - 2026-07-04

# Main function
def main():
    hash1 = ""          # hash to compare from
    hash2 = ""          # hash to compare to
    ignore_case = ""    # option to ignore case-sensitivity
    match = False       # tells if the two hashes are a match: initialized to False

    hash1 = input("Paste hash 1: ").strip()
    hash2 = input("Paste hash 2: ").strip()

    while True:
        ignore_case = input("Ignore case? (Y/N): ").strip().upper()

        if ignore_case == 'Y':
            match = hash1.lower() == hash2.lower()
            break
        elif ignore_case == 'N':
            match = hash1 == hash2
            break
        else:
            print("\033[31mINVALID INPUT\033[0m")

    print("MATCH" if match else "NO MATCH")

# dunder name guard
if __name__ == "__main__":
    main()