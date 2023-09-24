#!/usr/bin/env python

from argparse import ArgumentParser
from datetime import datetime
from os import chdir, chmod, makedirs, stat
from os.path import exists, join
from stat import S_IEXEC
from subprocess import PIPE, run
from sys import exit


def add_scripts(server_name):
    """
    Add custom scripts to the server directory.
    :param server_name: The name of the server to add the scripts to.
    :return: None
    """

    update_script = """
#!/usr/bin/env python

from argparse import ArgumentParser
from json import load
from os import listdir, remove
from os.path import isfile
from sys import exit
from urllib.request import urlopen


def fetch_json(url: str):
    \"""
    Fetch and parse JSON from a given URL.

    Args:
        url (str): The URL to fetch JSON from.

    Returns:
        The parsed JSON.
    \"""

    with urlopen(url) as response:
        return load(response)


parser = ArgumentParser(description="Update a PaperMC Minecraft server.")
parser.add_argument(
    "--mc-version",
    default="-1",
    help="Specify the Minecraft version. Default is the latest available version.",
)
parser.add_argument(
    "--papermc-build",
    type=int,
    default=-1,
    help="Specify the PaperMC build version. Default is the latest available build.",
)
parser.add_argument(
    "--check-latest",
    choices=["all", "mc-version", "papermc-build"],
    help="Check the latest Minecraft version or the latest PaperMC build.",
)

args = parser.parse_args()

# Find the latest Minecraft version if it is not specified.
if args.mc_version == "-1":
    mc_versions_url = "https://api.papermc.io/v2/projects/paper"
    args.mc_version = fetch_json(mc_versions_url)["versions"][-1]

# Find the latest PaperMC build if it is not specified.
if args.papermc_build == -1:
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
    exit(0)


# Find JAR name for download link.
jar_url = f"https://api.papermc.io/v2/projects/paper/versions/{args.mc_version}/builds/{args.papermc_build}"
jar_name = fetch_json(jar_url)["downloads"]["application"]["name"]

download_url = f"https://api.papermc.io/v2/projects/paper/versions/{args.mc_version}/builds/{args.papermc_build}/downloads/{jar_name}"

# Check if the latest build is already downloaded.
if isfile(jar_name):
    print(f"You are already on the latest build for Minecraft {args.mc_version}")
    exit(0)

# Delete old JAR.
for file in listdir():
    if file.startswith("paper") and file.endswith(".jar"):
        remove(file)

# Download the latest build of PaperMC.
with urlopen(download_url) as response, open(jar_name, "wb") as f:
    f.write(response.read())
""".lstrip(
        "\n"
    )

    update_script_path = join(server_name, "update.py")
    with open(update_script_path, "w") as f:
        f.write(update_script)
    # Make the script executable.
    chmod(update_script_path, stat(update_script_path).st_mode | S_IEXEC)

    start_script = """
#!/usr/bin/env python

from glob import glob
from os.path import join
from subprocess import run

# Check if there is an update and if so, update the server JAR.
run([join(".", "update.py"), "--mc-version", "{mc_version}"])

# Start PaperMC.
papermc_jar = glob("paper*.jar")[0]
run(["java", "-Xms512M", "-Xmx4G", "-jar", papermc_jar, "nogui"])
""".format(
        mc_version=run([join(".", server_name, "update.py"), "--check-latest", "mc-version"], stdout=PIPE)
        .stdout.decode()
        .strip()
    ).lstrip(
        "\n"
    )

    start_script_path = join(server_name, "start.py")
    with open(start_script_path, "w") as f:
        f.write(start_script)
    # Make the script executable.
    chmod(start_script_path, stat(start_script_path).st_mode | S_IEXEC)


parser = ArgumentParser(description="Setup or backup a Minecraft server.")

server_options = parser.add_mutually_exclusive_group()
server_options.add_argument(
    "-s", "--session", action="store_true", help="Continue or start a Minecraft server's console session"
)
server_options.add_argument("-n", "--new", action="store_true", help="Create a new server")
server_options.add_argument("-b", "--backup", action="store_true", help="Backup an existing server")

parser.add_argument(
    "server_name", nargs="?", help="The name of the Minecraft server to create or perform the action on"
)
server_options.add_argument("-d", "--delete", action="store_true", help="Delete an existing server")

parser.add_argument("--list-sessions", action="store_true", help="List all running Minecraft server sessions")

args = parser.parse_args()

if args.list_sessions:
    sessions = run(
        [
            "tmux",
            "ls",
            "-F",
            "#{session_name}: #{session_windows} windows (created #{t:session_created}) (#{?session_attached,attached,not attached})",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    # No sessions found would result in an error.
    if sessions.stderr.decode():
        print("No sessions found.")
    else:
        print(sessions.stdout.decode())

elif args.session:
    # The tmux id should not contain any slashes.
    if args.server_name[-1] in ["/", "\\"]:
        args.server_name = args.server_name[:-1]
    tmux_id = f"mc-{args.server_name}"

    # Check if the server name given exists.
    if not exists(args.server_name):
        print(f"A server with the name '{args.server_name}' does not exist.")
        if args.server_name.startswith("mc-"):
            print(f"Did you mean './server.py -s {args.server_name[3:]}'?")
        exit(1)

    # Check if the server is already running.
    tmux_sessions = run(["tmux", "ls"], stdout=PIPE, stderr=PIPE)
    if tmux_id in tmux_sessions.stdout.decode():
        run(["tmux", "attach", "-t", tmux_id])
    else:
        chdir(args.server_name)

        # Use systemd-run to run tmux as a user process to prevent it from being killed when the user logs out.
        # If this is a new server, run 'loginctl enable-linger' to allow the process to stay active even if all users log off.
        run(["systemd-run", "--scope", "--user", "tmux", "new", "-s", tmux_id])

elif args.new:
    # Check if the server given exists.
    if exists(args.server_name):
        print(f"A server with the name '{args.server_name}' already exists.")
        exit(1)

    # Create the server directory and add the custom scripts.
    makedirs(args.server_name, exist_ok=True)
    add_scripts(args.server_name)

elif args.backup:
    # Check if the server given exists.
    if not exists(args.server_name):
        print(f"A server with the name '{args.server_name}' does not exist.")
        print("Please check the spelling and try again.")
        exit(1)

    # Define the backup location.
    if args.server_name[-1] in ["/", "\\"]:
        args.server_name = args.server_name[:-1]
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_location = join(args.server_name, "backup")
    makedirs(backup_location, exist_ok=True)
    backup_path = join(backup_location, f"{current_date}.tar.xz")

    # Navigate to the server directory.
    chdir(args.server_name)

    run(["tar", "-cvJf", join("..", backup_path), "./world", "./world_nether", "./world_the_end"])

    # Navigate back to the original directory.
    chdir("..")

elif args.delete:
    # Check if the server given exists.
    if not exists(args.server_name):
        print(f"A server with the name '{args.server_name}' does not exist.")
        print("Please check the spelling and try again.")
        exit(1)

    confirm_delete = input(
        f"Are you sure you want to delete '{args.server_name}'? This will delete the server backups as well. (y/N): "
    )
    if confirm_delete.lower() not in ["y", "yes"]:
        exit(0)

    # Delete the server directory.
    run(["rm", "-rf", args.server_name])
