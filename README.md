# Security Toolkit

A modular command-line security toolkit in Python: password auditing, hashing, and port scanning.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-in%20development-orange)

> **Note:** This project is under active development. Tools are being built one module at a time — see the [Roadmap](#roadmap) for current status.

## Overview

A collection of command-line tools for common security tasks, built entirely on Python's standard library (no third-party dependencies for the core tools). Each tool is self-contained and independently usable, with a shared `utils/` layer for common helpers.

This toolkit is intended for **learning and authorized security testing only**. See [Responsible Use](#responsible-use) before running the port scanner.

## Features

### Password Tool
- **Strength checker** — scores a password against length, uppercase, lowercase, digit, and symbol rules, and reports exactly what's missing.
- **Common-password detection** *(planned)* — check a candidate against a list of 100k+ known-common passwords using an O(1) set lookup.
- **Generator** *(planned)* — produce strong random passwords using Python's `secrets` module (cryptographically secure, unlike `random`), with basic and advanced modes.

### Hash Tool *(planned)*
- Generate hashes (MD5, SHA-1, SHA-256, SHA-512, SHA3-256, SHA3-512) of text or files.
- Salting support, with hex or base64 output.
- Compare a value against a known hash, with optional case-insensitive text matching.

### Port Scanner *(planned)*
- Scan a target across quick (common ports), full (0–65535), or custom port ranges.
- Configurable connection timeout.
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

Tools are run directly for now. The password strength checker:

```bash
python password_tool/checker.py
```

Example:

```
PASSWORD CHECKER

Enter a password: Catlover22

Score: 4 / 5
Verdict: Medium
Missing: symbol
```

A unified `main.py` entry point that dispatches to all tools is planned (see Roadmap).

## Roadmap

- [x] Password strength checker
- [ ] Common-password set lookup
- [ ] Password generator (basic + advanced)
- [ ] Unified `main.py` CLI dispatcher
- [ ] Hash tool (generate, salt, compare)
- [ ] Port scanner (quick / full / custom, service detection)
- [ ] Shared `utils/` layer
- [ ] Unit tests

## Responsible Use

The port scanner is designed to scan **only `localhost` and hosts you are explicitly authorized to test**. Scanning systems you do not own or have permission to assess may be illegal depending on your jurisdiction. Use these tools ethically and within the law.

## Credits

The common-password wordlist in `data/passwords.txt` is sourced from [SecLists](https://github.com/danielmiessler/SecLists), used under the MIT License. See `data/NOTICE.txt` for full attribution.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
