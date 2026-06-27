- basic password generator (doesn't ask anything), (automatically generates a 16-character password), (quick)
- advanced password generator (asks length [greater than 1]), (option to include lowercase, uppercase, numbers, symbols), (how many passwords if more than 1 [separated by newline])
- password generator uses 10 highly-compatible symbols !@#$%_-.+?

- combine password_checker and password_generator and name the program "password tool"

- hash generator (MD5, SHA-1, SHA-256, SHA-512, SHA3-256, SHA3-512)
- hash generator can use text or file

- hash generator + salt (print what salt was used)
- hash generator + salt option to use hex or base64

- hash comparison tool (use previous hash generator program)
- hash comparion tool can use text or file
- hash comparison tool option to ignore case on text

- combine hash generator and comparison tool and name the program "hash tool"

- port scanner tool (asks target [e.g. scanme.nmap.org])
- port scanner tool option for port range (quick scan for common ports, full scan for 0-65535, or custom range like 0-1023)
- port scanner tool option for timeout (in milliseconds)
- port scanner tool detects service
- port scanner tool prints total ports scanned, total ports open/closed, time taken (e.g. 3.14 seconds)

DONE:
- password_checker checks common passwords ("passwords.txt") using hash table lookup O(1)
- password_checker option to show password input or hide using getpass