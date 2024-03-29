# config

## About

`config` is a repo to host my configuration files for things.

### linux

#### asus

| File                                                                                                      | Description                                                                                                                      | Notes                                                                                                              |
| --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| [limit-battery.py](https://raw.githubusercontent.com/megabyte6/config/main/linux/asus/limit-battery.py) | A Python script used to set the battery's charge threshold for ASUS laptops since the MyASUS utility is not available for Linux. | To run, make sure this script is set to auto-run with the system. Then, run `sudo visudo` and add `yourusername ALL=(ALL) NOPASSWD: /bin/sh -c echo * > /sys/class/power_supply/BAT0/charge_control_end_threshold` where yourusername is replaced with your username.
| ~~[limit-battery](https://raw.githubusercontent.com/megabyte6/config/main/archive/linux/asus/limit-battery)~~ | A Python script used to set the battery's charge threshold for ASUS Laptops since the MyASUS utility is not available for Linux. | **Not maintained**<br>To run, copy the file to `/usr/local/bin/` and run `sudo limit-battery <max charge percent>` |

### minecraft

| File                                                                                                   | Description                                                                                                         | Notes                                                                                                                      |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| [server.py](https://raw.githubusercontent.com/megabyte6/config/main/minecraft/server.py)               | A Python script used to simplify the management process of Minecraft Java servers running PaperMC.                  |                                                                                                                            |
| ~~[tmux.py](https://raw.githubusercontent.com/megabyte6/config/main/archive/minecraft/tmux.py)~~       | A Python script used to mange `tmux` sessions for Minecraft servers.                                                | **Not maintained**<br>Replaced by [server.py](https://raw.githubusercontent.com/megabyte6/config/main/minecraft/server.py) |
| ~~[server.ps1](https://raw.githubusercontent.com/megabyte6/config/main/archive/minecraft/server.ps1)~~ | A PowerShell script used to automate the setup and backup processes of a Minecraft Java server set up with PaperMC. | **Not maintained**                                                                                                         |
| ~~[tmux.ps1](https://raw.githubusercontent.com/megabyte6/config/main/archive/minecraft/tmux.ps1)~~     | A PowerShell script used to manage `tmux` sessions for Minecraft servers.                                           | **Not maintained**                                                                                                         |

### nvim

| File                                                                                          | Description              | Notes              |
| --------------------------------------------------------------------------------------------- | ------------------------ | ------------------ |
| [NvChad config](https://github.com/megabyte6/config/blob/main/nvim/lua/custom)                | My NvChad configuration. |                    |
| ~~[init.vim](https://raw.githubusercontent.com/megabyte6/config/main/archive/nvim/init.vim)~~ | My Neovim configuration. | **Not maintained** |

### vscode

| File                                                                                                                          | Description                                                                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [eclipse-java-google-style.xml](https://raw.githubusercontent.com/megabyte6/config/main/vscode/eclipse-java-google-style.xml) | Custom formatter settings for Java in VSCode. Original formatter settings can be found [here](https://raw.githubusercontent.com/google/styleguide/gh-pages/eclipse-java-google-style.xml). |

---

## Not maintained

### linux

| File                                                                                                             | Description                                         | Notes              |
| ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | ------------------ |
| ~~[setup.py](https://raw.githubusercontent.com/megabyte6/config/main/linux/setup.py)~~                           | For setting up new linux installations.             | **Not maintained** |
| ~~[setup.ps1](https://raw.githubusercontent.com/megabyte6/config/main/archive/linux/setup.ps1)~~                 | For setting up new linux installations.             | **Not maintained** |
| ~~[ugreen-driver.ps1](https://raw.githubusercontent.com/megabyte6/config/main/archive/linux/ugreen-driver.ps1)~~ | For installing the drivers for ugreen wifi adapter. | **Not maintained** |

### powershell

| File                                                                                                                                                | Description                                                                                                                 | Notes              |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| ~~[Microsoft.PowerShell_profile.ps1](https://raw.githubusercontent.com/megabyte6/config/main/archive/powershell/Microsoft.PowerShell_profile.ps1)~~ | PowerShell configuration. Should be located at `C:\Users\<user name>\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` | **Not maintained** |

### ubuntu

| File                                                                                                              | Description                                                 | Notes              |
| ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------ |
| ~~[setup-headless.sh](https://raw.githubusercontent.com/megabyte6/config/main/archive/ubuntu/setup-headless.sh)~~ | Setup script for a fresh install of headless Ubuntu server. | **Not maintained** |
| ~~[setup.sh](https://raw.githubusercontent.com/megabyte6/config/main/archive/ubuntu/setup.sh)~~                   | Setup script for a fresh install of Ubuntu                  | **Not maintained** |
