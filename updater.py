# Jeffar - Updater Script
# Description - Checks for and applies updates from the gitHub repo.
# Created - 2026-07-13
# Last updated - 2026-07-13

# Modules
from pathlib import Path            # for filepath
import urllib.request               # for getting github API
import json                         # for reading JSON text
import subprocess                   # for executing commands
from rich.console import Console    # for colors
console = Console()                 # create a console

# Constants
GITHUB_API = "https://api.github.com/repos/jeffarseth/security-toolkit/releases/latest"

def get_local_version():
    """
    get_local_version - reads the current version from the VERSION file
    """

    version_file = Path(__file__).parent / "VERSION"    # VERSION sits next to this script
    version = version_file.read_text().strip()          # read it, strip trailing newline/spaces
    return version

def get_latest_version():
    """
    get_latest_version - asks github for the newest release tag
    """
    with urllib.request.urlopen(GITHUB_API) as response:    # send the request, get the response
        data = response.read()                              # read the raw JSON text (bytes)
        parsed = json.loads(data)                           # turn JSON text into a Python dict
        return parsed["tag_name"]                           # pull out just the version tag

def check_for_update():
    """
    check_for_update - compares local and latest versions, prompt git pull if an update exists
    """
    user_input = ""
    local = get_local_version()                     # should return x.x.x

    try:
        latest = get_latest_version().lstrip('v')       # left strip the 'v' so to return x.x.x
    except Exception:                               # for HTTPError/URLError
        console.print("[red]ERROR - could not check for updates.[/]")
        return

    if local == latest:                             # both versions match
        print(f"Up to date (v{local})")
        return
    else:
        console.print(f"[bold green]Update available: v{local} -> v{latest}[/]")

    # input validation
    while True:
        user_input = input("Install update (Y/n)? ").strip().upper()

        if user_input == "Y" or user_input == "":
            subprocess.run(["git", "pull"])         # pull the latest from gitHub
            print("Updated.")
            return
        elif user_input == "N":
            print("Skipping update.")
            return
        else:
            console.print("[red]INVALID INPUT[/]")

# dunder name guard
if __name__ == "__main__":
    check_for_update()