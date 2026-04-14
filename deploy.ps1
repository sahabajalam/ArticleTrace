# Aegis Compliance Engine -- Cloud Run deploy script
# Mirrors the pattern from project_7_Job_tracker/deploy.ps1
#
# Usage:
#   .\deploy.ps1
#   .\deploy.ps1 -UseCache
#   .\deploy.ps1 -SkipCachePrune

param(
    [switch]$UseCache,
    [switch]$SkipCachePrune
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# ---- Configuration ----
$REGION          = "europe-west1"
$ARTIFACT_REPO   = "aegis-images"
$PROJECT_ID      = "aegis-compliance-engine"

$SERVICE_KNOWLEDGE = "aegis-knowledge-engine"
$SERVICE_ORCH      = "aegis-orchestrator"
$SERVICE_FRONTEND  = "aegis-frontend"

# ---- Helpers ----
function Write-Step($msg) { Write-Host "`n[$((Get-Date).ToString('HH:mm:ss'))] $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "  OK: $msg" -ForegroundColor Green }
function Write-Err($msg)  { Write-Host "  ERROR: $msg" -ForegroundColor Red }

# Invoke-Native: runs a native command and throws on non-zero exit.
# Temporarily relaxes ErrorActionPreference so gcloud's PS wrapper stderr doesn't
# trigger a terminating error -- we rely on $LASTEXITCODE instead.
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

# Invoke-GcloudQuery: runs a gcloud read-only command and returns its stdout.
# Suppresses stderr (gcloud writes info messages there) without triggering
# PowerShell's NativeCommandError under $ErrorActionPreference = "Stop".
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

# ---- Pre-flight ----
Write-Step "Pre-flight checks"

if (-not (Get-Command gcloud.cmd -ErrorAction SilentlyContinue)) {
    Write-Err "gcloud CLI not found. Install: https://cloud.google.com/sdk/docs/install"
    exit 1
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Err "Docker not found. Install Docker Desktop."
    exit 1
}

$GCLOUD = (Get-Command gcloud.cmd -ErrorAction Stop).Source

# Verify project is set
Invoke-Native "gcloud config set project" { & $GCLOUD config set project $PROJECT_ID --quiet }
Write-Ok "Project: $PROJECT_ID"
Write-Ok "Region:  $REGION"
if ($UseCache)       { Write-Ok "Build mode: FAST (Docker cache enabled)" }
else                 { Write-Ok "Build mode: CLEAN (no cache)" }

$env:CLOUDSDK_CORE_DISABLE_PROMPTS = "1"

# ---- Verify required secrets exist ----
Write-Step "Verifying required secrets in Secret Manager"

$requiredSecrets = @(
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "DATABASE_URL_ORCHESTRATOR",
    "NEO4J_URI",
    "NEO4J_USER",
    "NEO4J_PASSWORD"
)

$existingSecrets = @()
Invoke-Native "gcloud secrets list" {
    $script:existingSecrets = (& $GCLOUD secrets list --format="value(name)" 2>$null) -split "`n" |
        ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
}

$missing = @()
foreach ($s in $requiredSecrets) {
    if ($existingSecrets -contains $s) {
        Write-Ok $s
    } else {
        Write-Err "$s -- MISSING"
        $missing += $s
    }
}
if ($missing.Count -gt 0) {
    Write-Host "`nRun .\setup-secrets.ps1 to push your .env values into Secret Manager." -ForegroundColor Yellow
    exit 1
}

# ---- Image tags ----
$buildTag = "manual-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$reg      = "$REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO"

$imgKnowledgeTag  = "$reg/knowledge-engine:$buildTag"; $imgKnowledgeLatest  = "$reg/knowledge-engine:latest"
$imgOrchTag       = "$reg/orchestrator:$buildTag"; $imgOrchLatest       = "$reg/orchestrator:latest"
$imgFrontendTag   = "$reg/frontend:$buildTag";    $imgFrontendLatest   = "$reg/frontend:latest"

# ---- Docker auth ----
Write-Step "Configuring Artifact Registry auth"
Invoke-Native "docker auth configure" { & $GCLOUD auth configure-docker "$REGION-docker.pkg.dev" --quiet }

# ---- Cache prune ----
$shouldPrune = (-not $UseCache) -and (-not $SkipCachePrune)
if ($shouldPrune) {
    Write-Step "Pruning Docker build cache"
    Invoke-Native "docker builder prune" { docker builder prune -af }
} else {
    Write-Step "Skipping cache prune"
}

# ---- Build helper ----
function Invoke-DockerBuild($label, $contextPath, $tag, $latestTag, $buildArgsList = @()) {
    $dockerArgs = @("build", "--platform", "linux/amd64")
    if (-not $UseCache) { $dockerArgs += "--no-cache" }
    foreach ($ba in $buildArgsList) { $dockerArgs += @("--build-arg", $ba) }
    $dockerArgs += @("-t", $tag, "-t", $latestTag, $contextPath)
    Invoke-Native "docker build $label" { docker @dockerArgs }
}

# ---- Build backend images (knowledge-engine, orchestrator) ----
$root = $PSScriptRoot

Write-Step "Building Knowledge Engine image"
Invoke-DockerBuild "knowledge-engine" "$root\knowledge_engine" $imgKnowledgeTag $imgKnowledgeLatest

Write-Step "Building Orchestrator image"
Invoke-DockerBuild "orchestrator" "$root\orchestrator" $imgOrchTag $imgOrchLatest

# ---- Push backend images ----
Write-Step "Pushing Knowledge Engine"
Invoke-Native "push knowledge tag"    { docker push $imgKnowledgeTag }
Invoke-Native "push knowledge latest" { docker push $imgKnowledgeLatest }

Write-Step "Pushing Orchestrator"
Invoke-Native "push orchestrator tag"    { docker push $imgOrchTag }
Invoke-Native "push orchestrator latest" { docker push $imgOrchLatest }

# ---- Deploy Knowledge Engine ----
Write-Step "Deploying Knowledge Engine to Cloud Run"
Invoke-Native "deploy knowledge-engine" {
    & $GCLOUD run deploy $SERVICE_KNOWLEDGE `
        --image=$imgKnowledgeTag `
        --region=$REGION `
        --platform=managed `
        --port=8001 `
        --allow-unauthenticated `
        --timeout=300 `
        --memory=2Gi `
        --cpu=2 `
        --min-instances=0 `
        --max-instances=5 `
        --set-env-vars="LOG_LEVEL=INFO,PARSED_DATA_DIR=./parsed_data" `
        --update-secrets="GOOGLE_API_KEY=GOOGLE_API_KEY:latest,NEO4J_URI=NEO4J_URI:latest,NEO4J_USER=NEO4J_USER:latest,NEO4J_PASSWORD=NEO4J_PASSWORD:latest"
}
$urlKnowledge = Invoke-GcloudQuery { & $GCLOUD run services describe $SERVICE_KNOWLEDGE --region=$REGION --format="value(status.url)" }
if ($urlKnowledge) { $urlKnowledge = $urlKnowledge.Trim() }
if (-not $urlKnowledge) { throw "Could not resolve Knowledge Engine URL after deploy" }
Write-Ok "Knowledge Engine: $urlKnowledge"

# ---- Deploy Orchestrator ----
Write-Step "Deploying Orchestrator to Cloud Run"
Invoke-Native "deploy orchestrator" {
    & $GCLOUD run deploy $SERVICE_ORCH `
        --image=$imgOrchTag `
        --region=$REGION `
        --platform=managed `
        --port=8004 `
        --allow-unauthenticated `
        --timeout=300 `
        --memory=2Gi `
        --cpu=2 `
        --min-instances=0 `
        --max-instances=5 `
        --set-env-vars="LOG_LEVEL=INFO,ENVIRONMENT=production,PRIMARY_MODEL=gemini-2.5-flash,MAX_DAILY_SPEND_USD=50.0,MAX_SPEND_PER_ASSESSMENT_USD=5.0,GRAPHRAG_API_URL=$urlKnowledge,REDIS_URL=,CORS_ORIGINS=*" `
        --update-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest,DATABASE_URL=DATABASE_URL_ORCHESTRATOR:latest"
}
$urlOrch = Invoke-GcloudQuery { & $GCLOUD run services describe $SERVICE_ORCH --region=$REGION --format="value(status.url)" }
if ($urlOrch) { $urlOrch = $urlOrch.Trim() }
if (-not $urlOrch) { throw "Could not resolve Orchestrator URL after deploy" }
Write-Ok "Orchestrator: $urlOrch"

# ---- Build Frontend (needs orchestrator URL baked in) ----
Write-Step "Building Frontend image (NEXT_PUBLIC_API_URL=$urlOrch)"
Invoke-DockerBuild "frontend" "$root\frontend" $imgFrontendTag $imgFrontendLatest @(
    "NEXT_PUBLIC_API_URL=$urlOrch"
)

Write-Step "Pushing Frontend"
Invoke-Native "push frontend tag"    { docker push $imgFrontendTag }
Invoke-Native "push frontend latest" { docker push $imgFrontendLatest }

# ---- Deploy Frontend ----
Write-Step "Deploying Frontend to Cloud Run"
Invoke-Native "deploy frontend" {
    & $GCLOUD run deploy $SERVICE_FRONTEND `
        --image=$imgFrontendTag `
        --region=$REGION `
        --platform=managed `
        --port=3000 `
        --allow-unauthenticated `
        --timeout=300 `
        --memory=512Mi `
        --cpu=1 `
        --min-instances=0 `
        --max-instances=5 `
        --set-env-vars="NODE_ENV=production,HOSTNAME=0.0.0.0"
}
$urlFrontend = Invoke-GcloudQuery { & $GCLOUD run services describe $SERVICE_FRONTEND --region=$REGION --format="value(status.url)" }
if ($urlFrontend) { $urlFrontend = $urlFrontend.Trim() }
if (-not $urlFrontend) { throw "Could not resolve Frontend URL after deploy" }
Write-Ok "Frontend: $urlFrontend"

# ---- Health checks ----
Write-Step "Health checks"
$checks = @(
    @{ Name = "Knowledge Engine";Url = "$urlKnowledge/health" },
    @{ Name = "Orchestrator";    Url = "$urlOrch/health" },
    @{ Name = "Frontend";        Url = $urlFrontend }
)
foreach ($c in $checks) {
    try {
        $resp = Invoke-WebRequest -Uri $c.Url -Method Get -TimeoutSec 20 -UseBasicParsing -ErrorAction Stop
        Write-Ok "$($c.Name) -- HTTP $($resp.StatusCode)"
    } catch {
        Write-Err "$($c.Name) -- $($_.Exception.Message)"
    }
}

# ---- Summary ----
Write-Host ""
Write-Host "Deployment complete!" -ForegroundColor Yellow
Write-Host "  Knowledge Engine : $urlKnowledge"    -ForegroundColor White
Write-Host "  Orchestrator     : $urlOrch"         -ForegroundColor White
Write-Host "  Frontend         : $urlFrontend"     -ForegroundColor White
Write-Host "  Image tag        : $buildTag"        -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Cloud Run Console:" -ForegroundColor DarkGray
Write-Host "  https://console.cloud.google.com/run?project=$PROJECT_ID" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Share as live demo:" -ForegroundColor Yellow
Write-Host "  $urlFrontend" -ForegroundColor Cyan
Write-Host ""
