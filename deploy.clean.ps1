# Clean deployment wrapper -- full rebuild with no Docker cache
# Usage:
#   .\deploy.clean.ps1

$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$mainScript = Join-Path $scriptDir "deploy.ps1"

& $mainScript
exit $LASTEXITCODE
