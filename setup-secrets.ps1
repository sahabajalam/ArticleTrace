# setup-secrets.ps1
# Reads .env files and pushes all secrets into GCP Secret Manager.
# Run this ONCE before the first deploy, or whenever secrets change.
#
# Usage:
#   .\setup-secrets.ps1

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$PROJECT_ID = "aegis-compliance-engine"
$GCLOUD     = (Get-Command gcloud.cmd -ErrorAction Stop).Source

$env:CLOUDSDK_CORE_DISABLE_PROMPTS = "1"

function Write-Step($msg) { Write-Host "`n[$((Get-Date).ToString('HH:mm:ss'))] $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "  OK: $msg" -ForegroundColor Green }
function Write-Skip($msg) { Write-Host "  SKIP: $msg" -ForegroundColor DarkGray }

function Invoke-Native {
    param([string]$Label, [scriptblock]$Command)
    $prev = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        & $Command
        $exitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }
    if ($exitCode -ne 0) { throw "$Label failed with exit code $exitCode" }
}

function Read-Env([string]$file, [string]$key) {
    if (-not (Test-Path $file)) { return "" }
    $line = Select-String -Path $file -Pattern "^$key=" | Select-Object -First 1
    if (-not $line) { return "" }
    return ($line.Line -split "=", 2)[1].Trim()
}

function Invoke-GcloudQuery {
    param([Parameter(Mandatory)][scriptblock]$Command)
    $prev = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        $result = & $Command 2>$null
    } finally {
        $ErrorActionPreference = $prev
    }
    return $result
}

function Push-Secret([string]$name, [string]$value) {
    if (-not $value -or $value.Length -lt 5) {
        Write-Skip "$name (empty or too short)"
        return
    }
    # Write to a temp file using WriteAllBytes — no BOM, no trailing CRLF.
    # PowerShell 5.1 piping adds \r\n, and WriteAllText adds a UTF-8 BOM,
    # both of which corrupt secret values when Cloud Run injects them as env vars.
    $tmp = [System.IO.Path]::GetTempFileName()
    try {
        [System.IO.File]::WriteAllBytes($tmp, [System.Text.Encoding]::UTF8.GetBytes($value))
        $exists = Invoke-GcloudQuery { & $GCLOUD secrets describe $name --format="value(name)" }
        if ($exists) {
            Write-Step "Updating: $name"
            Invoke-Native "secret version add $name" {
                & $GCLOUD secrets versions add $name --data-file=$tmp --quiet 2>$null
            }
        } else {
            Write-Step "Creating: $name"
            Invoke-Native "secret create $name" {
                & $GCLOUD secrets create $name --data-file=$tmp --replication-policy=automatic --quiet 2>$null
            }
        }
        Write-Ok "$name stored"
    } finally {
        Remove-Item $tmp -Force -ErrorAction SilentlyContinue
    }
}

Write-Step "Setting project to $PROJECT_ID"
Invoke-Native "set project" { & $GCLOUD config set project $PROJECT_ID --quiet }

Write-Step "Enabling Secret Manager API"
Invoke-Native "enable secretmanager" { & $GCLOUD services enable secretmanager.googleapis.com --quiet }

$root    = $PSScriptRoot
$orchEnv = Join-Path $root "orchestrator\.env"
$keEnv   = Join-Path $root "knowledge_engine\.env"

Write-Step "Pushing secrets from .env files..."

Push-Secret "GEMINI_API_KEY"            (Read-Env $orchEnv "GEMINI_API_KEY")
Push-Secret "GOOGLE_API_KEY"            (Read-Env $keEnv   "GOOGLE_API_KEY")
Push-Secret "DATABASE_URL_ORCHESTRATOR" (Read-Env $orchEnv "DATABASE_URL")
Push-Secret "NEO4J_URI"                 (Read-Env $keEnv   "NEO4J_URI")
Push-Secret "NEO4J_USER"                (Read-Env $keEnv   "NEO4J_USER")
Push-Secret "NEO4J_PASSWORD"            (Read-Env $keEnv   "NEO4J_PASSWORD")

# Grant default compute SA access to secrets (needed by Cloud Run)
Write-Step "Granting Secret Manager access to Cloud Run service account"
$projectNum = (& $GCLOUD projects describe $PROJECT_ID --format="value(projectNumber)" 2>$null).Trim()
$sa = "$projectNum-compute@developer.gserviceaccount.com"
Invoke-Native "iam binding" {
    & $GCLOUD projects add-iam-policy-binding $PROJECT_ID `
        --member="serviceAccount:$sa" `
        --role="roles/secretmanager.secretAccessor" `
        --quiet 2>$null | Out-Null
}
Write-Ok "IAM: $sa -> secretAccessor"

Write-Host ""
Write-Host "All secrets pushed. You can now run .\deploy.ps1" -ForegroundColor Yellow
Write-Host ""
