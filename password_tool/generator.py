# Jeffar - Password Generator
# Description - Generates passwords with custom options.
# Created - 2026-06-28
# Last updated - 2026-06-30

# Modules
import secrets      # for cryptographically generating passwords
import string       # for character sets

# Constants
SYMBOLS_SET = "!@#$%_-.+?"
LOWERCASE_SET = string.ascii_lowercase
UPPERCASE_SET = string.ascii_uppercase
DIGITS_SET = string.digits

# Main function
def main():
    user_input = ""

    while True:
        print("Select an option")
        print("(1) Basic mode")
        print("(2) Advanced mode")
        print("(0) Exit")
        
        user_input = input("Select option: ").strip()

        if user_input == '1':
            print(generate_basic())
        elif user_input == '2':
            print(generate_advanced())
        elif user_input == '0':
            return
        else:
            print("\033[31mINVALID INPUT\033[0m")

# Functions
def generate_basic():
    """
    generate_basic - generates a 16-character password
    """

    characters = SYMBOLS_SET + LOWERCASE_SET + UPPERCASE_SET + DIGITS_SET   # combines all of these characters into one string
    return "".join(secrets.choice(characters) for _ in range(16))           # returns the 16-character string

def generate_advanced():
    """
    generate_advanced - generates a password with several options
    """

    characters = ""             # combines all of these characters into one string
    length = 0                  # the password's length: initialized to 0
    has_lowercase = ""          # if password has lowercase
    has_uppercase = ""          # if password has uppercase
    has_digits = ""             # if password has digits
    has_symbols = ""            # if password has symbols
    how_many = 0                # how many passwords are generated: initialized to 0
    passwords = []              # array of passwords
    remaining = 0               # tells how how many slots are left after guaranteed characters: initialized to 0

    while True:
        try:
            length = int(input("Password Length (>0)? ").strip())               # prompt password's length
            if length <= 0:                                                     # password length must be greater than 0
                print("\033[31mINVALID INPUT - must be greater than 0!\033[0m")
                continue                                                        # repeat while loop
            
            break

        except ValueError:                                                      # handles non-integer input (e.g. "abc")
            print("\033[31mINVALID INPUT - enter a whole number!\033[0m")
            continue

    while True:
        while True:
            has_lowercase = input("Include Lowercase (Y/N)? ").strip().upper()  # prompt lowercase inclusion
            if has_lowercase != 'Y' and has_lowercase != 'N':
                print("\033[31mINVALID INPUT\033[0m")
            else:
                break

        while True:
            has_uppercase = input("Include Uppercase (Y/N)? ").strip().upper()  # prompt uppercase inclusion
            if has_uppercase != 'Y' and has_uppercase != 'N':
                print("\033[31mINVALID INPUT\033[0m")
            else:
                break

        while True:
            has_digits = input("Include Digits (Y/N)? ").strip().upper()        # prompt digits inclusion
            if has_digits != 'Y' and has_digits != 'N':
                print("\033[31mINVALID INPUT\033[0m")
            else:
                break

        while True:
            has_symbols = input("Include Symbols (Y/N)? ").strip().upper()      # prompt symbols inclusion
            if has_symbols != 'Y' and has_symbols != 'N':
                print("\033[31mINVALID INPUT\033[0m")
            else:
                break

        # repeat option selecting if all options are 'N'
        if has_lowercase == 'N' and has_uppercase == 'N' and has_digits == 'N' and has_symbols == 'N':
            print("\033[31mNONE OF THE OPTIONS WERE SELECTED, RETRY\033[0m")
        else:
            break

    while True:
        try:
            how_many = int(input("How many passwords (>0)? ").strip())          # prompt how many passwords
            if how_many <= 0:
                print("\033[31mINVALID INPUT - must be greater than 0!\033[0m")
                continue
            
            break

        except ValueError:
            print("\033[31mINVALID INPUT - enter a whole number!\033[0m")
            continue
        
    # concatenate the characters string
    if has_lowercase == 'Y':
        characters += LOWERCASE_SET
    if has_uppercase == 'Y':
        characters += UPPERCASE_SET
    if has_digits == 'Y':
        characters += DIGITS_SET
    if has_symbols == 'Y':
        characters += SYMBOLS_SET

    # generate each password
    for _ in range(how_many):
        guaranteed = []                                                                         # array of guaranteed characters from each type (symbol,lowercase,uppercase,digit)
 
        # step 1: seed one guaranteed character from each selected type
        # this ensures every selected type appears at least once
        if has_lowercase == 'Y':
            guaranteed.append(secrets.choice(LOWERCASE_SET))
        if has_uppercase == 'Y':
            guaranteed.append(secrets.choice(UPPERCASE_SET))
        if has_digits == 'Y':
            guaranteed.append(secrets.choice(DIGITS_SET))
        if has_symbols == 'Y':
            guaranteed.append(secrets.choice(SYMBOLS_SET))
 
        # if length is shorter than the number of selected types,
        # skip the guarantee and draw purely randomly to avoid overflow
        if length < len(guaranteed):
            password = "".join(secrets.choice(characters) for _ in range(length))
            passwords.append(password)
            continue                                                                            # skip to next password
 
        # step 2: fill remaining slots from the full combined unshuffled_chars
        remaining = length - len(guaranteed)                                                    # calculate how many slots are left after guaranteed characters
        rest = [secrets.choice(characters) for _ in range(remaining)]                           # fill remaining slots randomly
 
        # step 3: combine guaranteed + random, then shuffle securely
        unshuffled_chars = guaranteed + rest                                                    # one flat list of characters
 
        # fisher-yates shuffle using secrets.randbelow (cryptographically secure)
        # walks backwards through the list, swapping each position with a random earlier one
        # wikipedia reference: https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle
        for i in range(len(unshuffled_chars) - 1, 0, -1):                                       # i goes from last index down to 1
            j = secrets.randbelow(i + 1)                                                        # pick a random index from 0 to i
            unshuffled_chars[i], unshuffled_chars[j] = unshuffled_chars[j], unshuffled_chars[i] # swap the two positions
 
        password = "".join(unshuffled_chars)                                                    # join the shuffled list into one string
        passwords.append(password)
 
    return "\n".join(passwords)                                                                 # returns all passwords separated by newline

# dunder name guard
if __name__ == "__main__":
    main()