param(
    [string]$Python = "python",
    [string]$HandoffFile,
    [string]$HandoffText,
    [switch]$Stdin,
    [switch]$FromClipboard,
    [switch]$PrintOnly,
    [string]$Output,
    [string[]]$BridgeArgs = @()
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "build_operator_packet_from_handoff.py"

$inputSources = 0
if ($HandoffFile) { $inputSources += 1 }
if ($HandoffText) { $inputSources += 1 }
if ($Stdin) { $inputSources += 1 }
if ($FromClipboard) { $inputSources += 1 }

if ($inputSources -gt 1) {
    Write-Error "Choose only one input source: -HandoffFile, -HandoffText, -Stdin, or -FromClipboard."
    exit 1
}

$arguments = @($pythonScript)

if ($HandoffFile) {
    $arguments += @("--handoff-file", $HandoffFile)
} elseif ($HandoffText) {
    $arguments += @("--handoff-text", $HandoffText)
} elseif ($Stdin) {
    $arguments += "--stdin"
} else {
    $arguments += "--from-clipboard"
}

if ($Output) {
    $arguments += @("--output", $Output)
}

if ($BridgeArgs -and $BridgeArgs.Count -gt 0) {
    $arguments += $BridgeArgs
}

$packetJson = & $Python @arguments --format json
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    exit $exitCode
}

$packetText = ($packetJson | Out-String).Trim()
if (-not $packetText) {
    Write-Error "Operator packet generation returned no output."
    exit 1
}

$packet = $packetText | ConvertFrom-Json
$promptText = [string]$packet.prompt
$summaryLines = @(
    "Operator packet ready.",
    "Downstream skill: $($packet.skill)",
    "Mode: $($packet.mode)",
    "Completion proof: $(([string[]]$packet.completion_markers) -join ', ')"
)

if ($packet.missing_inputs -and $packet.missing_inputs.Count -gt 0) {
    $summaryLines += "Still needed: $(([string[]]$packet.missing_inputs) -join ', ')"
}

$summaryLines += "Next action: $($packet.next_action)"

$summaryText = ($summaryLines -join [Environment]::NewLine)
Write-Output $summaryText
Write-Output ""
if ($PrintOnly) {
    Write-Output "Execution prompt preview:"
} else {
    Write-Output "Execution prompt copied to clipboard:"
}
Write-Output $promptText

if (-not $PrintOnly -and $promptText) {
    Set-Clipboard -Value $promptText
}

if ($Output) {
    $packetPath = [System.IO.Path]::ChangeExtension($Output, ".json")
    $packetText | Set-Content -LiteralPath $packetPath -Encoding utf8
}

exit 0
