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
$pythonScript = Join-Path $scriptDir "build_execution_prompt_from_handoff.py"

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

$outputLines = & $Python @arguments
$exitCode = $LASTEXITCODE

if ($outputLines) {
    $outputText = ($outputLines | Out-String).TrimEnd("`r", "`n")
    if ($outputText.Length -gt 0) {
        Write-Output $outputText
    }
} else {
    $outputText = ""
}

if ($exitCode -ne 0) {
    exit $exitCode
}

if (-not $PrintOnly) {
    if ($Output) {
        $clipboardText = Get-Content -Path $Output -Raw -Encoding utf8
    } else {
        $clipboardText = $outputText
    }
    if ($clipboardText) {
        Set-Clipboard -Value $clipboardText
    }
}

exit 0
