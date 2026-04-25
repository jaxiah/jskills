param([string]$jskills = $PSScriptRoot)

$targets = @(
    Join-Path $env:USERPROFILE '.claude\skills'
    Join-Path $env:USERPROFILE '.gemini\skills'
)

$dirs = Get-ChildItem $jskills -Directory | Where-Object { $_.Name -notlike '.*' }

foreach ($target in $targets) {
    New-Item -ItemType Directory -Force -Path $target | Out-Null
    Write-Host "`n-> $target"
    foreach ($dir in $dirs) {
        $link = Join-Path $target $dir.Name
        if (Test-Path $link) {
            Write-Host "SKIP  $($dir.Name)  (already exists)"
        } else {
            New-Item -ItemType Junction -Path $link -Target $dir.FullName | Out-Null
            Write-Host "LINK  $($dir.Name)"
        }
    }
}
