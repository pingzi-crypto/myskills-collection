param(
    [Parameter(Mandatory = $true)]
    [string]$CheckFile
)

if (-not (Test-Path -LiteralPath $CheckFile)) {
    Write-Error "Preflight check file not found: $CheckFile"
    exit 1
}

$check = Get-Content -LiteralPath $CheckFile -Raw -Encoding utf8 | ConvertFrom-Json

$completionMarkers = ""
if ($check.expected_completion_markers) {
    $completionMarkers = ([string[]]$check.expected_completion_markers) -join ", "
}

$lines = @(
    "Bridge preflight gate ready.",
    "Gate: $($check.go_no_go.ToUpperInvariant())",
    "Skill: $($check.expected_skill)",
    "Mode: $($check.mode)",
    "Target: $($check.expected_target_path)",
    "Completion proof: $completionMarkers",
    "Prompt packet: $($check.prompt_output)",
    "Next action: $($check.manual_next_step)"
)

if ($check.placeholder_free -ne $null) {
    $lines += "Placeholder free: $($check.placeholder_free)"
}

if ($check.placeholder_markers -and $check.placeholder_markers.Count -gt 0) {
    $lines += "Blocking placeholders: $(([string[]]$check.placeholder_markers) -join ', ')"
}

$outputText = ($lines -join [Environment]::NewLine)
Write-Output $outputText

if ($check.go_no_go -ne "go") {
    exit 2
}

exit 0
