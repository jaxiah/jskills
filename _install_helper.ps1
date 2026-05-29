param([string]$jskills = $PSScriptRoot)

$targetsFile = Join-Path $jskills 'install-targets.local.txt'
if (-not (Test-Path $targetsFile)) {
    Write-Error "Missing local target config: $targetsFile"
    Write-Error "Create it with one agent skills directory per line, for example: %USERPROFILE%\.codex\skills"
    exit 1
}

$targets = Get-Content $targetsFile |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -and -not $_.StartsWith('#') } |
    ForEach-Object { [Environment]::ExpandEnvironmentVariables($_) }

if (-not $targets) {
    Write-Error "No install targets found in $targetsFile"
    exit 1
}

$dirs = Get-ChildItem $jskills -Directory | Where-Object { $_.Name -notlike '.*' }

foreach ($target in $targets) {
    New-Item -ItemType Directory -Force -Path $target | Out-Null
    Write-Host "`n-> $target"
    foreach ($dir in $dirs) {
        $dest = Join-Path $target $dir.Name
        if (Test-Path $dest) {
            Write-Host "SKIP  $($dir.Name)  (already exists)"
        } else {
            Copy-Item -LiteralPath $dir.FullName -Destination $dest -Recurse
            Write-Host "COPY  $($dir.Name)"
        }
    }
}

exit 0
