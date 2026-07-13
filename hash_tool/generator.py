# Jeffar - Hash Generator
# Description - Generates hash of text (with optional salting) or file. (MD5, SHA-1, SHA-256, SHA-512, SHA3-256, SHA3-512)
# Created - 2026-07-02
# Last updated - 2026-07-13

# Modules
import hashlib                      # for cryptographic hashing
import base64                       # for base64 encoding
import secrets                      # for salt generation
import string                       # for character sets
from getpass import getpass         # for hiding input
from pathlib import Path            # for filepath

from rich.console import Console    # for colors
console = Console()                 # create a console

# Constants
SYMBOLS_SET = "!@#$%_-.+?"
LOWERCASE_SET = string.ascii_lowercase
UPPERCASE_SET = string.ascii_uppercase
DIGITS_SET = string.digits
SALT_LENGTH = 42                        # salt character length (~256 bits of entropy)

# Main function
def main():
    user_input = ""
    
    print("(1) Hash text")
    print("(2) Hash a file")
    print("(0) Exit")

    user_input = input("Select an option: ").strip()

    if user_input == '1':
        hash_text()
    elif user_input == '2':
        hash_file()
    elif user_input == '0':
        return
    else:
        console.print("[red]INVALID INPUT[/]")

def hash_text():
    """
    hash_text - hashes plaintext
    """

    # function lookup table for hashing algorithms
    hashing_algorithms = {
        "md5": md5_text,
        "sha1": sha1_text,
        "sha256": sha256_text,
        "sha512": sha512_text,
        "sha3_256": sha3_256_text,
        "sha3_512": sha3_512_text
    }

    # function lookup table for encoding types (binary to text)
    encoding_types = {
        "hex": hex_encode,
        "base64": base64_encode
    }

    plaintext = ""      # text to be hashed
    algorithm = ""      # which hashing algorithm to use
    hide = ""           # option to hide input
    has_salt = ""       # if text has salt
    salt = ""           # generated salt
    output = ""         # encoding type (hex/base64)
    hasher = None       # hash object
    hash_value = ""     # hash in string

    # input validation
    while True:
        hide = input("Hide input (Y/N)? ").strip().upper()

        if hide == 'Y':
            plaintext = getpass("Enter text: ")         # user input's hidden
            while plaintext == "":                      # plaintext cannot be blank
                console.print("[red]INVALID INPUT[/]")
                plaintext = getpass("Enter text: ")
            break
        elif hide == 'N':
            plaintext = input("Enter text: ")           # user inputs in plaintext
            while plaintext == "":
                console.print("[red]INVALID INPUT[/]")
                plaintext = input("Enter text: ")
            break
        else:
            console.print("[red]INVALID INPUT[/]")

    # input validation
    while True:
        has_salt = input("Add a salt (Y/N)? ").strip().upper()      # this enhances the flavor of your dish by suppressing bitterness (a.k.a. rainbow tables — which probably came from the nyan cat)

        if has_salt == 'Y':
            salt = generate_salt()
            break
        elif has_salt == 'N':
            break
        else:
            console.print("[red]INVALID INPUT[/]")

    # input validation
    while True:
        algorithm = input("Algorithm (md5/sha1/sha256/sha512/sha3_256/sha3_512):").strip().lower()

        if algorithm in hashing_algorithms:                         # only use function if it's a valid hashing algorithm
            hasher = hashing_algorithms[algorithm](plaintext, salt)
            break
        else:
            console.print("[red]INVALID INPUT[/]")
    

    # input validation
    while True:
        output = input("Output format (hex/base64): ").strip().lower()
    
        if output in encoding_types:                                # only use function if it's a valid encoding type
            hash_value = encoding_types[output](hasher)
            break
        else:
            console.print("[red]INVALID INPUT[/]")

    print(f"{algorithm.upper()}: {hash_value}")
    print(f"Salt used: {salt}")

def hash_file():
    """
    hash_file - hashes a file/folder
    """

    user_input = ""     # handles user input when pasting directories

    # function lookup table for hashing algorithms
    hashing_algorithms = {
        "md5": md5_file,
        "sha1": sha1_file,
        "sha256": sha256_file,
        "sha512": sha512_file,
        "sha3_256": sha3_256_file,
        "sha3_512": sha3_512_file
    }

    # function lookup table for encoding types (binary to text)
    encoding_types = {
        "hex": hex_encode,
        "base64": base64_encode
    }

    algorithm = ""      # which hashing algorithm to use
    filepath = ""       # where the file/folder is
    output = ""         # encoding type (hex/base64)
    hasher = None       # hash object
    hash_value = ""     # hash in string

    # check if file/folder exists
    while True:
        user_input = input("Enter filepath: ")                      # get raw string first
        filepath = Path(user_input.strip().strip('"').strip("'"))   # removes leading/trailing whitespace/newlines and surrounding Windows quotes when using "Copy as path"
        
        if filepath.exists():                                       # check if file/folder exists on disk
            break                                                   # exit loop when a valid path is found
        else:
            console.print("[red]Path not found.[/]")

    # input validation
    while True:
        algorithm = input("Algorithm (md5/sha1/sha256/sha512/sha3_256/sha3_512):").strip().lower()

        if algorithm in hashing_algorithms:                         # only use function if it's a valid hashing algorithm
            hasher = hashing_algorithms[algorithm](filepath)
            break
        else:
            console.print("[red]INVALID INPUT[/]")

    # input validation
    while True:
        output = input("Output format (hex/base64): ").strip().lower()
    
        if output in encoding_types:                                # only use function if it's a valid encoding type
            hash_value = encoding_types[output](hasher)
            break
        else:
            console.print("[red]INVALID INPUT[/]")

    print(f"{algorithm.upper()}: {hash_value}")

def generate_salt():
    """
    generate_salt - generates a 42-character salt (~256 bits of entropy)
    """

    characters = SYMBOLS_SET + LOWERCASE_SET + UPPERCASE_SET + DIGITS_SET   # combines all of these characters into one string
    return "".join(secrets.choice(characters) for _ in range(SALT_LENGTH))  # returns the 42-character string

def md5_text(plaintext, salt):
    """
    md5_text - md5 hashing algorithm
    plaintext - text to be hashed
    salt - generated salt
    """

    hasher = hashlib.md5()              # create new hash object using md5 hashing algorithm
    hasher.update(plaintext.encode())   # feed plaintext into hash state
    hasher.update(salt.encode())        # feed salt (if any) into hash state

    return hasher

def sha1_text(plaintext, salt):
    """
    sha1_text - sha1 hashing algorithm
    plaintext - text to be hashed
    salt - generated salt
    """

    hasher = hashlib.sha1()
    hasher.update(plaintext.encode())
    hasher.update(salt.encode())

    return hasher

def sha256_text(plaintext, salt):
    """
    sha256_text - sha256 hashing algorithm
    plaintext - text to be hashed
    salt - generated salt
    """

    hasher = hashlib.sha256()
    hasher.update(plaintext.encode())
    hasher.update(salt.encode())

    return hasher

def sha512_text(plaintext, salt):
    """
    sha512_text - sha512 hashing algorithm
    plaintext - text to be hashed
    salt - generated salt
    """

    hasher = hashlib.sha512()
    hasher.update(plaintext.encode())
    hasher.update(salt.encode())

    return hasher

def sha3_256_text(plaintext, salt):
    """
    sha3_256_text - sha3_256 hashing algorithm
    plaintext - text to be hashed
    salt - generated salt
    """

    hasher = hashlib.sha3_256()
    hasher.update(plaintext.encode())
    hasher.update(salt.encode())

    return hasher

def sha3_512_text(plaintext, salt):
    """
    sha3_512_text - sha3_512 hashing algorithm
    plaintext - text to be hashed
    salt - generated salt
    """

    hasher = hashlib.sha3_512()
    hasher.update(plaintext.encode())
    hasher.update(salt.encode())

    return hasher

def md5_file(filepath):
    """
    md5_file - md5 hashing algorithm
    filepath - where the file/folder is
    """
    
    hasher = hashlib.md5()

    with open(filepath, "rb") as file:      # open the file and read it as raw bytes
        while chunk := file.read(4096):     # read it by chunk because files can be MASSIVE (4096 bytes), keep grabbing these chunks until there are no more
            hasher.update(chunk)            # send chunks into the hasher

    return hasher

def sha1_file(filepath):
    """
    sha1_file - sha1 hashing algorithm
    filepath - where the file/folder is
    """
    
    hasher = hashlib.sha1()

    with open(filepath, "rb") as file:
        while chunk := file.read(4096):
            hasher.update(chunk)

    return hasher

def sha256_file(filepath):
    """
    sha256_file - sha256 hashing algorithm
    filepath - where the file/folder is
    """
    
    hasher = hashlib.sha256()

    with open(filepath, "rb") as file:
        while chunk := file.read(4096):
            hasher.update(chunk)

    return hasher


def sha512_file(filepath):
    """
    sha512_file - sha512 hashing algorithm
    filepath - where the file/folder is
    """
    
    hasher = hashlib.sha512()

    with open(filepath, "rb") as file:
        while chunk := file.read(4096):
            hasher.update(chunk)

    return hasher


def sha3_256_file(filepath):
    """
    sha3_256_file - sha3_256 hashing algorithm
    filepath - where the file/folder is
    """
    
    hasher = hashlib.sha3_256()

    with open(filepath, "rb") as file:
        while chunk := file.read(4096):
            hasher.update(chunk)

    return hasher


def sha3_512_file(filepath):
    """
    sha3_512_file - sha3_512 hashing algorithm
    filepath - where the file/folder is
    """
    
    hasher = hashlib.sha3_512()

    with open(filepath, "rb") as file:
        while chunk := file.read(4096):
            hasher.update(chunk)

    return hasher

def hex_encode(hasher):
    """
    hex_encode - hash output in hex
    hasher - hash object
    """
    
    return hasher.hexdigest()

def base64_encode(hasher):
    """
    base64_encode - hash output in base64
    hasher - hash object
    """
    
    raw_digest = None       # binary hash (in bytes)
    base64_bytes = None     # base64 hash (in bytes)

    raw_digest = hasher.digest()                    # hash into binary bytes
    base64_bytes = base64.b64encode(raw_digest)     # binary bytes into base64 bytes
    return base64_bytes.decode()                    # finished output after byte to str conversion

# dunder name guard
if __name__ == "__main__":
    main()