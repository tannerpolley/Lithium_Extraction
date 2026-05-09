<#
.SYNOPSIS
Sync the Lithium_Extraction docs\latex manuscript into the LaTeX-Projects mirror folder.

.DESCRIPTION
The source manuscript lives in Lithium_Extraction\docs\latex. The mirror folder
under LaTeX-Projects keeps the LaTeX project in the same family as the user's
other Overleaf-oriented manuscript folders. Use -WhatIf to preview the sync.
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$MirrorRoot = 'C:\Users\Tanner\Documents\git\LaTeX-Projects\Lithium-Extraction-LaTeX',
    [switch]$CleanBuildFiles
)

$ErrorActionPreference = 'Stop'

function Resolve-OrCreatePath {
    param(
        [Parameter(Mandatory = $true)][string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Force -Path $Path | Out-Null
    }

    return (Resolve-Path -LiteralPath $Path).Path
}

function Invoke-RobocopyChecked {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    $scriptName = Split-Path -Leaf $PSCommandPath
    $args = @(
        $Source,
        $Destination,
        '/E',
        '/R:2',
        '/W:1',
        '/NFL',
        '/NDL',
        '/NJH',
        '/NJS',
        '/XD',
        '.git',
        'out',
        '__pycache__',
        '.pytest_cache',
        '/XF',
        $scriptName,
        '*.aux',
        '*.bbl',
        '*.blg',
        '*.fdb_latexmk',
        '*.fls',
        '*.log',
        '*.out',
        '*.synctex.gz',
        '*.xdv'
    )

    if ($WhatIfPreference) {
        $args += '/L'
    }

    & robocopy @args | Out-Host
    $exitCode = $LASTEXITCODE
    if ($exitCode -gt 7) {
        throw "robocopy failed with exit code $exitCode while syncing '$Source' to '$Destination'"
    }
}

$sourcePath = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$mirrorPath = Resolve-OrCreatePath -Path $MirrorRoot

if ($sourcePath -eq $mirrorPath) {
    throw 'Source and mirror paths are the same.'
}

Write-Host "Source LaTeX folder: $sourcePath"
Write-Host "Mirror root: $mirrorPath"

if ($PSCmdlet.ShouldProcess($mirrorPath, "Sync LaTeX manuscript from $sourcePath")) {
    Invoke-RobocopyChecked -Source $sourcePath -Destination $mirrorPath
}

if ($CleanBuildFiles) {
    $buildPatterns = @('*.aux', '*.bbl', '*.blg', '*.fdb_latexmk', '*.fls', '*.log', '*.out', '*.synctex.gz', '*.xdv')
    foreach ($pattern in $buildPatterns) {
        Get-ChildItem -LiteralPath $mirrorPath -Filter $pattern -File -Recurse -ErrorAction SilentlyContinue |
            ForEach-Object {
                if ($PSCmdlet.ShouldProcess($_.FullName, 'Remove LaTeX build artifact')) {
                    Remove-Item -LiteralPath $_.FullName -Force
                }
            }
    }
}

Write-Host 'LaTeX mirror sync complete.'
