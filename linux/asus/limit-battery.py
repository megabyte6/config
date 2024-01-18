#!/usr/bin/env python

import os
import subprocess
import sys
import time


def already_running(pid_file_path: str) -> bool:
    if os.path.isfile(pid_file_path):
        with open(pid_file_path, "r") as f:
            daemon_pid = int(f.read().strip())
            try:
                os.kill(daemon_pid, 0)
            except OSError:
                return False
            else:
                return True
    else:
        return False


def charging_state() -> bool:
    with open("/sys/class/power_supply/BAT0/status", "r") as f:
        state = f.read().strip()
        if state in ["Charging", "Not charging", "Full"]:
            return True
        elif state == "Discharging":
            return False
        else:
            raise ValueError(
                f"Unknown state: {state} in /sys/class/power_supply/BAT0/status"
            )


def request_charge_limit() -> int:
    option = subprocess.check_output(
        [
            "notify-send",
            "--app-name=Battery Limiter",
            "--action=60%",
            "--action=80%",
            "Do you want to limit the battery charge level?",
        ]
    ).strip()

    if not option:
        return 100
    elif int(option) == 0:
        return 60
    elif int(option) == 1:
        return 80
    else:
        raise ValueError(f"Unknown option: {option}")


def set_charge_limit(charge_limit: int) -> None:
    subprocess.run(
        [
            "sudo",
            "sh",
            "-c",
            f"echo {charge_limit} > /sys/class/power_supply/BAT0/charge_control_end_threshold",
        ]
    )


if __name__ == "__main__":
    pid_file_path = "/tmp/limit-battery.pid"
    if already_running(pid_file_path):
        print("Already running")
        sys.exit(0)

    with open(pid_file_path, "w") as f:
        f.write(str(os.getpid()))

    old_state = charging_state()

    while True:
        time.sleep(1)
        new_state = charging_state()

        if old_state == new_state:
            continue

        if new_state:
            set_charge_limit(request_charge_limit())
        else:
            set_charge_limit(100)

        old_state = new_state
