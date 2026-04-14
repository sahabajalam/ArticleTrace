# Fast deployment wrapper -- reuses Docker cache (much faster on code-only changes)
# Usage:
#   .\deploy.fast.ps1

$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$mainScript = Join-Path $scriptDir "deploy.ps1"

& $mainScript -UseCache -SkipCachePrune
exit $LASTEXITCODE
