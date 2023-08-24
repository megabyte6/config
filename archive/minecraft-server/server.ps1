#!/usr/bin/env pwsh

param(
    [ValidateSet("new","backup","help")][string]$Command,
    [string]$ServerName
)

function Write-CustomScripts {
    param(
        [string]$ServerName
    )

@'
#!/usr/bin/env pwsh

param(
    [string]$MCVersion = -1,
    [int]$BuildVersion = -1,
    [ValidateSet("all","MCVersion","Build")][string]$CheckLatest
)

# Find latest Minecraft version if it isn't specified.
if ($MCVersion -eq -1) {
    $MCVersionsURL = "https://api.papermc.io/v2/projects/paper"
    $MCVersion = (Invoke-WebRequest $MCVersionsURL | ConvertFrom-Json).
            versions[-1]
}

# Find latest PaperMC build version if it isn't specified.
if ($BuildVersion -eq -1) {
    $BuildVersionsURL = "https://api.papermc.io/v2/projects/paper/versions/$MCVersion/builds"
    $BuildVersion = (Invoke-WebRequest $BuildVersionsURL | ConvertFrom-Json).
            builds[-1].
            build
}

# Check if the user wants to know both the latest Minecraft version or the
# latest PaperMC build.
if ($CheckLatest) {
    Write-Output $(switch ($CheckLatest) {
        'MCVersion' { $MCVersion }
        'Build'     { $BuildVersion }
        default     { "Latest build for Minecraft $MCVersion is version $BuildVersion" }
    })
    exit
}

# Find JAR name for download link.
$JarURL = "https://api.papermc.io/v2/projects/paper/versions/$MCVersion/builds/$BuildVersion"
$JarName = (Invoke-WebRequest $JarURL | ConvertFrom-Json).
        downloads.
        application.
        name

$DownloadURL = "https://api.papermc.io/v2/projects/paper/versions/$MCVersion/builds/$BuildVersion/downloads/$JarName"

# Check if the latest build is already downloaded.
if (Test-Path $JarName -PathType Leaf) {
    Write-Output "You are already on the latest build for Minecraft $MCVersion"
    exit
}

# Delete old JAR.
Remove-Item "paper*.jar"

# Download the latest build of PaperMC.
Invoke-WebRequest $DownloadURL -OutFile $JarName
'@ | Out-File -FilePath $(Join-Path "." $ServerName "update.ps1")

@"
#!/usr/bin/env pwsh

# Check if there is an update and if so, update the server JAR.
./update.ps1 -MCVersion $(pwsh $(Join-Path "." $ServerName "update.ps1") -CheckLatest MCVersion)

# Start PaperMC.
java -Xms512M -Xmx4G -jar paper*.jar nogui
"@ | Out-File -FilePath $(Join-Path "." $ServerName "start.ps1")
}

function Show-Help {
    Write-Output @'
-----------------------------------------------------------
Help
-----------------------------------------------------------
Possible sub-commands:
    "new <server name>"
        Create a new server with the specified server name.
    "backup <server name>"
        Backup the server specified.
    "help"
        Show this menu.
'@
}

# Make input lowercase.
if ($Command -ne "") {
    $Command = $Command.ToLower()
}

switch ($Command) {

    "new" {
        # Make sure the correct number of arguments were passed.
        if ($ServerName -eq "") {
            Write-Output "Please specify a new server name."
            exit
        }

        # Check if the server given exists.
        if (Test-Path -Path $ServerName) {
            Write-Output "That server already exists."
            Write-Output "Please choose a new name and try again."
            exit
        }

        # Create the server directory and add the custom scripts.
        New-Item -Path "." -Name $ServerName -ItemType "directory" > $null
        Write-CustomScripts -ServerName $ServerName
    }

    "backup" {
        # Make sure the correct number of arguments were passed.
        if ($ServerName -eq "") {
            Write-Output "Please specify a server to backup."
            exit
        }

        # Check if the server given exists.
        if (!(Test-Path -Path $ServerName)) {
            Write-Output "That server does not seem to exist."
            Write-Output "Please check the spelling and try again."
            exit
        }

        $currentDate = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

        $backupLocation = Join-Path $ServerName "backup" "$currentDate.7z"

        # Navigate to the server directory.
        Set-Location $(Join-Path "." $ServerName)

        # Create the archive file.
        7z a $(Join-Path ".." $backupLocation) ./world ./world_nether ./world_the_end

        # Change location back to root.
        Set-Location ../
    }

    default {
        Show-Help
    }

}

