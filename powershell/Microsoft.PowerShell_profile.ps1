# Thanks to Tim Sneath <tim@sneath.org>
# From https://gist.github.com/timsneath/19867b12eee7fd5af2ba

# As a reminder, to enable unsigned script execution of local scripts on client Windows,
# you need to run this line from an elevated PowerShell prompt:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
# This is the default policy on Windows Server 2012 R2 and above for server Windows. For
# more information about execution policies, run Get-Help about_Execution_Policies.

# Find out if the current user identity is elevated (has admin rights)
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal $identity
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

# Delete them to prevent cluttering up the user profile. 
Remove-Variable identity
Remove-Variable principal

# Append [ADMIN] if appropriate for easy taskbar identification
if ($isAdmin) {
    $Host.UI.RawUI.WindowTitle += " [ADMIN]"
}

# Useful shortcuts for traversing directories
function cd... {
    Set-Location ..\..
}

function cd.... {
    Set-Location ..\..\..
}

# Compute file hashes - useful for checking successful downloads 
function md5 {
    param (
        [string]$File,
        [string]$CompareWith
    )

    $Hash = Get-FileHash -Algorithm MD5 $File
    if ($PSBoundParameters.ContainsKey('CompareWith')) {
        Write-Output ($Hash.Hash -eq $CompareWith)
    } else {
        Write-Output $Hash
    }
}

function sha1 {
    param (
        [string]$File,
        [string]$CompareWith
    )

    $Hash = Get-FileHash -Algorithm SHA1 $File
    if ($PSBoundParameters.ContainsKey('CompareWith')) {
        Write-Output ($Hash.Hash -eq $CompareWith)
    } else {
        Write-Output $Hash
    }
}

function sha256 {
    param (
        [string]$File,
        [string]$CompareWith
    )

    $Hash = Get-FileHash -Algorithm SHA256 $File
    if ($PSBoundParameters.ContainsKey('CompareWith')) {
        Write-Output ($Hash.Hash -eq $CompareWith)
    } else {
        Write-Output $Hash
    }
}

function sha512 {
    param (
        [string]$File,
        [string]$CompareWith
    )

    $Hash = Get-FileHash -Algorithm SHA512 $File
    if ($PSBoundParameters.ContainsKey('CompareWith')) {
        Write-Output ($Hash.Hash -eq $CompareWith)
    } else {
        Write-Output $Hash
    }
}

# Does the the rough equivalent of dir /s /b or the tree command from windows.
# For example, dirs *.png is dir /s /b *.png
function dirs {
    if ($args.Count -gt 0) {
        Get-ChildItem -Recurse -Include "$args" | Foreach-Object FullName
    } else {
        Get-ChildItem -Recurse | Foreach-Object FullName
    }
}

# Simple function to start a new elevated process. If arguments are supplied then 
# a single command is started with admin rights. If not then a new admin instance
# of PowerShell is started.
function admin {
    if ($args.Count -gt 0) {
        $argList = "& '" + $args + "'"
        Start-Process "$PSHOME\pwsh.exe" -Verb runAs -ArgumentList $argList
    } else {
        Start-Process "$PSHOME\pwsh.exe" -Verb runAs
    }
}
New-Alias -Name su -Value admin
New-Alias -Name sudo -Value admin

function find {
    param (
        [string]$Search
    )

    Get-ChildItem -Recurse -Filter "*${Search}*" -ErrorAction SilentlyContinue |
        ForEach-Object { Write-Output $_.FullName }
}

function unzip {
    param (
        [string]$File
    )

    Write-Output("Extracting", $File, "to", $PWD)
	$fullFile = Get-ChildItem -Path $PWD -Filter .\cove.zip | ForEach-Object{$_.FullName}
    Expand-Archive -Path $fullFile -DestinationPath $PWD
}

function grep {
    param (
        [string]$Regex,
        [string]$Dir
    )

    if ($Dir) {
        Get-ChildItem $Dir | Select-String $Regex
        return
    }
    $input | Select-String $Regex
}

function touch {
    param (
        [string]$Name
    )

    New-Item $Name
}

function which {
    param (
        [string]$Name
    )

    Get-Command $Name | Select-Object -ExpandProperty Definition
}

function wget {
    param (
        [string]$Url,
        [string]$OutFile
    )

    # Use the file name from the Url if one isn't given.
    if ($OutFile -eq "") {
        $parts = $Url.Split('/')
        $OutFile = $parts[-1]
    }

    Invoke-WebRequest -Uri $Url -OutFile $OutFile
}

function pkill {
    param (
        [string]$Name
    )

    Get-Process $Name -ErrorAction SilentlyContinue | Stop-Process
}

function pgrep {
    param (
        [string]$Name
    )

    Get-Process $Name
}
