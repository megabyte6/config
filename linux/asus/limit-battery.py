#!/usr/bin/env python

import subprocess
import time


def charging_state() -> bool:
    with open("/sys/class/power_supply/BAT0/status", "r") as f:
        state = f.read().strip()
        if state in ["Charging", "Not charging"]:
            return True
        elif state == "Discharging":
            return False
        else:
            raise ValueError(f"Unknown state: {state} in /sys/class/power_supply/BAT0/status")


def get_requested_charge_limit() -> int:
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
    old_state = charging_state()

    while True:
        time.sleep(1)
        new_state = charging_state()

        if old_state == new_state:
            continue

        if new_state:
            set_charge_limit(get_requested_charge_limit())
        else:
            set_charge_limit(100)

        old_state = new_state
