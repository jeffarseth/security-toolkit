# Jeffar - Password Checker
# Description - Evaluates password strength.
# Last updated - 2026-06-28

# Modules
# i learnt the differences between libraries, modules, and the functions inside a module (class)
from pathlib import Path    # for filepath
from getpass import getpass # for hiding input

# Constants
MIN_LENGTH = 8                                                              # password's minimum length
WORDLIST_PATH = Path(__file__).parent.parent / "data" / "passwords.txt"     # passwords.txt file path: gets to "security-toolkit"

# Main function
def main():
    score = 0                       # score default: is 0 as the weakest
    length = False                  # default: length < 8 is False
    has_uppercase = False           # default: uppercase not present
    has_lowercase = False           # default: lowercase not present
    has_digit = False               # default: digit not present
    has_symbol = False              # default: symbol not present

    print("PASSWORD CHECKER\n")
    password = enter_password()

    # add one to the score if there are >= 8 characters
    if check_length(password):
        score+=1
        length = True

    # add one to the score if there is an uppercase in password
    if check_uppercase(password):
        score+=1
        has_uppercase = True
    
    # add one to the score if there is a lowercase in password
    if check_lowercase(password):
        score+=1
        has_lowercase = True

    # add one to the score if there is a digit in password
    if check_digit(password):
        score+=1
        has_digit = True

    # add one to the score if there is a symbol in password
    if check_symbol(password):
        score+=1
        has_symbol = True

    print(f"\nScore: {score} / 5")  # prints score out of 5

    print("Verdict: ", end="")      # prints verdict
    if score <= 2:                  # Weak (1-2)
        print("Weak")
    elif score > 2 and score <=4:   # Medium (3-4)
        print("Medium")
    else:                           # Strong (5)
        print("Strong")

    # Find what failed
    if score != 5:                                  # only runs if it doesn't have a perfect score
        missing = []                                # list for printing missing requirements

        if not length:
            missing.append("at least 8 characters") # append() adds this string into the list
        if not has_uppercase:
            missing.append("uppercase letter")
        if not has_lowercase:
            missing.append("lowercase letter")
        if not has_digit:
            missing.append("digit")
        if not has_symbol:
            missing.append("symbol")

        print("Missing:", ", ".join(missing))       # join() combines the list of strings into one string (separated by ", ")

    # check if password is a commonly-used password
    if check_wordlist(password, load_wordlist()):
        print(f"WARNING: \"{password}\" was found in a list of commonly-used passwords!")

# Functions
def enter_password():
    """
    enter_password - prompts the user to enter a password
    """

    hide = ""

    # input validation
    while True:
        hide = input("Hide input (Y/N)? ").upper()

        if hide == 'Y': 
            password = getpass("Enter a password: ")    # user input's hidden
            break
        elif hide == 'N':
            password = input("Enter a password: ")      # user inputs in plaintext
            break
        else:
            print("\033[31mINVALID INPUT\033[0m")

    return password

def check_length(password):
    """
    check_length - checks password

    password - the password the user wants to check
    """

    if len(password) >= MIN_LENGTH:
        return True
    return False
    
def check_uppercase(password):
    """
    check_uppercase - checks if password has an uppercase

    password - the password the user wants to check
    """

    for i in password:
        if i.isupper():
            return True
    return False

def check_lowercase(password):
    """
    check_lowercase - checks if password has a lowercase
    
    password - the password the user wants to check
    """

    for i in password:
        if i.islower():
            return True
    return False

def check_digit(password):
    """
    check_digit - checks if password has a digit

    password - the password the user wants to check
    """
    for i in password:
        if i.isdigit():
            return True
    return False

def check_symbol(password):
    """
    check_symbol - checks if password has atleast a symbol
    
    password - the password the user wants to check
    """

    symbols = r'!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'

    if any(char in symbols for char in password):
        return True
    return False

def load_wordlist():
    """
    load_wordlist - returns the passwords (set) of password.txt
    """

    if not WORDLIST_PATH.exists():      # if passwords.txt isn't found
        print("wordlist not found.")
        return set()                    # returns an empty set and ignores rest of the function

    # set comprehension with wordlist
    with open(WORDLIST_PATH, encoding="utf-8", errors="ignore") as file:    # utf-8 to avoid UnicodeDecodeError
        wordlist_set =  {line.strip().lower() for line in file}             # line.strip() removes spaces, tabs, newlines.
                                                                            # lower() makes it case-insensitive (match with user's password)
                                                                            # this iterates every line found in passwords.txt.

    return wordlist_set

def check_wordlist(password, wordlist):
    """
    check_wordlist - checks if password is in passwords.txt
    
    password - the password the user wants to check
    
    wordlist - the set of common passwords
    """

    return password.lower() in wordlist         # compares password to wordlist using 'in' then returns True if password is found in wordlist
                                                # lower() makes it case-insensitive (match with wordlist)

main()