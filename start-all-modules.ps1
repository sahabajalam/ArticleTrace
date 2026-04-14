#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Starts the full AlloyCode Compliance Engine pipeline (backend + frontend)

.DESCRIPTION
    Orchestrates startup of the complete system:
    - Weaviate vector DB (Port 8080/50051) — required by knowledge_engine
    - Knowledge Engine: GraphRAG Legal Research Engine (Port 8001)
    - Orchestrator: Scan-driven Compliance Engine (Port 8004)
    - Frontend: AlloyCode Compliance Dashboard (Port 3000)

    In local mode the Python services run via UV on the host, but the
    Weaviate container is still started via docker-compose because the
    knowledge engine cannot run without it.

.PARAMETER Mode
    Startup mode: "docker" (uses root docker-compose.yml) or "local" (uses UV + npm)
    Default: local

.PARAMETER SkipFrontend
    Skip starting the frontend (backend only)
    Default: false

.PARAMETER SkipInfra
    Skip starting infra containers (Weaviate). Use when they are already up.
    Default: false

.EXAMPLE
    .\start-all-modules.ps1
    .\start-all-modules.ps1 -Mode docker
    .\start-all-modules.ps1 -Mode local -SkipFrontend
    .\start-all-modules.ps1 -Mode local -SkipInfra
#>

param(
    [ValidateSet("docker", "local")]
    [string]$Mode = "local",

    [switch]$SkipFrontend,

    [switch]$SkipInfra
)

$ErrorActionPreference = "Stop"

# ---------- Helpers ----------

function Write-Status {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "  ==========================================================" -ForegroundColor Cyan
    Write-Host "    $Text" -ForegroundColor Cyan
    Write-Host "  ==========================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Name, [string]$Detail, [string]$Color = "White")
    Write-Host "  > " -ForegroundColor $Color -NoNewline
    Write-Host "$Name " -ForegroundColor White -NoNewline
    Write-Host "- $Detail" -ForegroundColor DarkGray
}

function Test-PortOpen {
    param([int]$Port, [int]$TimeoutMs = 1000)
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $result = $tcp.BeginConnect("127.0.0.1", $Port, $null, $null)
        $success = $result.AsyncWaitHandle.WaitOne($TimeoutMs)
        $tcp.Close()
        return $success
    }
    catch {
        return $false
    }
}

function Stop-PortProcess {
    param([int]$Port)
    $conns = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
             Where-Object { $_.State -eq "Listen" }
    if (-not $conns) { return $false }

    $pids = $conns | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($p in $pids) {
        try {
            $proc = Get-Process -Id $p -ErrorAction SilentlyContinue
            if ($proc -and $proc.ProcessName -ne "System") {
                Write-Status "    Killing $($proc.ProcessName) (PID $p) on port $Port" "DarkGray"
                Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
            }
        }
        catch {
            # Process may have already exited
        }
    }
    # Brief pause for OS to release the port
    Start-Sleep -Milliseconds 500
    return $true
}

function Wait-ForService {
    param([string]$Name, [int]$Port, [int]$MaxWaitSec = 30)
    Write-Host "    Waiting for $Name on port $Port..." -ForegroundColor DarkGray -NoNewline
    for ($i = 0; $i -lt $MaxWaitSec; $i++) {
        if (Test-PortOpen -Port $Port) {
            Write-Host " ready!" -ForegroundColor Green
            return $true
        }
        Start-Sleep -Seconds 1
        Write-Host "." -ForegroundColor DarkGray -NoNewline
    }
    Write-Host " timeout!" -ForegroundColor Red
    return $false
}

# ---------- Project Root ----------

$ProjectRoot = $PSScriptRoot

Write-Header "AlloyCode Compliance Engine - Startup"
Write-Status "  Mode: $Mode" "Yellow"
Write-Status "  Root: $ProjectRoot" "DarkGray"
Write-Host ""

# ---------- Prerequisite Checks ----------

Write-Status "  Checking prerequisites..." "Yellow"

if ($Mode -eq "docker") {
    try {
        docker --version | Out-Null
        Write-Status "  [OK] Docker available" "Green"
    }
    catch {
        Write-Status "  [X] Docker not found. Install: https://www.docker.com/products/docker-desktop" "Red"
        exit 1
    }
}
else {
    # Local mode: check UV + Node, plus Docker (needed for Weaviate infra)
    try {
        $script:UvPath = (Get-Command uv -ErrorAction Stop).Source
        $uvVer = (& $script:UvPath --version 2>&1) -join ""
        Write-Status "  [OK] UV: $uvVer ($($script:UvPath))" "Green"
    }
    catch {
        Write-Status "  [X] UV not found. Install: https://docs.astral.sh/uv/" "Red"
        exit 1
    }

    if (-not $SkipInfra) {
        try {
            docker --version | Out-Null
            Write-Status "  [OK] Docker available (needed for Weaviate)" "Green"
        }
        catch {
            Write-Status "  [X] Docker not found. Install: https://www.docker.com/products/docker-desktop" "Red"
            Write-Status "      Or run with -SkipInfra if Weaviate is already running elsewhere." "DarkGray"
            exit 1
        }
    }

    if (-not $SkipFrontend) {
        try {
            $script:NpmPath = (Get-Command npm -ErrorAction Stop).Source
            $script:NodePath = (Get-Command node -ErrorAction Stop).Source
            $nodeVer = (& $script:NodePath --version 2>&1) -join ""
            Write-Status "  [OK] Node.js: $nodeVer" "Green"
        }
        catch {
            Write-Status "  [X] Node.js/npm not found. Install: https://nodejs.org/" "Red"
            exit 1
        }
    }
}

# ---------- Clean Up Stale Processes ----------

Write-Host ""
Write-Status "  Cleaning up stale processes..." "Yellow"

# Stop any existing PowerShell background jobs from previous runs
$existingJobs = Get-Job -ErrorAction SilentlyContinue
if ($existingJobs) {
    $existingJobs | Stop-Job -ErrorAction SilentlyContinue
    $existingJobs | Remove-Job -Force -ErrorAction SilentlyContinue
    Write-Status "  [OK] Cleared $($existingJobs.Count) stale background job(s)" "Green"
}

# Kill anything listening on our ports (8004, 8001, 3000)
$targetPorts = @(8004, 8001, 3000)
$killedAny = $false
foreach ($port in $targetPorts) {
    if (Stop-PortProcess -Port $port) {
        $killedAny = $true
    }
}

if ($killedAny) {
    Write-Status "  [OK] Freed occupied ports" "Green"
    # Extra pause to let OS fully release ports
    Start-Sleep -Seconds 2
}
else {
    Write-Status "  [OK] All ports are free" "Green"
}

# ---------- Check .env Files ----------

Write-Host ""
Write-Status "  Checking environment files..." "Yellow"

$backendModules = @("knowledge_engine", "orchestrator")
foreach ($mod in $backendModules) {
    $modPath = Join-Path $ProjectRoot $mod
    $envFile = Join-Path $modPath ".env"
    $envExample = Join-Path $modPath ".env.example"
    if (-not (Test-Path $envFile)) {
        if (Test-Path $envExample) {
            Write-Status "  [!] $mod - copied .env from .env.example" "Yellow"
            Copy-Item $envExample $envFile
        }
        else {
            Write-Status "  [!] $mod - no .env file found" "Yellow"
        }
    }
    else {
        Write-Status "  [OK] $mod .env" "Green"
    }
}

# Check root .env (used by docker-compose)
$rootEnv = Join-Path $ProjectRoot ".env"
if ($Mode -eq "docker" -and -not (Test-Path $rootEnv)) {
    Write-Status "  [!] Root .env not found (needed by docker-compose)" "Yellow"
}

# ---------- Docker Mode ----------

if ($Mode -eq "docker") {
    Write-Host ""
    Write-Header "Starting Backend (Docker Compose)"

    Push-Location $ProjectRoot
    try {
        Write-Status "  Building and starting all services..." "Yellow"
        docker-compose up -d --build
        Write-Status "  [OK] All backend containers started" "Green"
    }
    catch {
        Write-Status "  [X] docker-compose up failed: $_" "Red"
        Pop-Location
        exit 1
    }
    Pop-Location

    # Wait for backend services
    Write-Host ""
    Wait-ForService -Name "Knowledge Engine" -Port 8001
    Wait-ForService -Name "Orchestrator" -Port 8004

    # Start frontend
    if (-not $SkipFrontend) {
        Write-Host ""
        Write-Header "Starting Frontend"

        $frontendPath = Join-Path $ProjectRoot "frontend"
        $nodeModulesPath = Join-Path $frontendPath "node_modules"
        if (-not (Test-Path $nodeModulesPath)) {
            Write-Status "  Installing dependencies..." "Yellow"
            Push-Location $frontendPath
            npm install
            Pop-Location
        }

        $frontendJob = Start-Job -ScriptBlock {
            param($npmExe, $path)
            Set-Location $path
            & $npmExe run dev 2>&1
        } -ArgumentList $script:NpmPath, $frontendPath

        Write-Status "  [OK] Frontend starting (Job ID: $($frontendJob.Id))" "Green"
        Wait-ForService -Name "Frontend" -Port 3000 -MaxWaitSec 45
    }
}

# ---------- Local Mode ----------

if ($Mode -eq "local") {
    # ---- Infra (Weaviate) ----
    if (-not $SkipInfra) {
        Write-Host ""
        Write-Header "Starting Infra (Weaviate)"

        Push-Location $ProjectRoot
        try {
            Write-Status "  Starting Weaviate container..." "Yellow"
            docker compose up -d weaviate | Out-Null
            Write-Status "  [OK] Weaviate container requested" "Green"
        }
        catch {
            Write-Status "  [X] Failed to start Weaviate: $_" "Red"
            Pop-Location
            exit 1
        }
        Pop-Location

        if (-not (Wait-ForService -Name "Weaviate" -Port 8080 -MaxWaitSec 60)) {
            Write-Status "  [X] Weaviate failed to come up on port 8080" "Red"
            exit 1
        }
    }
    else {
        Write-Host ""
        Write-Status "  Skipping infra startup (-SkipInfra)" "DarkGray"
    }

    Write-Host ""
    Write-Header "Starting Backend Services (UV)"

    $modules = @(
        @{ Name = "knowledge_engine"; Desc = "GraphRAG Knowledge Engine"; Port = 8001; Color = "Blue" },
        @{ Name = "orchestrator";     Desc = "Compliance Agent";          Port = 8004; Color = "Green" }
    )

    $jobs = @()

    foreach ($module in $modules) {
        $modulePath = Join-Path $ProjectRoot $module.Name

        Write-Step $module.Name "$($module.Desc) -> :$($module.Port)" $module.Color

        $job = Start-Job -ScriptBlock {
            param($uvExe, $path, $port, $name)
            Set-Location $path
            $env:PYTHONUNBUFFERED = "1"
            & $uvExe run python -m uvicorn src.api.main:app --reload --port $port --host 0.0.0.0 2>&1
        } -ArgumentList $script:UvPath, $modulePath, $module.Port, $module.Name

        $jobs += @{ Name = $module.Name; Job = $job; Port = $module.Port }
        Write-Status "    Job ID: $($job.Id)" "DarkGray"
        Start-Sleep -Seconds 3
    }

    # Give jobs a moment to either start or fail
    Start-Sleep -Seconds 5

    # Wait for each backend service and check for early failures
    Write-Host ""
    foreach ($j in $jobs) {
        # Check if job crashed immediately
        $jobObj = Get-Job -Id $j.Job.Id -ErrorAction SilentlyContinue
        if ($jobObj.State -eq "Failed") {
            Write-Status "  [X] $($j.Name) failed to start!" "Red"
            # Show stdout
            $output = Receive-Job -Id $j.Job.Id -ErrorAction SilentlyContinue 2>&1
            foreach ($line in $output) {
                Write-Status "    $line" "Red"
            }
            # Show job error details
            if ($jobObj.ChildJobs) {
                foreach ($child in $jobObj.ChildJobs) {
                    if ($child.Error) {
                        foreach ($err in $child.Error) {
                            Write-Status "    ERROR: $err" "Red"
                        }
                    }
                }
            }
            continue
        }
        if ($jobObj.State -eq "Completed") {
            Write-Status "  [X] $($j.Name) exited unexpectedly!" "Red"
            $output = Receive-Job -Id $j.Job.Id -ErrorAction SilentlyContinue 2>&1
            foreach ($line in $output) {
                Write-Status "    $line" "Yellow"
            }
            continue
        }
        Wait-ForService -Name $j.Name -Port $j.Port -MaxWaitSec 30
    }

    # Start frontend
    if (-not $SkipFrontend) {
        Write-Host ""
        Write-Header "Starting Frontend (Next.js)"

        $frontendPath = Join-Path $ProjectRoot "frontend"

        # Install deps if needed
        $nodeModulesPath = Join-Path $frontendPath "node_modules"
        if (-not (Test-Path $nodeModulesPath)) {
            Write-Status "  Installing npm dependencies..." "Yellow"
            Push-Location $frontendPath
            npm install
            Pop-Location
        }

        $frontendJob = Start-Job -ScriptBlock {
            param($npmExe, $path)
            Set-Location $path
            $env:NEXT_PUBLIC_API_URL = "http://localhost:8004"
            & $npmExe run dev 2>&1
        } -ArgumentList $script:NpmPath, $frontendPath

        $jobs += @{ Name = "frontend"; Job = $frontendJob; Port = 3000 }
        Write-Step "frontend" "AlloyCode Dashboard -> :3000" "Cyan"
        Write-Status "    Job ID: $($frontendJob.Id)" "DarkGray"

        Wait-ForService -Name "Frontend" -Port 3000 -MaxWaitSec 45
    }
}

# ---------- Summary ----------

Write-Host ""
Write-Header "Pipeline Ready"

Write-Status "  Infra:" "Cyan"
Write-Status "    Weaviate (vector DB)        -> http://localhost:8080" "Magenta"
Write-Host ""
Write-Status "  Backend:" "Cyan"
Write-Status "    Knowledge Engine (GraphRAG) -> http://localhost:8001" "Blue"
Write-Status "    Orchestrator (Agent)        -> http://localhost:8004" "Green"

if (-not $SkipFrontend) {
    Write-Host ""
    Write-Status "  Frontend:" "Cyan"
    Write-Status "    AlloyCode Dashboard             -> http://localhost:3000" "Cyan"
}

Write-Host ""
Write-Status "  Commands:" "Yellow"
if ($Mode -eq "local") {
    Write-Status "    View logs   -> Receive-Job -Id <id> -Keep" "DarkGray"
    Write-Status "    List jobs   -> Get-Job" "DarkGray"
    Write-Status "    Stop all    -> .\stop-all-modules.ps1 -Mode local" "DarkGray"
}
else {
    Write-Status "    View logs   -> docker-compose logs -f" "DarkGray"
    Write-Status "    Status      -> docker-compose ps" "DarkGray"
    Write-Status "    Stop all    -> .\stop-all-modules.ps1" "DarkGray"
}

Write-Host ""
Write-Status "  [OK] All systems online" "Green"
Write-Host ""
