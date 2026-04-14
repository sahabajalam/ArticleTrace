<#
.SYNOPSIS
    Tear down all Aegis Compliance Engine GCP resources to start from scratch.
    Deletes Cloud Run services, Artifact Registry images, and Secret Manager secrets.
    Does NOT delete the GCP project itself (uncomment the last section if you want that).

.USAGE
    .\cleanup_gcp.ps1
    .\cleanup_gcp.ps1 -ProjectId "aegis-compliance-engine" -Region "europe-west1"
    .\cleanup_gcp.ps1 -IncludeProject   # also deletes the GCP project
#>

param(
    [string]$ProjectId = "aegis-compliance-engine",
    [string]$Region    = "europe-west1",
    [string]$RepoName  = "aegis-images",
    [switch]$IncludeProject
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

function Invoke-GcloudSafe {
    param([string]$Label, [scriptblock]$Command)
    $prev = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        & $Command 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-OK $Label
        } else {
            Write-Warn "$Label -- skipped (not found or already deleted)"
        }
    } finally {
        $ErrorActionPreference = $prev
    }
}

$GCLOUD = (Get-Command gcloud.cmd -ErrorAction Stop).Source
$env:CLOUDSDK_CORE_DISABLE_PROMPTS = "1"

Invoke-GcloudSafe "set project" { & $GCLOUD config set project $ProjectId --quiet }

# ============================================================
# Confirmation
# ============================================================
Write-Header "AEGIS CLEANUP -- $ProjectId"
Write-Host ""
Write-Host "  This will DELETE the following from project '$ProjectId':" -ForegroundColor Red
Write-Host "    - All Cloud Run services (aegis-knowledge-engine, aegis-orchestrator, aegis-frontend)" -ForegroundColor White
Write-Host "    - All images in Artifact Registry repo '$RepoName'" -ForegroundColor White
Write-Host "    - All secrets (GEMINI_API_KEY, GOOGLE_API_KEY, DATABASE_URL_*, NEO4J_*)" -ForegroundColor White
if ($IncludeProject) {
    Write-Host "    - THE ENTIRE GCP PROJECT '$ProjectId'" -ForegroundColor Red
}
Write-Host ""
$confirm = Read-Host "  Type 'yes' to proceed"
if ($confirm -ne "yes") {
    Write-Host "`n  Aborted." -ForegroundColor Yellow
    exit 0
}

# ============================================================
# 1. Delete Cloud Run services
# ============================================================
Write-Header "DELETING CLOUD RUN SERVICES"

$services = @("aegis-knowledge-engine", "aegis-orchestrator", "aegis-frontend")
foreach ($svc in $services) {
    Write-Step "Deleting service: $svc"
    Invoke-GcloudSafe "deleted $svc" {
        & $GCLOUD run services delete $svc --region=$Region --quiet
    }
}

# ============================================================
# 2. Delete Artifact Registry images
# ============================================================
Write-Header "CLEANING ARTIFACT REGISTRY"

$repoExists = Invoke-GcloudQuery {
    & $GCLOUD artifacts repositories list --location=$Region --filter="name~/$RepoName`$" --format="value(name)"
}
if ($repoExists) {
    Write-Step "Deleting entire repo '$RepoName' (all images)..."
    Invoke-GcloudSafe "deleted repo $RepoName" {
        & $GCLOUD artifacts repositories delete $RepoName --location=$Region --quiet
    }
} else {
    Write-OK "Repo '$RepoName' does not exist -- nothing to delete"
}

# ============================================================
# 3. Delete secrets
# ============================================================
Write-Header "DELETING SECRETS"

$secrets = @(
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "DATABASE_URL_ORCHESTRATOR",
    "DATABASE_URL_MONITOR",
    "DATABASE_URL_SENTINEL",
    "NEO4J_URI",
    "NEO4J_USER",
    "NEO4J_PASSWORD"
)
foreach ($s in $secrets) {
    Write-Step "Deleting secret: $s"
    Invoke-GcloudSafe "deleted $s" {
        & $GCLOUD secrets delete $s --quiet
    }
}

# ============================================================
# 4. Prune local Docker images
# ============================================================
Write-Header "PRUNING LOCAL DOCKER ARTIFACTS"

$registry = "$Region-docker.pkg.dev/$ProjectId/$RepoName"
Write-Step "Removing local images matching: $registry/*"

$prev = $ErrorActionPreference
try {
    $ErrorActionPreference = "Continue"
    $localImages = docker images --format "{{.Repository}}:{{.Tag}}" 2>$null |
        Where-Object { $_ -like "$registry/*" }
} finally {
    $ErrorActionPreference = $prev
}

if ($localImages) {
    foreach ($img in $localImages) {
        Write-Step "Removing: $img"
        docker rmi $img 2>$null | Out-Null
    }
    Write-OK "Local images removed"
} else {
    Write-OK "No local images to remove"
}

Write-Step "Pruning Docker build cache"
$prev = $ErrorActionPreference
try {
    $ErrorActionPreference = "Continue"
    docker builder prune -af 2>$null | Out-Null
} finally {
    $ErrorActionPreference = $prev
}
Write-OK "Build cache pruned"

# ============================================================
# 5. (Optional) Delete the entire GCP project
# ============================================================
if ($IncludeProject) {
    Write-Header "DELETING GCP PROJECT"
    Write-Host "  WARNING: This deletes EVERYTHING in project '$ProjectId'!" -ForegroundColor Red
    $confirm2 = Read-Host "  Type the project ID to confirm"
    if ($confirm2 -eq $ProjectId) {
        Invoke-GcloudSafe "deleted project $ProjectId" {
            & $GCLOUD projects delete $ProjectId --quiet
        }
    } else {
        Write-Warn "Project ID did not match -- skipping project deletion"
    }
}

# ============================================================
# Summary
# ============================================================
Write-Header "CLEANUP COMPLETE"

Write-Host @"

  All Aegis resources have been removed from '$ProjectId'.

  To redeploy from scratch:
    1. .\deploy_gcp.ps1        # setup project, APIs, registry, secrets
    2. .\deploy.clean.ps1      # build + deploy all services

"@ -ForegroundColor Cyan
