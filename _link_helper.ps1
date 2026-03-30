param([string]$jskills = $PSScriptRoot)

$target = Join-Path $env:USERPROFILE '.claude\skills'

Get-ChildItem $jskills -Directory | Where-Object { $_.Name -notlike '.*' } | ForEach-Object {
    $link = Join-Path $target $_.Name
    if (Test-Path $link) {
        Write-Host "SKIP  $($_.Name)  (already exists)"
    } else {
        New-Item -ItemType Junction -Path $link -Target $_.FullName | Out-Null
        Write-Host "LINK  $($_.Name)"
    }
}
