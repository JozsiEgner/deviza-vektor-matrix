param(
    [Parameter(Mandatory = $false)]
    [string]$InputFile = "..\examples\sample-input.json",

    [Parameter(Mandatory = $false)]
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = Join-Path $root "src"
$resolvedInput = Resolve-Path (Join-Path $PSScriptRoot $InputFile)

& $Python -m dvm.cli $resolvedInput
if ($LASTEXITCODE -ne 0) {
    throw "A Deviza-Vektor Matrix futtatasa sikertelen."
}
