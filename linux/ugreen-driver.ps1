Param (
    [ValidateSet("Debian", "RHEL")][string]$OS
)

function Install-Debian {
    $Commands = @(
        "sudo apt update",
        "sudo apt install -y git dkms"
        "git clone https://github.com/aircrack-ng/rtl8812au.git"
        "cd ./rtl8812au/"
        "sudo make dkms_install"
    )
    foreach ($SelectedCommand in $Commands) {
        Invoke-Expression $SelectedCommand
    }
}

function Install-RHEL {
    $Commands = @(
        "sudo dnf upgrade",
        "sudo dnf install -y git dkms kernel-devel"
        "git clone https://github.com/aircrack-ng/rtl8812au.git"
        "cd ./rtl8812au/"
        "sudo make dkms_install"
    )
    foreach ($SelectedCommand in $Commands) {
        Invoke-Expression $SelectedCommand
    }
}

switch ($OS.ToLower()) {
    "debian" { Install-Debian }
    "rhel" { Install-RHEL }
}
