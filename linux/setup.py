# !/usr/bin/env python3

import sys
import os

flatpak_setup = [
    "flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo",
    "flatpak install flathub -y com.github.tchx84.Flatseal",
    "flatpak install flathub -y com.google.Chrome",
    "flatpak install flathub -y com.jetbrains.IntelliJ-IDEA-Community",
    "flatpak install flathub -y com.visualstudio.code",
    "flatpak install flathub -y com.discordapp.Discord",
    "flatpak install flathub -y com.atlauncher.ATLauncher",
    "flatpak install flathub -y com.spotify.Client",
    "flatpak install flathub -y md.obsidian.Obsidian",
    "flatpak install flathub -y org.gimp.GIMP",
    "flatpak install flathub -y com.gluonhq.SceneBuilder",
    "flatpak install flathub -y com.protonvpn.www",
]

commands = {
    "ubuntu": {
        "upgrade": [
            "sudo apt update",
            "sudo apt upgrade -y",
        ],
        "setup": [
            "sudo apt install -y htop neofetch neovim git httpie nala flatpak gnome-software-plugin-flatpak",
            *flatpak_setup,
        ],
    },
    "kubuntu": {
        "upgrade": [
            "sudo apt update",
            "sudo apt upgrade -y",
        ],
        "setup": [
            "sudo apt install -y htop neofetch neovim git httpie nala flatpak plasma-discover-backend-flatpak",
            *flatpak_setup,
        ],
    },
    "raspberry pi os": {
        "upgrade": [
            "sudo apt update",
            "sudo apt upgrade -y",
        ],
        "setup": [
            "sudo apt install -y htop neofetch neovim git httpie nala flatpak",
            *flatpak_setup,
        ],
    },
    "fedora": {
        "upgrade": [
            "sudo dnf upgrade -y",
        ],
        "setup": [
            "sudo dnf install -y htop neofetch neovim git httpie",
            *flatpak_setup,
        ],
    },
    "opensuse": {
        "upgrade": [
            "sudo zypper update",
        ],
        "setup": [
            "sudo zypper install -y htop neofetch neovim git httpie flatpak",
            *flatpak_setup,
        ],
    },
}


def print_help():
    print(
        f"""
A setup script used to set up or update a Linux OS after installing.

Usage:
    ./setup.py <[--os] <String>> [--upgrade] [--setup] [--no-install]
    ./setup.py --help

Options:
    --os <os>: The OS to target.
        can be one of {list(commands.keys())}
    --upgrade: Update/upgrade the OS.
    --setup: Setup the OS and install packages and apps.

Example:
    ./setup.py --os ubuntu --action upgrade
    ./setup.py "raspberry pi os"
    ./setup.py --os fedora --action setup --no-install
        """
    )


def invalid_argument(message: str):
    print(message)
    print("Try './setup.py --help' for more information.")
    sys.exit(0)


def update_os():
    for command in commands[arguments["--os"]]["upgrade"]:
        if arguments["--no-install"]:
            print(command)
        else:
            os.system(command)


def setup_os():
    # Make sure the OS us updated before setup
    update_os()

    for command in commands[arguments["--os"]]["setup"]:
        if arguments["--no-install"]:
            print(command)
        else:
            os.system(command)


arguments = {
    "--os": None,
    "--action": "help",
    "-—no-install": False,
}

if len(sys.argv) == 1:
    invalid_argument("Missing target OS")

for i, arg in enumerate(sys.argv):
    # Skip first argument because it is the script name
    if i == 0:
        continue

    if arg == "-h" or arg == "--help":
        print_help()
        sys.exit(0)

    if arg == "--os":
        if i + 1 >= len(sys.argv):
            invalid_argument("No OS specified after '--os' flag.")
        arguments["--os"] = sys.argv[i + 1]
    elif arg == "-s" or arg == "--setup":
        arguments["--action"] = "setup"
    elif arg == "-u" or arg == "--upgrade":
        arguments["--action"] = "upgrade"
    elif arg == "--no-install":
        arguments["--no-install"] = True
    else:
        # If no flag is passed, assume it is the OS to target
        arguments["--os"] = arg

# Perform some checks on the arguments passed
if arguments["--os"] is None:
    invalid_argument("No OS specified")

arguments["--os"] = arguments["--os"].lower()

if arguments["--no-install"]:
    print(
        "No installation will be performed. But here are the commands that would be run:",
        end="\n\n",
    )

# Run the commands
if arguments["--action"] == "upgrade":
    update_os()
else:
    # The default action is 'setup'
    setup_os()
