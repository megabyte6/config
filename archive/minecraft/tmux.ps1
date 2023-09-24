#!/usr/bin/env pwsh

# Check if args were passed.
if ($args.Count -eq 0) {
    tmux ls -F "#{session_name}: #{session_windows} windows (created #{t:session_created}) (#{?session_attached,attached,not attached})"
    exit
}

if ($args[0][-1] -eq "/" || $args[0][-1] -eq "\\") {
    $args[0] = $args[0].Substring(0, $args[0].length - 1);
}

# Check if the server given exists.
$tmuxID = "mc-$($args[0])"
if (tmux ls | Select-String -Pattern $tmuxID -Quiet) {
    tmux attach -t $tmuxID
} else {
    Set-Location $args[0]

    # Use systemd-run to run tmux as a user process to prevent it from being
    # killed when the user logs out.
    # If this is a new server, run 'loginctl enable-linger' to allow the
    # process to stay active even if all users log off.
    systemd-run --scope --user tmux new -s $tmuxID
}
