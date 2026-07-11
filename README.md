# Security Toolkit

A modular command-line security toolkit in Python: password auditing, hashing, and port scanning.

> **Note:** This project is under active development. Tools are being built one module at a time. See the [Roadmap](#roadmap) for current status.

## Overview

A collection of command-line tools for common security tasks, built entirely on Python's standard library (no third-party dependencies for the core tools). Each tool is self-contained and independently usable, with a shared `utils/` layer for common helpers.

This toolkit is intended for **learning and authorized security testing only**. See [Responsible Use](#responsible-use) before running the port scanner.

## Features

### Password Tool
- **Strength checker** - scores a password against length, uppercase, lowercase, digit, and symbol rules, and reports exactly what's missing. Includes common-password detection to check a candidate against a list of 100k+ known-common passwords using an O(1) set lookup.
- **Generator** - produce strong random passwords using Python's `secrets` module (cryptographically secure, unlike `random`), with basic and advanced modes.

### Hash Tool
- Generate hashes (MD5, SHA-1, SHA-256, SHA-512, SHA3-256, SHA3-512) of text or files.
- Salting support, with hex or base64 output.
- Compare two known hashes directly, with optional case-insensitive comparison.

### Port Scanner
- Scan a target across quick (common ports), full (0–65535), custom range, or custom selection of individual ports.
- Configurable connection timeout and thread count for concurrent scanning (capped for system stability).
- Multithreaded scanning via `ThreadPoolExecutor` - significantly faster on large port ranges or slow/filtered targets.
- Banner grabbing on open ports - captures service identification strings where available.
- Service detection and a summary report (ports scanned, open/closed counts, time taken).

## Installation

Requires Python 3.11 or newer.

```bash
git clone https://github.com/jeffarseth/security-toolkit.git
cd security-toolkit
```

The core tools use only the standard library, so there's nothing to install. To run the test suite:

```bash
pip install -r requirements.txt   # installs pytest
```

## Usage

Run the password tool's unified menu from the repo root:

```bash
python -m password_tool.cli
```

Example:

```
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

A repo-root `main.py` that dispatches across password, hash, and scan tools is planned (see Roadmap).

## Roadmap

- [x] Password strength checker
- [x] Common-password set lookup
- [x] Password generator (basic + advanced)
- [x] Password tool CLI (check + generate menu)
- [x] Hash generator (generate, salt, hex/base64)
- [x] Hash comparison tool
- [x] Hash tool CLI (unified generate + compare menu)
- [x] Port scanner
- [ ] Unified `main.py` entry point (dispatches password / hash / scan)
- [ ] Shared `utils/` layer
- [ ] Unit tests

## Responsible Use

The port scanner is designed to scan **only `localhost` and hosts you are explicitly authorized to test**. Scanning systems you do not own or have permission to assess may be illegal depending on your jurisdiction. Use these tools ethically and within the law.

## Credits

The common-password wordlist in `data/passwords.txt` is sourced from [SecLists](https://github.com/danielmiessler/SecLists), used under the MIT License. See `data/NOTICE.txt` for full attribution.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
