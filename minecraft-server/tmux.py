#!/usr/bin/env python

from argparse import ArgumentParser
from os import chdir
from subprocess import PIPE, run
from sys import exit

parser = ArgumentParser(description="Start or continue the Minecraft server console session.")

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-l", "--list", action="store_true", help="List all running Minecraft server sessions.")
group.add_argument(
    "server_name", nargs="?", help="The directory name of the server to start or continue the console session for."
)

args = parser.parse_args()

if args.list:
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
    if sessions.stderr.decode():
        print("No sessions found.")
    else:
        print(sessions.stdout.decode())
    exit(0)

# The tmux id should not contain any slashes.
if args.server_name[-1] in ["/", "\\"]:
    args.server_name = args.server_name[:-1]

# Check if the server name given exists.
tmux_id = f"mc-{args.server_name}"
tmux_sessions = run(["tmux", "ls"], stdout=PIPE, stderr=PIPE)
if tmux_id in tmux_sessions.stdout.decode():
    run(["tmux", "attach", "-t", tmux_id])
else:
    chdir(args.server_name)

    # Use systemd-run to run tmux as a user process to prevent it from being killed when the user logs out.
    # If this is a new server, run 'loginctl enable-linger' to allow the process to stay active even if all users log off.
    run(["systemd-run", "--scope", "--user", "tmux", "new", "-s", tmux_id])
