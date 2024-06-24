#!/usr/bin/env python

"""
Script Name: server.py
Author: Brayden Chan
Date Created: 2023-08-24
Date Modified: 2024-06-23
Description: A script to set up and manage Minecraft servers.

Dependencies:
    - Python 3.6+
    - tmux
    - 7z (or tar if compressing to any .tar.* file)

Version: 2.3

License: This file is licensed under the MIT License. See LICENSE for more information.

Contact Information:
    - GitHub: https://github.com/megabyte6
"""

import os
import shutil
import stat
import subprocess
import sys
from argparse import ArgumentParser
from datetime import datetime


def add_scripts(server_name):
    """
    Add custom scripts to the server directory.

    Args:
        server_name (str): The name of the server to add the scripts to.
    """

    if sys.executable.endswith("python3"):
        python_executable = "python3"
    else:
        python_executable = "python"

    update_script = (
        f"#!/usr/bin/env {python_executable}\n\n"
        """
import json
import os
import sys
import urllib.request
from argparse import ArgumentParser


def fetch_json(url: str):
    \"""
    Fetch and parse JSON from a given URL.

    Args:
        url (str): The URL to fetch JSON from.

    Returns:
        The parsed JSON.
    \"""

    with urllib.request.urlopen(url) as response:
        return json.load(response)


parser = ArgumentParser(description="Update a PaperMC Minecraft server JAR.")
parser.add_argument(
    "--mc-version",
    default=None,
    help="Specify the Minecraft version. Default is the latest available version.",
)
parser.add_argument(
    "--papermc-build",
    type=int,
    default=None,
    help="Specify the PaperMC build version. Default is the latest available build.",
)
parser.add_argument(
    "--check-latest",
    choices=["all", "mc-version", "papermc-build"],
    help="Check the latest Minecraft version or the latest PaperMC build",
)
parser.add_argument(
    "--quiet",
    action="store_true",
    help="Suppress output",
)

args = parser.parse_args()

# Find the latest Minecraft version if it is not specified.
if not args.mc_version:
    mc_versions_url = "https://api.papermc.io/v2/projects/paper"
    args.mc_version = fetch_json(mc_versions_url)["versions"][-1]

# Find the latest PaperMC build if it is not specified.
if not args.papermc_build:
    papermc_builds_url = f"https://api.papermc.io/v2/projects/paper/versions/{args.mc_version}/builds"
    args.papermc_build = fetch_json(papermc_builds_url)["builds"][-1]["build"]


# Check if the user wants to know both or just the latest Minecraft version or the latest PaperMC build.
if args.check_latest:
    if args.check_latest == "mc-version":
        print(args.mc_version)
    elif args.check_latest == "papermc-build":
        print(args.papermc_build)
    else:
        print(f"Latest build for Minecraft {args.mc_version} is version {args.papermc_build}")
    sys.exit()


# Find JAR name for download link.
jar_url = f"https://api.papermc.io/v2/projects/paper/versions/{args.mc_version}/builds/{args.papermc_build}"
jar_name = fetch_json(jar_url)["downloads"]["application"]["name"]

download_url = f"https://api.papermc.io/v2/projects/paper/versions/{args.mc_version}/builds/{args.papermc_build}/downloads/{jar_name}"

# Check if the latest build is already downloaded.
if os.path.isfile(jar_name):
    if not args.quiet:
        print(f"You are already on the latest build for Minecraft {args.mc_version}")
    sys.exit()

# Delete old JAR.
for file in os.listdir():
    if file.startswith("paper") and file.endswith(".jar"):
        if not args.quiet:
            print(f"Deleting old JAR: {file}")
        os.remove(file)

# Download the latest build of PaperMC.
if not args.quiet:
    print(f"Downloading PaperMC {args.mc_version} build {args.papermc_build}...")
with urllib.request.urlopen(download_url) as response, open(jar_name, "wb") as f:
    f.write(response.read())
""".lstrip(
            "\n"
        )
    )

    update_script_path = os.path.join(server_name, "update.py")
    with open(update_script_path, "w") as f:
        f.write(update_script)
    if not is_windows():
        # Make the script executable.
        os.chmod(update_script_path, os.stat(update_script_path).st_mode | stat.S_IEXEC)

    if is_windows():
        mc_version = (
            subprocess.run(
                ["py", os.path.join(".", server_name, "update.py"), "--check-latest", "mc-version"],
                stdout=subprocess.PIPE,
            )
            .stdout.decode()
            .strip()
        )
    else:
        mc_version = (
            subprocess.run(
                [os.path.join(".", server_name, "update.py"), "--check-latest", "mc-version"], stdout=subprocess.PIPE
            )
            .stdout.decode()
            .strip()
        )
    start_script = f"""
#!/usr/bin/env {python_executable}

import glob
import os.path
import subprocess
import sys

# Check if there is an update and if so, update the server JAR.
update_args = [os.path.join(".", "update.py"), "--mc-version", "{mc_version}"]
if "win" in sys.platform:
    update_args.insert(0, "py")
subprocess.run(update_args)

# Start PaperMC.
papermc_jar = glob.glob("paper*.jar")[0]
subprocess.run(["java", "-Xms512M", "-Xmx4G", "-jar", papermc_jar, "nogui"])
""".lstrip(
        "\n"
    )

    start_script_path = os.path.join(server_name, "start.py")
    with open(start_script_path, "w") as f:
        f.write(start_script)
    if not is_windows():
        # Make the script executable.
        os.chmod(start_script_path, os.stat(start_script_path).st_mode | stat.S_IEXEC)


def is_windows():
    return "win" in sys.platform


def is_macos():
    return sys.platform == "darwin"


def is_linux():
    return sys.platform == "linux"


if not is_windows() and not is_macos() and not is_linux():
    print("Unsupported operating system.")
    exit(1)

compression_file_extensions = {
    "7z": "7z",
    "gzip": "tar.gz",
    "bzip2": "tar.bz2",
    "xz": "tar.xz",
    "lzip": "tar.lz",
    "lzma": "tar.lzma",
    "lzop": "tar.lzo",
    "zstd": "tar.zst",
    "compress": "tar.Z",
}

parser = ArgumentParser(description="Setup or backup a Minecraft server.")

parser.add_argument(
    "server_name", nargs="?", help="The name of the Minecraft server to create or perform the action on"
)

parser.add_argument("-y", action="store_true", help="Answer yes to all prompts")
if is_linux():
    parser.add_argument(
        "-s", "--session", action="store_true", help="Continue or start a Minecraft server's console session"
    )

server_options = parser.add_mutually_exclusive_group()
server_options.add_argument("-n", "--new", action="store_true", help="Create a new server")
server_options.add_argument("-b", "--backup", action="store_true", help="Backup an existing server")
server_options.add_argument("-d", "--delete", action="store_true", help="Delete an existing server")

if is_linux():
    parser.add_argument("--list-sessions", action="store_true", help="List all running Minecraft server sessions")
parser.add_argument(
    "--compression",
    choices=compression_file_extensions.keys(),
    default="7z",
    help="Specify the compression type. Uses '7z' by default. Requires '-b' or '--backup' to be used.",
)
parser.add_argument(
    "--world-name",
    default="world",
    help="Specify the world name as is in server.properties. Only needs to be set if the world save name is not the default.",
)

args = parser.parse_args()

# Print usage example if no arguments are passed.
if len(sys.argv) == 1:
    parser.print_usage()
    print("run with '-h' to get help")
    sys.exit()

if is_linux() and args.list_sessions:
    sessions = subprocess.run(
        [
            "tmux",
            "ls",
            "-F",
            "#{session_name}: #{session_windows} windows (created #{t:session_created}) (#{?session_attached,attached,not attached})",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # No sessions found would result in an error.
    if sessions.stderr.decode():
        print("No sessions found.")
    else:
        print(sessions.stdout.decode())

    sys.exit()

if args.new:
    # Check if the server given exists.
    if os.path.exists(args.server_name):
        print(f"A server with the name '{args.server_name}' already exists.")
        sys.exit(1)

    # Create the server directory and add the custom scripts.
    os.makedirs(args.server_name, exist_ok=True)
    add_scripts(args.server_name)

elif args.backup:
    # Check if the server given exists.
    if not os.path.exists(args.server_name):
        print(f"A server with the name '{args.server_name}' does not exist.")
        print("Please check the spelling and try again.")
        sys.exit(1)

    # Define the backup location.
    if args.server_name[-1] in ["/", "\\"]:
        args.server_name = args.server_name[:-1]

    os.chdir(args.server_name)

    world_saves = [
        args.world_name,
        f"{args.world_name}_nether",
        f"{args.world_name}_the_end",
    ]
    # Make sure the world save directories exist.
    for directory in world_saves:
        if not os.path.exists(directory):
            print(f"Could not find a world save at '{directory}' in '{args.server_name}'.")
            sys.exit(1)

    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_directory = "backup"
    os.makedirs(backup_directory, exist_ok=True)
    backup_path = os.path.join(backup_directory, f"{current_date}.{compression_file_extensions[args.compression]}")

    if args.compression == "7z":
        subprocess.run(["7z", "a", backup_path, *world_saves])
    else:
        subprocess.run(["tar", "--create", "--verbose", "--auto-compress", "--file", backup_path, *world_saves])

    os.chdir("..")

elif args.delete:
    # Check if the server given exists.
    if not os.path.exists(args.server_name):
        print(f"A server with the name '{args.server_name}' does not exist.")
        print("Please check the spelling and try again.")
        sys.exit(1)

    try:
        delete_confirmation = input(
            f"Are you sure you want to delete '{args.server_name}'? This will delete the server backups as well. (y/N): "
        )
    except KeyboardInterrupt:
        sys.exit()
    if not args.y and delete_confirmation.lower() not in ["y", "yes"]:
        sys.exit()

    # Delete the server directory.
    shutil.rmtree(args.server_name)

    sys.exit()

if is_linux() and args.session:
    # The tmux id should not contain any slashes.
    if args.server_name[-1] in ["/", "\\"]:
        args.server_name = args.server_name[:-1]
    tmux_id = f"mc-{args.server_name}"

    # Check if the server name given exists.
    if not os.path.exists(args.server_name):
        print(f"A server with the name '{args.server_name}' does not exist.")
        if args.server_name.startswith("mc-"):
            print(f"Did you mean './server.py -s {args.server_name[3:]}'?")
        sys.exit(1)

    # Check if the server is already running.
    tmux_sessions = subprocess.run(["tmux", "ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if tmux_id in tmux_sessions.stdout.decode():
        subprocess.run(["tmux", "attach", "-t", tmux_id])
    else:
        os.chdir(args.server_name)

        # Use systemd-run to run tmux as a user process to prevent it from being killed when the user logs out.
        # If this is a new server, run 'loginctl enable-linger' to allow the process to stay active even if all users log off.
        subprocess.run(["systemd-run", "--scope", "--user", "tmux", "new", "-s", tmux_id])
