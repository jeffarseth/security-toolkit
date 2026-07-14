#!/usr/bin/env bash
# Jeffar - run.sh
# Description - bash launcher that checks for updates, then starts the toolkit.
# Created - 2026-07-13
# Last updated - 2026-07-13

cd "$(dirname "$0")"                                # move into the repo folder (where this script lives)
source .venv/bin/activate                           # activate the virtual environment
python updater.py                                   # check for updates
read -n 1 -s -r -p "Press any key to continue..."   # pause
python main.py                                      # launch the toolkit