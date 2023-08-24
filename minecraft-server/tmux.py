#!/usr/bin/env python3

import os
import subprocess
import sys

# Check if args were passed
if len(sys.argv) == 1:
    subprocess.run(
        [
            "tmux",
            "ls",
            "-F",
            "#{session_name}: #{session_windows} windows (created #{t:session_created}) (#{?session_attached,attached,not attached})",
        ]
    )
    sys.exit(0)

server_name = sys.argv[1]

if server_name[-1] in ["/", "\\"]:
    server_name = server_name[:-1]

# Check if the server name given exists.
tmux_id = f"mc-{server_name}"
tmux_sessions = subprocess.run(["tmux", "ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if tmux_id in tmux_sessions.stdout.decode():
    subprocess.run(["tmux", "attach", "-t", tmux_id])
else:
    os.chdir(server_name)

    # Use systemd-run to run tmux as a user process to prevent it from being killed when the user logs out.
    # If this is a new server, run 'loginctl enable-linger' to allow the process to stay active even if all users log
    # off.
    subprocess.run(["systemd-run", "--scope", "--user", "tmux", "new", "-s", tmux_id])
