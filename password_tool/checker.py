# Jeffar - Password Checker
# Description - Evaluates password strength.
# 2026-06-11

# Constants
MIN_LENGTH = 8      # password's minimum length

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
    if score != 5:
        missing = []

        if not length:
            missing.append("at least 8 characters")
        if not has_uppercase:
            missing.append("uppercase letter")
        if not has_lowercase:
            missing.append("lowercase letter")
        if not has_digit:
            missing.append("digit")
        if not has_symbol:
            missing.append("symbol")

        print("Missing:", ", ".join(missing))

# enter_password - prompts the user to enter a password
def enter_password():
    password = input("Enter a password: ")
    return password

# check_length - checks password
# password - the password the user wants to check
def check_length(password):
    if len(password) >= MIN_LENGTH:
        return True
    return False
    
# check_uppercase - checks if password has an uppercase
# password - the password the user wants to check
def check_uppercase(password):
    for i in password:
        if i.isupper():
            return True
    return False

# check_lowercase - checks if password has a lowercase
# password - the password the user wants to check
def check_lowercase(password):
    for i in password:
        if i.islower():
            return True
    return False

# check_digit - checks if password has a digit
# password - the password the user wants to check     
def check_digit(password):
    for i in password:
        if i.isdigit():
            return True
    return False

# check_symbol - checks if password has atleast a symbol
def check_symbol(password):
    symbols = r'!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'

    if any(char in symbols for char in password):
        return True
    return False

main()