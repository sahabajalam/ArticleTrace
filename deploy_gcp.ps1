<#
.SYNOPSIS
    First-time GCP project setup for Aegis Compliance Engine.
    Creates the GCP project, enables APIs, sets up Artifact Registry,
    and pushes secrets. Does NOT build or deploy -- run deploy.ps1 after.

.USAGE
    .\deploy_gcp.ps1                          # setup only
    .\deploy_gcp.ps1 ; .\deploy.ps1           # setup then deploy
    .\deploy_gcp.ps1 ; .\deploy.fast.ps1      # setup then fast deploy

.PREREQUISITES
    - gcloud CLI installed & authenticated (gcloud auth login)
    - GCP billing enabled on the project
    - .env files in orchestrator/ and knowledge_engine/
#>

param(
    [string]$ProjectId = "aegis-compliance-engine",
    [string]$Region    = "europe-west1",
    [string]$RepoName  = "aegis-images"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# ============================================================
# Helpers
# ============================================================
function Write-Header([string]$msg) {
    Write-Host "`n$('=' * 60)" -ForegroundColor Cyan
    Write-Host "  $msg" -ForegroundColor Cyan
    Write-Host "$('=' * 60)" -ForegroundColor Cyan
}
function Write-Step([string]$msg)  { Write-Host "`n[+] $msg" -ForegroundColor Yellow }
function Write-OK([string]$msg)    { Write-Host "    [OK] $msg" -ForegroundColor Green }
function Write-Warn([string]$msg)  { Write-Host "    [!!] $msg" -ForegroundColor DarkYellow }
function Write-Fail([string]$msg)  { Write-Host "    [ERR] $msg" -ForegroundColor Red }

function Invoke-Native {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][scriptblock]$Command
    )
    $prev = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        & $Command
        $exitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }
    if ($exitCode -ne 0) {
        throw "$Label failed with exit code $exitCode"
    }
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

$Root     = $PSScriptRoot
if (-not $Root) { $Root = (Get-Location).Path }
$Registry = "$Region-docker.pkg.dev/$ProjectId/$RepoName"
$GCLOUD   = (Get-Command gcloud.cmd -ErrorAction Stop).Source

$env:CLOUDSDK_CORE_DISABLE_PROMPTS = "1"

# ============================================================
# 0. Prerequisites
# ============================================================
Write-Header "PREREQUISITE CHECK"

$Account = Invoke-GcloudQuery { & $GCLOUD auth list --filter="status:ACTIVE" --format="value(account)" }
if (-not $Account) {
    Write-Fail "No active gcloud account. Run: gcloud auth login"
    exit 1
}
Write-OK "gcloud authenticated as: $Account"

# ============================================================
# 1. GCP Project setup
# ============================================================
Write-Header "GCP PROJECT SETUP"

Write-Step "Setting active project to: $ProjectId"
$existing = Invoke-GcloudQuery { & $GCLOUD projects list --filter="projectId=$ProjectId" --format="value(projectId)" }

if ($existing -eq $ProjectId) {
    Write-OK "Project '$ProjectId' already exists -- skipping creation."
} else {
    Write-Step "Creating GCP project '$ProjectId'..."
    Invoke-Native "project create" { & $GCLOUD projects create $ProjectId --name="Aegis Compliance Engine" }
    Write-OK "Project created."
}

Invoke-Native "set project" { & $GCLOUD config set project $ProjectId --quiet }
Write-OK "Active project: $ProjectId"

# ============================================================
# 2. Enable APIs  (billing must be enabled first)
# ============================================================
Write-Header "ENABLING APIS"

$apis = @("run.googleapis.com","artifactregistry.googleapis.com","secretmanager.googleapis.com")
foreach ($api in $apis) {
    Write-Step "Enabling $api ..."
    Invoke-Native "enable $api" { & $GCLOUD services enable $api --quiet }
    Write-OK "$api enabled"
}

# ============================================================
# 3. Artifact Registry
# ============================================================
Write-Header "ARTIFACT REGISTRY"

Write-Step "Checking repo '$RepoName' in $Region..."
$repoExists = Invoke-GcloudQuery { & $GCLOUD artifacts repositories list --location=$Region --filter="name~/$RepoName`$" --format="value(name)" }
if ($repoExists) {
    Write-OK "Repo already exists."
} else {
    Write-Step "Creating Artifact Registry repo..."
    Invoke-Native "create artifact repo" {
        & $GCLOUD artifacts repositories create $RepoName `
            --repository-format=docker `
            --location=$Region `
            --description="Aegis Compliance Engine images" `
            --quiet
    }
    Write-OK "Repo created: $Registry"
}

# ============================================================
# 4. Secrets (delegates to setup-secrets.ps1)
# ============================================================
Write-Header "SECRET MANAGER"

$secretsScript = Join-Path $Root "setup-secrets.ps1"
if (Test-Path $secretsScript) {
    Write-Step "Running setup-secrets.ps1 ..."
    & $secretsScript
    Write-OK "Secrets pushed"
} else {
    Write-Fail "setup-secrets.ps1 not found at $secretsScript"
    exit 1
}

# ============================================================
# Done
# ============================================================
Write-Header "GCP SETUP COMPLETE"

Write-Host @"

  Project  : $ProjectId
  Region   : $Region
  Registry : $Registry

  Next steps:
    .\deploy.clean.ps1    # full clean build + deploy
    .\deploy.fast.ps1     # fast cached build + deploy

"@ -ForegroundColor Cyan
