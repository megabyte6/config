#!/usr/bin/env python3

import argparse
import subprocess

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

os_commands = {
    "ubuntu": {
        "upgrade": [
            "sudo apt update",
            "sudo apt upgrade -y",
        ],
        "setup": [
            "sudo apt install -y htop neofetch neovim git httpie nala flatpak gnome-software-plugin-flatpak",
            *flatpak_setup,
        ],
        "terminal games": [
            "sudo apt install -y bastet pacman4console nsnake 2048 nudoku moon-buggy ninvaders greed bsdgames",
            "sudo apt install -y snapd",
            "snap install ascii-patrol",
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
        "terminal games": [
            "sudo apt install -y bastet pacman4console nsnake 2048 nudoku moon-buggy ninvaders greed bsdgames",
            "sudo apt install -y snapd",
            "snap install ascii-patrol",
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
        "terminal games": [
            "sudo apt install -y bastet pacman4console nsnake 2048 nudoku moon-buggy ninvaders greed bsdgames",
            "sudo apt install -y snapd",
            "snap install ascii-patrol",
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
        "terminal games": [
            "sudo dnf install -y bastet pacman4console nsnake 2048-cli nudoku moon-buggy ninvaders greed bsdgames",
            "sudo dnf install -y snapd",
            "snap install ascii-patrol",
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
        "terminal games": [
            "echo No games listed for openSUSE",
        ],
    },
}


def execute_commands(commands: list, no_install: bool = False):
    if no_install:
        for command in commands:
            print(command)
    else:
        for command in commands:
            subprocess.run(command)


parser = argparse.ArgumentParser(
    description="A setup script used to set up or update a Linux OS after installing."
)

parser.add_argument("os", choices=os_commands, help=f"the OS to target")
parser.add_argument(
    "--only-upgrade",
    action="store_true",
    help="only update/upgrade the OS and do not install setup packages and apps",
)
parser.add_argument(
    "--install-terminal-games", action="store_true", help="install fun terminal games"
)
parser.add_argument(
    "--no-install",
    action="store_true",
    help="list what commands would be run but do not install any packages or apps",
)

args = parser.parse_args()

# Perform some preprocessing on the arguments passed
args.os = args.os.lower()

if args.no_install:
    print(
        "No installation will be performed. But here are the commands that would be run:",
        end="\n\n",
    )

# Run update/upgrade command regardless of the arguments passed as all cases
# require this to be run
execute_commands(
    commands=os_commands[args.os]["upgrade"],
    no_install=args.no_install,
)

# Run setup command only if '--only-upgrade' was not passed
if not args.only_upgrade:
    execute_commands(
        commands=os_commands[args.os]["setup"],
        no_install=args.no_install,
    )

if args.install_terminal_games:
    execute_commands(
        commands=os_commands[args.os]["terminal games"],
        no_install=args.no_install,
    )
