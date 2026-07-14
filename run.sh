#!/usr/bin/env bash
# Jeffar - run.sh
# Description - bash launcher that checks for updates, then starts the toolkit.
# Created - 2026-07-13
# Last updated - 2026-07-13

cd "$(dirname "$0")"                                # move into the repo folder (where this script lives)

# build the venv and install dependencies only if .venv is missing
if [ ! -d ".venv" ]; then
    python -m venv .venv                    # create the virtual environment
    source .venv/bin/activate               # activate it
    pip install -r requirements.txt         # install dependencies
else
    source .venv/bin/activate               # venv already exists, just activate it
fi

python updater.py                                   # check for updates
read -n 1 -s -r -p "Press any key to continue..."   # pause
python main.py                                      # launch the toolkit