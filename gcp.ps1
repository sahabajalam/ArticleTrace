#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Unified GCP lifecycle controller for ArticleTrace.

.DESCRIPTION
    Merges the previous deploy_gcp.ps1 / setup-secrets.ps1 / deploy.ps1 /
    deploy.clean.ps1 / deploy.fast.ps1 / cleanup_gcp.ps1 scripts into a
    single entry point with a verb parameter.

    Actions:
      setup         First-time GCP setup: project, APIs, Artifact Registry,
                    and secrets. Does NOT build or deploy.
      secrets       Push .env values from orchestrator/ and knowledge_engine/
                    into Secret Manager and grant Cloud Run SA access.
      deploy        Clean build + deploy via deploy.ps1 (no Docker cache).
      deploy-fast   Cached build + deploy via deploy.ps1 -UseCache -SkipCachePrune.
      cleanup       Delete Cloud Run services, Artifact Registry repo, secrets,
                    and local Docker images. Optionally also delete the project.

.PARAMETER Action
    setup | secrets | deploy | deploy-fast | cleanup | help

.PARAMETER ProjectId
    GCP project ID. Default: gdpreuai.

.PARAMETER Region
    GCP region. Default: europe-west1.

.PARAMETER RepoName
    Artifact Registry repo name. Default: aegis-images.

.PARAMETER IncludeProject
    cleanup only: also delete the GCP project itself.

.EXAMPLE
    .\gcp.ps1 -Action setup
    .\gcp.ps1 -Action secrets
    .\gcp.ps1 -Action deploy
    .\gcp.ps1 -Action deploy-fast
    .\gcp.ps1 -Action cleanup
    .\gcp.ps1 -Action cleanup -IncludeProject
#>

param(
    [Parameter(Position = 0)]
    [ValidateSet("setup", "secrets", "deploy", "deploy-fast", "cleanup", "help")]
    [string]$Action,

    [string]$ProjectId = "gdpreuai",
    [string]$Region    = "europe-west1",
    [string]$RepoName  = "aegis-images",

    [switch]$IncludeProject
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = $PSScriptRoot
if (-not $Root) { $Root = (Get-Location).Path }

# ---------- Shared helpers ----------

function Write-Header([string]$msg) {
    Write-Host "`n$('=' * 60)" -ForegroundColor Cyan
    Write-Host "  $msg" -ForegroundColor Cyan
    Write-Host "$('=' * 60)" -ForegroundColor Cyan
}
function Write-Step([string]$msg) { Write-Host "`n[+] $msg" -ForegroundColor Yellow }
function Write-OK([string]$msg)   { Write-Host "    [OK] $msg" -ForegroundColor Green }
function Write-Warn([string]$msg) { Write-Host "    [!!] $msg" -ForegroundColor DarkYellow }
function Write-Fail([string]$msg) { Write-Host "    [ERR] $msg" -ForegroundColor Red }
function Write-Skip([string]$msg) { Write-Host "    [--] $msg" -ForegroundColor DarkGray }

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
    }
    finally {
        $ErrorActionPreference = $prev
    }
    if ($exitCode -ne 0) { throw "$Label failed with exit code $exitCode" }
}

function Invoke-GcloudQuery {
    param([Parameter(Mandatory)][scriptblock]$Command)
    $prev = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        $result = & $Command 2>$null
    }
    finally {
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
        if ($LASTEXITCODE -eq 0) { Write-OK $Label }
        else { Write-Warn "$Label -- skipped (not found or already deleted)" }
    }
    finally {
        $ErrorActionPreference = $prev
    }
}

function Read-Env([string]$file, [string]$key) {
    if (-not (Test-Path $file)) { return "" }
    $line = Select-String -Path $file -Pattern "^$key=" | Select-Object -First 1
    if (-not $line) { return "" }
    return ($line.Line -split "=", 2)[1].Trim()
}

function Get-Gcloud {
    return (Get-Command gcloud.cmd -ErrorAction Stop).Source
}

function Push-Secret {
    param([string]$Gcloud, [string]$Name, [string]$Value)
    if (-not $Value -or $Value.Length -lt 5) {
        Write-Skip "$Name (empty or too short)"
        return
    }
    # Use WriteAllBytes to avoid BOM / trailing CRLF corrupting secret values.
    $tmp = [System.IO.Path]::GetTempFileName()
    try {
        [System.IO.File]::WriteAllBytes($tmp, [System.Text.Encoding]::UTF8.GetBytes($Value))
        $exists = Invoke-GcloudQuery { & $Gcloud secrets describe $Name --format="value(name)" }
        if ($exists) {
            Write-Step "Updating: $Name"
            Invoke-Native "secret version add $Name" {
                & $Gcloud secrets versions add $Name --data-file=$tmp --quiet 2>$null
            }
        }
        else {
            Write-Step "Creating: $Name"
            Invoke-Native "secret create $Name" {
                & $Gcloud secrets create $Name --data-file=$tmp --replication-policy=automatic --quiet 2>$null
            }
        }
        Write-OK "$Name stored"
    }
    finally {
        Remove-Item $tmp -Force -ErrorAction SilentlyContinue
    }
}

# ---------- Usage / interactive menu ----------

function Show-Usage {
    Write-Host ""
    Write-Host "  gcp.ps1 - ArticleTrace GCP lifecycle controller" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Usage: .\gcp.ps1 -Action <action> [options]" -ForegroundColor White
    Write-Host ""
    Write-Host "  Actions:" -ForegroundColor Yellow
    Write-Host "    setup          First-time GCP setup: project, APIs, Artifact Registry, secrets" -ForegroundColor Gray
    Write-Host "    secrets        Push .env values into Secret Manager" -ForegroundColor Gray
    Write-Host "    deploy         Clean build + deploy (no Docker cache)" -ForegroundColor Gray
    Write-Host "    deploy-fast    Cached build + deploy (fast; for code-only changes)" -ForegroundColor Gray
    Write-Host "    cleanup        Delete Cloud Run services, repo, secrets, local images" -ForegroundColor Gray
    Write-Host "    help           Show this message" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Options:" -ForegroundColor Yellow
    Write-Host "    -ProjectId <id>        Default: gdpreuai" -ForegroundColor Gray
    Write-Host "    -Region <region>       Default: europe-west1" -ForegroundColor Gray
    Write-Host "    -RepoName <name>       Default: aegis-images" -ForegroundColor Gray
    Write-Host "    -IncludeProject        cleanup only. Also delete the GCP project" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Examples:" -ForegroundColor Yellow
    Write-Host "    .\gcp.ps1 -Action setup" -ForegroundColor DarkGray
    Write-Host "    .\gcp.ps1 -Action secrets" -ForegroundColor DarkGray
    Write-Host "    .\gcp.ps1 -Action deploy" -ForegroundColor DarkGray
    Write-Host "    .\gcp.ps1 -Action deploy-fast" -ForegroundColor DarkGray
    Write-Host "    .\gcp.ps1 -Action cleanup" -ForegroundColor DarkGray
    Write-Host "    .\gcp.ps1 -Action cleanup -IncludeProject" -ForegroundColor DarkGray
    Write-Host ""
}

function Read-InteractiveAction {
    Show-Usage
    Write-Host "  Select an action:" -ForegroundColor Yellow
    Write-Host "    [1] setup         (one-time: project, APIs, registry, secrets)" -ForegroundColor Gray
    Write-Host "    [2] secrets       (push .env -> Secret Manager)" -ForegroundColor Gray
    Write-Host "    [3] deploy        (clean build, no cache)" -ForegroundColor Gray
    Write-Host "    [4] deploy-fast   (cached build, for code-only changes)" -ForegroundColor Gray
    Write-Host "    [5] cleanup       (delete services/repo/secrets)" -ForegroundColor Gray
    Write-Host "    [6] cleanup +project  (also delete the GCP project)" -ForegroundColor Gray
    Write-Host "    [q] quit" -ForegroundColor Gray
    Write-Host ""
    $choice = Read-Host "  Choice"
    switch ($choice.Trim().ToLower()) {
        "1"           { $script:Action = "setup" }
        "setup"       { $script:Action = "setup" }
        "2"           { $script:Action = "secrets" }
        "secrets"     { $script:Action = "secrets" }
        "3"           { $script:Action = "deploy" }
        "deploy"      { $script:Action = "deploy" }
        "4"           { $script:Action = "deploy-fast" }
        "deploy-fast" { $script:Action = "deploy-fast" }
        "5"           { $script:Action = "cleanup" }
        "cleanup"     { $script:Action = "cleanup" }
        "6"           { $script:Action = "cleanup"; $script:IncludeProject = $true }
        "q"           { Write-Host "  Cancelled." -ForegroundColor DarkGray; return $false }
        "quit"        { Write-Host "  Cancelled." -ForegroundColor DarkGray; return $false }
        ""            { Write-Host "  No choice entered. Cancelled." -ForegroundColor DarkGray; return $false }
        default       { Write-Host "  Unknown choice '$choice'." -ForegroundColor Red; return $false }
    }
    return $true
}

if ($Action -eq "help") { Show-Usage; return }
if (-not $Action) {
    if (-not (Read-InteractiveAction)) { return }
}

# ---------- Action: secrets ----------

function Invoke-Secrets {
    $gcloud = Get-Gcloud
    $env:CLOUDSDK_CORE_DISABLE_PROMPTS = "1"

    Write-Step "Setting project to $ProjectId"
    Invoke-Native "set project" { & $gcloud config set project $ProjectId --quiet }

    Write-Step "Enabling Secret Manager API"
    Invoke-Native "enable secretmanager" { & $gcloud services enable secretmanager.googleapis.com --quiet }

    $orchEnv = Join-Path $Root "orchestrator\.env"
    $keEnv   = Join-Path $Root "knowledge_engine\.env"

    Write-Step "Pushing secrets from .env files..."
    Push-Secret $gcloud "GEMINI_API_KEY"            (Read-Env $orchEnv "GEMINI_API_KEY")
    Push-Secret $gcloud "GOOGLE_API_KEY"            (Read-Env $keEnv   "GOOGLE_API_KEY")
    Push-Secret $gcloud "DATABASE_URL_ORCHESTRATOR" (Read-Env $orchEnv "DATABASE_URL")
    Push-Secret $gcloud "NEO4J_URI"                 (Read-Env $keEnv   "NEO4J_URI")
    Push-Secret $gcloud "NEO4J_USER"                (Read-Env $keEnv   "NEO4J_USER")
    Push-Secret $gcloud "NEO4J_PASSWORD"            (Read-Env $keEnv   "NEO4J_PASSWORD")

    Write-Step "Granting Secret Manager access to Cloud Run service account"
    $projectNum = (& $gcloud projects describe $ProjectId --format="value(projectNumber)" 2>$null).Trim()
    $sa = "$projectNum-compute@developer.gserviceaccount.com"
    Invoke-Native "iam binding" {
        & $gcloud projects add-iam-policy-binding $ProjectId `
            --member="serviceAccount:$sa" `
            --role="roles/secretmanager.secretAccessor" `
            --quiet 2>$null | Out-Null
    }
    Write-OK "IAM: $sa -> secretAccessor"

    Write-Host ""
    Write-Host "All secrets pushed. You can now run: .\gcp.ps1 -Action deploy" -ForegroundColor Yellow
    Write-Host ""
}

# ---------- Action: setup ----------

function Invoke-Setup {
    $gcloud = Get-Gcloud
    $env:CLOUDSDK_CORE_DISABLE_PROMPTS = "1"
    $registry = "$Region-docker.pkg.dev/$ProjectId/$RepoName"

    Write-Header "PREREQUISITE CHECK"
    $account = Invoke-GcloudQuery { & $gcloud auth list --filter="status:ACTIVE" --format="value(account)" }
    if (-not $account) {
        Write-Fail "No active gcloud account. Run: gcloud auth login"
        exit 1
    }
    Write-OK "gcloud authenticated as: $account"

    Write-Header "GCP PROJECT SETUP"
    Write-Step "Setting active project to: $ProjectId"
    $existing = Invoke-GcloudQuery { & $gcloud projects list --filter="projectId=$ProjectId" --format="value(projectId)" }
    if ($existing -eq $ProjectId) {
        Write-OK "Project '$ProjectId' already exists -- skipping creation."
    }
    else {
        Write-Step "Creating GCP project '$ProjectId'..."
        Invoke-Native "project create" { & $gcloud projects create $ProjectId --name="ArticleTrace" }
        Write-OK "Project created."
    }
    Invoke-Native "set project" { & $gcloud config set project $ProjectId --quiet }
    Write-OK "Active project: $ProjectId"

    Write-Header "ENABLING APIS"
    $apis = @("run.googleapis.com", "artifactregistry.googleapis.com", "secretmanager.googleapis.com")
    foreach ($api in $apis) {
        Write-Step "Enabling $api ..."
        Invoke-Native "enable $api" { & $gcloud services enable $api --quiet }
        Write-OK "$api enabled"
    }

    Write-Header "ARTIFACT REGISTRY"
    Write-Step "Checking repo '$RepoName' in $Region..."
    $repoExists = Invoke-GcloudQuery { & $gcloud artifacts repositories list --location=$Region --filter="name~/$RepoName`$" --format="value(name)" }
    if ($repoExists) {
        Write-OK "Repo already exists."
    }
    else {
        Write-Step "Creating Artifact Registry repo..."
        Invoke-Native "create artifact repo" {
            & $gcloud artifacts repositories create $RepoName `
                --repository-format=docker `
                --location=$Region `
                --description="ArticleTrace images" `
                --quiet
        }
        Write-OK "Repo created: $registry"
    }

    Write-Header "SECRET MANAGER"
    Write-Step "Pushing secrets (inline)..."
    Invoke-Secrets

    Write-Header "GCP SETUP COMPLETE"
    Write-Host @"

  Project  : $ProjectId
  Region   : $Region
  Registry : $registry

  Next steps:
    .\gcp.ps1 -Action deploy       # full clean build + deploy
    .\gcp.ps1 -Action deploy-fast  # fast cached build + deploy

"@ -ForegroundColor Cyan
}

# ---------- Actions: deploy / deploy-fast ----------

function Invoke-DockerBuild {
    param(
        [string]$Label,
        [string]$ContextPath,
        [string]$Tag,
        [string]$LatestTag,
        [string[]]$BuildArgsList = @(),
        [switch]$UseCache
    )
    $dockerArgs = @("build", "--platform", "linux/amd64")
    if (-not $UseCache) { $dockerArgs += "--no-cache" }
    foreach ($ba in $BuildArgsList) { $dockerArgs += @("--build-arg", $ba) }
    $dockerArgs += @("-t", $Tag, "-t", $LatestTag, $ContextPath)
    Invoke-Native "docker build $Label" { docker @dockerArgs }
}

function Invoke-Deploy {
    param([switch]$Fast)

    $REGION            = $Region
    $ARTIFACT_REPO     = $RepoName
    $PROJECT_ID        = $ProjectId
    $SERVICE_KNOWLEDGE = "aegis-knowledge-engine"
    $SERVICE_ORCH      = "aegis-orchestrator"
    $SERVICE_FRONTEND  = "aegis-frontend"

    $skipCachePrune = [bool]$Fast

    # ---- Pre-flight ----
    Write-Step "Pre-flight checks"
    if (-not (Get-Command gcloud.cmd -ErrorAction SilentlyContinue)) {
        Write-Fail "gcloud CLI not found. Install: https://cloud.google.com/sdk/docs/install"
        exit 1
    }
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Fail "Docker not found. Install Docker Desktop."
        exit 1
    }

    $gcloud = Get-Gcloud
    Invoke-Native "gcloud config set project" { & $gcloud config set project $PROJECT_ID --quiet }
    Write-OK "Project: $PROJECT_ID"
    Write-OK "Region:  $REGION"
    if ($Fast) { Write-OK "Build mode: FAST (Docker cache enabled)" }
    else       { Write-OK "Build mode: CLEAN (no cache)" }

    $env:CLOUDSDK_CORE_DISABLE_PROMPTS = "1"

    # ---- Verify required secrets ----
    Write-Step "Verifying required secrets in Secret Manager"
    $requiredSecrets = @(
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "DATABASE_URL_ORCHESTRATOR",
        "NEO4J_URI",
        "NEO4J_USER",
        "NEO4J_PASSWORD"
    )
    # Use Invoke-GcloudQuery so the captured output is returned through the
    # function boundary rather than buried inside a scriptblock's local scope.
    $rawList = Invoke-GcloudQuery { & $gcloud secrets list --format="value(name)" }
    $existingSecrets = @()
    if ($rawList) {
        $existingSecrets = ($rawList -split "`r?`n") |
            ForEach-Object { $_.Trim() } |
            Where-Object { $_ -ne "" }
    }
    $missing = @()
    foreach ($s in $requiredSecrets) {
        if ($existingSecrets -contains $s) { Write-OK $s }
        else { Write-Fail "$s -- MISSING"; $missing += $s }
    }
    if ($missing.Count -gt 0) {
        Write-Host "`nRun .\gcp.ps1 -Action secrets to push your .env values into Secret Manager." -ForegroundColor Yellow
        exit 1
    }

    # ---- Image tags ----
    $buildTag = "manual-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    $reg      = "$REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO"

    $imgKnowledgeTag    = "$reg/knowledge-engine:$buildTag"
    $imgKnowledgeLatest = "$reg/knowledge-engine:latest"
    $imgOrchTag         = "$reg/orchestrator:$buildTag"
    $imgOrchLatest      = "$reg/orchestrator:latest"
    $imgFrontendTag     = "$reg/frontend:$buildTag"
    $imgFrontendLatest  = "$reg/frontend:latest"

    # ---- Docker auth ----
    Write-Step "Configuring Artifact Registry auth"
    Invoke-Native "docker auth configure" { & $gcloud auth configure-docker "$REGION-docker.pkg.dev" --quiet }

    # ---- Cache prune ----
    $shouldPrune = (-not $Fast) -and (-not $skipCachePrune)
    if ($shouldPrune) {
        Write-Step "Pruning Docker build cache"
        Invoke-Native "docker builder prune" { docker builder prune -af }
    }
    else {
        Write-Step "Skipping cache prune"
    }

    # ---- Build backend images ----
    Write-Step "Building Knowledge Engine image"
    Invoke-DockerBuild -Label "knowledge-engine" -ContextPath (Join-Path $Root "knowledge_engine") `
        -Tag $imgKnowledgeTag -LatestTag $imgKnowledgeLatest -UseCache:$Fast

    Write-Step "Building Orchestrator image"
    Invoke-DockerBuild -Label "orchestrator" -ContextPath (Join-Path $Root "orchestrator") `
        -Tag $imgOrchTag -LatestTag $imgOrchLatest -UseCache:$Fast

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
        & $gcloud run deploy $SERVICE_KNOWLEDGE `
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
    $urlKnowledge = Invoke-GcloudQuery { & $gcloud run services describe $SERVICE_KNOWLEDGE --region=$REGION --format="value(status.url)" }
    if ($urlKnowledge) { $urlKnowledge = $urlKnowledge.Trim() }
    if (-not $urlKnowledge) { throw "Could not resolve Knowledge Engine URL after deploy" }
    Write-OK "Knowledge Engine: $urlKnowledge"

    # ---- Deploy Orchestrator ----
    Write-Step "Deploying Orchestrator to Cloud Run"
    Invoke-Native "deploy orchestrator" {
        & $gcloud run deploy $SERVICE_ORCH `
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
    $urlOrch = Invoke-GcloudQuery { & $gcloud run services describe $SERVICE_ORCH --region=$REGION --format="value(status.url)" }
    if ($urlOrch) { $urlOrch = $urlOrch.Trim() }
    if (-not $urlOrch) { throw "Could not resolve Orchestrator URL after deploy" }
    Write-OK "Orchestrator: $urlOrch"

    # ---- Build Frontend (bakes orchestrator URL) ----
    Write-Step "Building Frontend image (NEXT_PUBLIC_API_URL=$urlOrch)"
    Invoke-DockerBuild -Label "frontend" -ContextPath (Join-Path $Root "frontend") `
        -Tag $imgFrontendTag -LatestTag $imgFrontendLatest -UseCache:$Fast `
        -BuildArgsList @("NEXT_PUBLIC_API_URL=$urlOrch")

    Write-Step "Pushing Frontend"
    Invoke-Native "push frontend tag"    { docker push $imgFrontendTag }
    Invoke-Native "push frontend latest" { docker push $imgFrontendLatest }

    # ---- Deploy Frontend ----
    Write-Step "Deploying Frontend to Cloud Run"
    Invoke-Native "deploy frontend" {
        & $gcloud run deploy $SERVICE_FRONTEND `
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
    $urlFrontend = Invoke-GcloudQuery { & $gcloud run services describe $SERVICE_FRONTEND --region=$REGION --format="value(status.url)" }
    if ($urlFrontend) { $urlFrontend = $urlFrontend.Trim() }
    if (-not $urlFrontend) { throw "Could not resolve Frontend URL after deploy" }
    Write-OK "Frontend: $urlFrontend"

    # ---- Health checks ----
    Write-Step "Health checks"
    $checks = @(
        @{ Name = "Knowledge Engine"; Url = "$urlKnowledge/health" },
        @{ Name = "Orchestrator";     Url = "$urlOrch/health" },
        @{ Name = "Frontend";         Url = $urlFrontend }
    )
    foreach ($c in $checks) {
        try {
            $resp = Invoke-WebRequest -Uri $c.Url -Method Get -TimeoutSec 20 -UseBasicParsing -ErrorAction Stop
            Write-OK "$($c.Name) -- HTTP $($resp.StatusCode)"
        }
        catch {
            Write-Fail "$($c.Name) -- $($_.Exception.Message)"
        }
    }

    # ---- Summary ----
    Write-Host ""
    Write-Host "Deployment complete!" -ForegroundColor Yellow
    Write-Host "  Knowledge Engine : $urlKnowledge" -ForegroundColor White
    Write-Host "  Orchestrator     : $urlOrch"      -ForegroundColor White
    Write-Host "  Frontend         : $urlFrontend"  -ForegroundColor White
    Write-Host "  Image tag        : $buildTag"     -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  Cloud Run Console:" -ForegroundColor DarkGray
    Write-Host "  https://console.cloud.google.com/run?project=$PROJECT_ID" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  Share as live demo:" -ForegroundColor Yellow
    Write-Host "  $urlFrontend" -ForegroundColor Cyan
    Write-Host ""
}

# ---------- Action: cleanup ----------

function Invoke-Cleanup {
    $gcloud = Get-Gcloud
    $env:CLOUDSDK_CORE_DISABLE_PROMPTS = "1"
    Invoke-GcloudSafe "set project" { & $gcloud config set project $ProjectId --quiet }

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
        return
    }

    Write-Header "DELETING CLOUD RUN SERVICES"
    $services = @("aegis-knowledge-engine", "aegis-orchestrator", "aegis-frontend")
    foreach ($svc in $services) {
        Write-Step "Deleting service: $svc"
        Invoke-GcloudSafe "deleted $svc" {
            & $gcloud run services delete $svc --region=$Region --quiet
        }
    }

    Write-Header "CLEANING ARTIFACT REGISTRY"
    $repoExists = Invoke-GcloudQuery {
        & $gcloud artifacts repositories list --location=$Region --filter="name~/$RepoName`$" --format="value(name)"
    }
    if ($repoExists) {
        Write-Step "Deleting entire repo '$RepoName' (all images)..."
        Invoke-GcloudSafe "deleted repo $RepoName" {
            & $gcloud artifacts repositories delete $RepoName --location=$Region --quiet
        }
    }
    else {
        Write-OK "Repo '$RepoName' does not exist -- nothing to delete"
    }

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
        Invoke-GcloudSafe "deleted $s" { & $gcloud secrets delete $s --quiet }
    }

    Write-Header "PRUNING LOCAL DOCKER ARTIFACTS"
    $registry = "$Region-docker.pkg.dev/$ProjectId/$RepoName"
    Write-Step "Removing local images matching: $registry/*"
    $prev = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        $localImages = docker images --format "{{.Repository}}:{{.Tag}}" 2>$null |
                       Where-Object { $_ -like "$registry/*" }
    }
    finally {
        $ErrorActionPreference = $prev
    }
    if ($localImages) {
        foreach ($img in $localImages) {
            Write-Step "Removing: $img"
            docker rmi $img 2>$null | Out-Null
        }
        Write-OK "Local images removed"
    }
    else {
        Write-OK "No local images to remove"
    }

    Write-Step "Pruning Docker build cache"
    $prev = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        docker builder prune -af 2>$null | Out-Null
    }
    finally {
        $ErrorActionPreference = $prev
    }
    Write-OK "Build cache pruned"

    if ($IncludeProject) {
        Write-Header "DELETING GCP PROJECT"
        Write-Host "  WARNING: This deletes EVERYTHING in project '$ProjectId'!" -ForegroundColor Red
        $confirm2 = Read-Host "  Type the project ID to confirm"
        if ($confirm2 -eq $ProjectId) {
            Invoke-GcloudSafe "deleted project $ProjectId" {
                & $gcloud projects delete $ProjectId --quiet
            }
        }
        else {
            Write-Warn "Project ID did not match -- skipping project deletion"
        }
    }

    Write-Header "CLEANUP COMPLETE"
    Write-Host @"

  All ArticleTrace resources have been removed from '$ProjectId'.

  To redeploy from scratch:
    1. .\gcp.ps1 -Action setup      # project, APIs, registry, secrets
    2. .\gcp.ps1 -Action deploy     # clean build + deploy

"@ -ForegroundColor Cyan
}

# ---------- Dispatch ----------

switch ($Action) {
    "setup"       { Invoke-Setup }
    "secrets"     { Invoke-Secrets }
    "deploy"      { Invoke-Deploy }
    "deploy-fast" { Invoke-Deploy -Fast }
    "cleanup"     { Invoke-Cleanup }
}
