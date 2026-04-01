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

$repoRoot = Split-Path -Parent $PSScriptRoot
$innerScript = Join-Path $repoRoot "skills\shared\learning-card-core\scripts\use_operator_packet.ps1"

if (-not (Test-Path -LiteralPath $innerScript)) {
    Write-Error "Shared operator packet script not found: $innerScript"
    exit 1
}

$invokeArgs = @{
    Python = $Python
}

if ($HandoffFile) {
    $invokeArgs.HandoffFile = $HandoffFile
}

if ($HandoffText) {
    $invokeArgs.HandoffText = $HandoffText
}

if ($Stdin) {
    $invokeArgs.Stdin = $true
}

if ($FromClipboard) {
    $invokeArgs.FromClipboard = $true
}

if ($PrintOnly) {
    $invokeArgs.PrintOnly = $true
}

if ($Output) {
    $invokeArgs.Output = $Output
}

if ($BridgeArgs -and $BridgeArgs.Count -gt 0) {
    $invokeArgs.BridgeArgs = $BridgeArgs
}

& $innerScript @invokeArgs
exit $LASTEXITCODE
