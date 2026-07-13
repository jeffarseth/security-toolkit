# Security Toolkit

A modular command-line security toolkit in Python: password auditing, hashing, and port scanning.

> **Note:** This project is under active development. See the [Roadmap](#roadmap) for current status.

## Overview

A collection of command-line tools for common security tasks. Each tool is self-contained and independently usable, and all three are accessible from a single menu-driven entry point.

This toolkit is intended for **learning and authorized security testing only**. See [Responsible Use](#responsible-use) before running the port scanner.

## Features

### Password Tool
- Strength checker that scores a password against length, uppercase, lowercase, digit, and symbol rules, and reports exactly what's missing. Includes common-password detection to check a candidate against a list of 100k+ known-common passwords using an O(1) set lookup.
- Generates strong random passwords using the `secrets` module (cryptographically secure, unlike `random`), with basic and advanced modes.

### Hash Tool
- Generate hashes (MD5, SHA-1, SHA-256, SHA-512, SHA3-256, SHA3-512) of text or files.
- Salting support, with hex or base64 output.
- Compare two known hashes directly, with optional case-insensitive comparison.

### Port Scanner
- Scan a target across quick (common ports), full (0-65535), custom range, or custom selection of individual ports.
- TCP and UDP scanning, with three-state UDP reporting (open / open|filtered / closed).
- Configurable connection timeout and thread count for concurrent scanning.
- Multithreaded scanning via `ThreadPoolExecutor`, significantly faster on large port ranges or slow/filtered targets.
- Banner grabbing on open ports.
- Service detection and a summary report (ports scanned, open/closed counts, time taken).
- Export results to text, JSON, or CSV.

## Installation

Requires Python 3.11 or newer.

```bash
git clone https://github.com/jeffarseth/security-toolkit.git
cd security-toolkit
pip install -r requirements.txt
```

Installing dependencies is required. The toolkit uses [`rich`](https://github.com/Textualize/rich) for terminal styling and [`pyfiglet`](https://github.com/pwaller/pyfiglet) for the banner.

## Usage

Run the whole toolkit from the repo root:

```bash
python main.py
```

Example:

```
SECURITY TOOLKIT

(1) Password Tool
(2) Hash Tool
(3) Port Scanner
(0) Exit
Select option: 1

PASSWORD TOOL

(1) Check a password
(2) Generate a password
(0) Exit
Select option: 1

PASSWORD CHECKER

Enter a password: Jeffarisapoopyhead123

Score: 4 / 5
Verdict: Medium
Missing: symbol
```

## Roadmap

- [x] Password strength checker
- [x] Password generator
- [x] Password tool CLI
- [x] Hash generator
- [x] Hash comparison tool
- [x] Hash tool CLI
- [x] Port scanner
- [x] Unified `main.py` entry point
- [x] Unit tests (pytest)

## Responsible Use

The port scanner is designed to scan **only `localhost` and hosts you are explicitly authorized to test**. Scanning systems you do not own or have permission to assess may be illegal depending on your jurisdiction. Use these tools ethically and within the law.

## Credits

The common-password wordlist in `data/passwords.txt` is sourced from [SecLists](https://github.com/danielmiessler/SecLists), used under the MIT License. See `data/NOTICE.txt` for full attribution.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
