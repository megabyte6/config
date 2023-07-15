<#
.SYNOPSIS
A setup script used to set up a Linux OS after installing.

.DESCRIPTION
This is a setup script written in PowerShell to be used for installing or updating a Linux OS.

.PARAMETER Action
"Install"           Just install the packages.
"Update"            Just update the packages installed on the system.
"Help"              Get some help.

.PARAMETER OS
"Ubuntu"
"Kubuntu"
"Fedora"
"RPi"

.PARAMETER NoInstall
Show what's being installed but don't install anything.
#>

Param(
    [ValidateSet("Install", "Upgrade", "Help")][string]$Action = "Help",
    [ValidateSet("Ubuntu", "Kubuntu", "Fedora", "RPi")][string]$OS,
    [switch]$NoInstall
)

$Action = $Action.ToLower()

# Always add upgrade command first
$Commands = @{
    Ubuntu = @(
        "sudo apt update && sudo apt upgrade -y",
        "sudo apt install -y htop neofetch neovim httpie git flatpak gnome-software-plugin-flatpak",
        "flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo",
        "flatpak install flathub -y com.github.tchx84.Flatseal",
        "flatpak install flathub -y com.google.Chrome",
        "flatpak install flathub -y com.visualstudio.code",
        "flatpak install flathub -y com.discordapp.Discord",
        "flatpak install flathub -y org.polymc.PolyMC",
        "flatpak install flathub -y org.gimp.GIMP",
        "flatpak install flathub -y org.kde.kdenlive"
    )
    Kubuntu = @(
        "sudo apt update && sudo apt upgrade -y",
        "sudo apt install -y htop neofetch neovim httpie git flatpak plasma-discover-flatpak-backend",
        "flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo",
        "flatpak install flathub -y com.github.tchx84.Flatseal",
        "flatpak install flathub -y com.google.Chrome",
        "flatpak install flathub -y com.visualstudio.code",
        "flatpak install flathub -y com.discordapp.Discord",
        "flatpak install flathub -y org.polymc.PolyMC",
        "flatpak install flathub -y org.gimp.GIMP",
        "flatpak install flathub -y org.kde.kdenlive"
    )
    Fedora = @(
        "sudo dnf upgrade -y",
        "sudo dnf install -y htop neofetch neovim httpie git",
        "flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo",
        "flatpak install flathub -y com.github.tchx84.Flatseal",
        "flatpak install flathub -y com.google.Chrome",
        "flatpak install flathub -y com.visualstudio.code",
        "flatpak install flathub -y com.discordapp.Discord",
        "flatpak install flathub -y org.polymc.PolyMC",
        "flatpak install flathub -y org.gimp.GIMP",
        "flatpak install flathub -y org.kde.kdenlive"
    )
    RPi = @(
        "sudo apt update && sudo apt upgrade -y",
        "sudo apt install -y htop neofetch neovim httpie flatpak git",
        "flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo",
        "flatpak install flathub -y com.github.tchx84.Flatseal",
        "flatpak install flathub -y com.google.Chrome",
        "flatpak install flathub -y com.visualstudio.code",
        "flatpak install flathub -y com.discordapp.Discord",
        "flatpak install flathub -y org.polymc.PolyMC",
        "flatpak install flathub -y org.gimp.GIMP",
        "flatpak install flathub -y org.kde.kdenlive"
    )
}

function Get-Help {
    Write-Output 'Use "Get-Help ./setup.ps1" to see help info.'
}

function Invoke-Text {
    Param(
        [Parameter(Mandatory=$true)][string]$Command
    )
    if ($NoInstall) {
        Write-Output $Command
    } else {
        Invoke-Expression $Command
    }
}

function Install-Ubuntu {
    if ($Action -eq "upgrade") {
        Invoke-Text $Commands.Ubuntu[0]
        Exit
    }
    foreach ($CurrentCommand in $Commands.Ubuntu) {
        Invoke-Text $CurrentCommand
    }
}

function Install-Kubuntu {
    if ($Action -eq "upgrade") {
        Invoke-Text $Commands.Kubuntu[0]
        Exit
    }
    foreach ($CurrentCommand in $Commands.Kubuntu) {
        Invoke-Text $CurrentCommand
    }
}

function Install-Fedora {
    if ($Action -eq "upgrade") {
        Invoke-Text $Commands.Fedora[0]
        Exit
    }
    foreach ($CurrentCommand in $Commands.Fedora) {
        Invoke-Text $CurrentCommand
    }
}

function Install-RPi {
    if ($Action -eq "upgrade") {
        Invoke-Text $Commands.RPi[0]
        Exit
    }
    foreach ($CurrentCommand in $Commands.RPi) {
        Invoke-Text $CurrentCommand
    }
}

# Start of script
if ($Action -eq "help") {
    Get-Help
    Exit
}

switch ($OS.ToLower()) {
    "ubuntu" {
        Install-Ubuntu
        Break
    }
    "kubuntu" {
        Install-Kubuntu
        Break
    }
    "fedora" {
        Install-Fedora
        Break
    }
    "rpi" {
        Install-RPi
        Break
    }
}
