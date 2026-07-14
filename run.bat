@echo off
:: Jeffar - run.bat
:: Description - batch launcher that checks for updates, then starts the toolkit.
:: Created - 2026-07-13
:: Last updated - 2026-07-13

:: move into this script's own folder (so it works no matter where it's run from)
cd /d "%~dp0"

:: build the venv and install dependencies only if .venv is missing
if not exist ".venv\" (
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

:: check GitHub for a newer release first
python updater.py

pause

:: then launch the toolkit
python main.py