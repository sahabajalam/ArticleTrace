#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Unified lifecycle controller for the AlloyCode Compliance Engine pipeline.

.DESCRIPTION
    Merges the previous start-all-modules / stop-all-modules / terminate-ports /
    restart_orch scripts into a single entry point with a verb parameter.

    Actions:
      start        Start the full pipeline (Weaviate + knowledge_engine +
                   orchestrator + frontend). Honors -Mode, -SkipFrontend, -SkipInfra.
      stop         Stop everything started by "start". Honors -Mode, -SkipInfra.
      restart-orch Kill whatever is listening on :8004, clear orchestrator
                   __pycache__, and relaunch the orchestrator as a background job.
      kill-ports   Terminate any process listening on -Ports (defaults to the
                   pipeline ports 8004/8001/3000). Use -All for every user-space
                   listener above 1024.

.PARAMETER Action
    start | stop | restart-orch | kill-ports

.PARAMETER Mode
    docker | local (used by start/stop). Default: local.

.PARAMETER SkipFrontend
    start only: skip the Next.js frontend.

.PARAMETER SkipInfra
    start/stop only: skip the Weaviate container.

.PARAMETER Ports
    kill-ports only: ports to terminate. Default: 8004, 8001, 3000.

.PARAMETER All
    kill-ports only: terminate every user-space TCP listener (> 1024).

.EXAMPLE
    .\pipeline.ps1 -Action start
    .\pipeline.ps1 -Action start -Mode docker
    .\pipeline.ps1 -Action start -Mode local -SkipFrontend
    .\pipeline.ps1 -Action stop
    .\pipeline.ps1 -Action stop -SkipInfra
    .\pipeline.ps1 -Action restart-orch
    .\pipeline.ps1 -Action kill-ports
    .\pipeline.ps1 -Action kill-ports -Ports 9000,9001
    .\pipeline.ps1 -Action kill-ports -All
#>

param(
    [Parameter(Position = 0)]
    [ValidateSet("start", "stop", "restart-orch", "kill-ports", "help")]
    [string]$Action,

    [ValidateSet("docker", "local")]
    [string]$Mode = "local",

    [switch]$SkipFrontend,
    [switch]$SkipInfra,

    [int[]]$Ports = @(8004, 8001, 3000),
    [switch]$All
)

function Show-Usage {
    Write-Host ""
    Write-Host "  pipeline.ps1 - AlloyCode Compliance Engine lifecycle controller" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Usage: .\pipeline.ps1 -Action <action> [options]" -ForegroundColor White
    Write-Host ""
    Write-Host "  Actions:" -ForegroundColor Yellow
    Write-Host "    start          Start Weaviate + knowledge_engine + orchestrator + frontend" -ForegroundColor Gray
    Write-Host "    stop           Stop jobs, free ports, stop Weaviate" -ForegroundColor Gray
    Write-Host "    restart-orch   Kill :8004, clear orchestrator __pycache__, relaunch orchestrator" -ForegroundColor Gray
    Write-Host "    kill-ports     Terminate processes on -Ports (default 8004,8001,3000)" -ForegroundColor Gray
    Write-Host "    help           Show this message" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Options:" -ForegroundColor Yellow
    Write-Host "    -Mode <docker|local>   start/stop only. Default: local" -ForegroundColor Gray
    Write-Host "    -SkipFrontend          start only. Skip the Next.js frontend" -ForegroundColor Gray
    Write-Host "    -SkipInfra             start/stop only. Skip the Weaviate container" -ForegroundColor Gray
    Write-Host "    -Ports <int[]>         kill-ports only. Ports to terminate" -ForegroundColor Gray
    Write-Host "    -All                   kill-ports only. Terminate every user-space listener (>1024)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Examples:" -ForegroundColor Yellow
    Write-Host "    .\pipeline.ps1 -Action start" -ForegroundColor DarkGray
    Write-Host "    .\pipeline.ps1 -Action start -Mode docker" -ForegroundColor DarkGray
    Write-Host "    .\pipeline.ps1 -Action start -SkipFrontend" -ForegroundColor DarkGray
    Write-Host "    .\pipeline.ps1 -Action stop -SkipInfra" -ForegroundColor DarkGray
    Write-Host "    .\pipeline.ps1 -Action restart-orch" -ForegroundColor DarkGray
    Write-Host "    .\pipeline.ps1 -Action kill-ports -Ports 9000,9001" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  Full help: Get-Help .\pipeline.ps1 -Detailed" -ForegroundColor DarkGray
    Write-Host ""
}

function Read-InteractiveAction {
    Show-Usage
    Write-Host "  Select an action:" -ForegroundColor Yellow
    Write-Host "    [1] start          (local mode, with frontend + Weaviate)" -ForegroundColor Gray
    Write-Host "    [2] start-docker   (docker mode)" -ForegroundColor Gray
    Write-Host "    [3] start-backend  (local, -SkipFrontend)" -ForegroundColor Gray
    Write-Host "    [4] stop           (local mode)" -ForegroundColor Gray
    Write-Host "    [5] stop-keep-infra (local, -SkipInfra)" -ForegroundColor Gray
    Write-Host "    [6] restart-orch" -ForegroundColor Gray
    Write-Host "    [7] kill-ports     (8004, 8001, 3000)" -ForegroundColor Gray
    Write-Host "    [q] quit" -ForegroundColor Gray
    Write-Host ""
    $choice = Read-Host "  Choice"
    switch ($choice.Trim().ToLower()) {
        "1"            { $script:Action = "start" }
        "start"        { $script:Action = "start" }
        "2"            { $script:Action = "start"; $script:Mode = "docker" }
        "start-docker" { $script:Action = "start"; $script:Mode = "docker" }
        "3"            { $script:Action = "start"; $script:SkipFrontend = $true }
        "start-backend" { $script:Action = "start"; $script:SkipFrontend = $true }
        "4"            { $script:Action = "stop" }
        "stop"         { $script:Action = "stop" }
        "5"            { $script:Action = "stop"; $script:SkipInfra = $true }
        "stop-keep-infra" { $script:Action = "stop"; $script:SkipInfra = $true }
        "6"            { $script:Action = "restart-orch" }
        "restart-orch" { $script:Action = "restart-orch" }
        "7"            { $script:Action = "kill-ports" }
        "kill-ports"   { $script:Action = "kill-ports" }
        "q"            { Write-Host "  Cancelled." -ForegroundColor DarkGray; return $false }
        "quit"         { Write-Host "  Cancelled." -ForegroundColor DarkGray; return $false }
        ""             { Write-Host "  No choice entered. Cancelled." -ForegroundColor DarkGray; return $false }
        default        { Write-Host "  Unknown choice '$choice'." -ForegroundColor Red; return $false }
    }
    return $true
}

if ($Action -eq "help") {
    Show-Usage
    return
}

if (-not $Action) {
    if (-not (Read-InteractiveAction)) { return }
}

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$PipelinePorts = @(8004, 8001, 3000)

# ---------- Shared helpers ----------

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
    param([int]$Port, [switch]$Quiet)
    $conns = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
             Where-Object { $_.State -eq "Listen" }
    if (-not $conns) { return $false }

    $pids = $conns | Select-Object -ExpandProperty OwningProcess -Unique
    $killed = $false
    foreach ($p in $pids) {
        try {
            $proc = Get-Process -Id $p -ErrorAction SilentlyContinue
            if ($proc -and $proc.ProcessName -notmatch "^(System|Idle|svchost)$") {
                if (-not $Quiet) {
                    Write-Status "    Killing $($proc.ProcessName) (PID $p) on port $Port" "DarkGray"
                }
                Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
                $killed = $true
            }
        }
        catch {
            # Process may have already exited
        }
    }
    Start-Sleep -Milliseconds 500
    return $killed
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

# ---------- Action: kill-ports ----------

function Invoke-KillPorts {
    Write-Header "Port Termination Utility"

    $targetPorts = $Ports
    if ($All) {
        Write-Status "  Identifying ALL active user-space ports..." "Yellow"
        $activeConns = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
                       Where-Object {
                           $_.LocalPort -gt 1024 -and
                           ($_.LocalAddress -eq '0.0.0.0' -or $_.LocalAddress -eq '::' -or $_.LocalAddress -eq '127.0.0.1')
                       }
        $targetPorts = $activeConns.LocalPort | Select-Object -Unique
    }

    if (-not $targetPorts -or $targetPorts.Count -eq 0) {
        Write-Status "  No target ports specified or found." "DarkGray"
        return
    }

    $killedCount = 0
    $foundCount = 0
    foreach ($port in $targetPorts) {
        $before = (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue |
                   Select-Object -ExpandProperty OwningProcess -Unique).Count
        if ($before -gt 0) { $foundCount++ }
        if (Stop-PortProcess -Port $port) {
            $killedCount++
        }
    }

    Write-Host ""
    if ($killedCount -gt 0) {
        Write-Status "  Terminated process(es) across $foundCount port(s)." "Green"
    }
    else {
        Write-Status "  No active processes found on specified ports." "DarkGray"
    }
    Write-Host ""
}

# ---------- Action: restart-orch ----------

function Invoke-RestartOrch {
    Write-Header "Orchestrator Restart"

    if (Stop-PortProcess -Port 8004) {
        Write-Status "  Freed port 8004" "Green"
        Start-Sleep -Seconds 2
    }
    else {
        Write-Status "  No listener on 8004" "DarkGray"
    }

    Write-Status "  Clearing orchestrator __pycache__..." "Yellow"
    Get-ChildItem -Path (Join-Path $ProjectRoot "orchestrator/src") -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Write-Status "  [OK] Cache cleared" "Green"

    try {
        $uv = (Get-Command uv -ErrorAction Stop).Source
    }
    catch {
        Write-Status "  [X] UV not found on PATH" "Red"
        exit 1
    }
    $orchPath = (Resolve-Path (Join-Path $ProjectRoot "orchestrator")).Path

    Write-Status "  Starting orchestrator as a background job..." "Yellow"
    $j = Start-Job -ScriptBlock {
        param($uvExe, $path)
        Set-Location $path
        $env:PYTHONUNBUFFERED = "1"
        & $uvExe run python -m uvicorn src.api.main:app --reload --port 8004 --host 0.0.0.0 2>&1
    } -ArgumentList $uv, $orchPath

    Write-Status "  [OK] Started job Id: $($j.Id)" "Green"
    Write-Host ""
}

# ---------- Action: stop ----------

function Invoke-Stop {
    Write-Header "AlloyCode Compliance Engine - Shutdown"
    Write-Status "  Mode: $Mode" "Yellow"
    Write-Host ""

    if ($Mode -eq "docker") {
        Write-Status "  Stopping Docker containers..." "Yellow"
        Push-Location $ProjectRoot
        try {
            docker-compose down
            Write-Status "  [OK] All backend containers stopped" "Green"
        }
        catch {
            Write-Status "  [X] docker-compose down failed: $_" "Red"
        }
        Pop-Location

        $frontendJobs = Get-Job -ErrorAction SilentlyContinue | Where-Object { $_.State -eq "Running" }
        if ($frontendJobs) {
            Write-Status "  Stopping frontend job(s)..." "Yellow"
            $frontendJobs | Stop-Job
            $frontendJobs | Remove-Job -Force
            Write-Status "  [OK] Frontend job(s) stopped" "Green"
        }
    }
    else {
        $runningJobs = Get-Job -ErrorAction SilentlyContinue |
                       Where-Object { $_.State -eq "Running" -or $_.State -eq "NotStarted" }

        if (-not $runningJobs -or $runningJobs.Count -eq 0) {
            Write-Status "  No running jobs found." "DarkGray"
        }
        else {
            Write-Status "  Stopping $($runningJobs.Count) background job(s)..." "Yellow"
            foreach ($job in $runningJobs) {
                Write-Status "    Stopping Job $($job.Id) ($($job.Name))..." "DarkGray"
                Stop-Job -Id $job.Id -ErrorAction SilentlyContinue
            }
            Write-Status "  [OK] All jobs stopped" "Green"
        }

        $allJobs = Get-Job -ErrorAction SilentlyContinue
        if ($allJobs) {
            $allJobs | Remove-Job -Force -ErrorAction SilentlyContinue
            Write-Status "  [OK] Job history cleared" "Green"
        }

        foreach ($port in $PipelinePorts) {
            Stop-PortProcess -Port $port | Out-Null
        }

        if (-not $SkipInfra) {
            Write-Host ""
            Write-Status "  Stopping infra (Weaviate)..." "Yellow"
            try {
                docker --version | Out-Null
                Push-Location $ProjectRoot
                try {
                    docker compose stop weaviate 2>&1 | Out-Null
                    Write-Status "  [OK] Weaviate container stopped" "Green"
                }
                finally {
                    Pop-Location
                }
            }
            catch {
                Write-Status "  [!] Docker unavailable - skipping Weaviate stop" "DarkGray"
            }
        }
        else {
            Write-Status "  Skipping infra shutdown (-SkipInfra)" "DarkGray"
        }
    }

    Write-Host ""
    Write-Status "  [OK] Shutdown complete" "Green"
    Write-Host ""
}

# ---------- Action: start ----------

function Invoke-Start {
    Write-Header "AlloyCode Compliance Engine - Startup"
    Write-Status "  Mode: $Mode" "Yellow"
    Write-Status "  Root: $ProjectRoot" "DarkGray"
    Write-Host ""

    # ---- Prerequisites ----
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

    # ---- Clean up stale state ----
    Write-Host ""
    Write-Status "  Cleaning up stale processes..." "Yellow"

    $existingJobs = Get-Job -ErrorAction SilentlyContinue
    if ($existingJobs) {
        $existingJobs | Stop-Job -ErrorAction SilentlyContinue
        $existingJobs | Remove-Job -Force -ErrorAction SilentlyContinue
        Write-Status "  [OK] Cleared $($existingJobs.Count) stale background job(s)" "Green"
    }

    $killedAny = $false
    foreach ($port in $PipelinePorts) {
        if (Stop-PortProcess -Port $port) {
            $killedAny = $true
        }
    }
    if ($killedAny) {
        Write-Status "  [OK] Freed occupied ports" "Green"
        Start-Sleep -Seconds 2
    }
    else {
        Write-Status "  [OK] All ports are free" "Green"
    }

    # ---- .env checks ----
    Write-Host ""
    Write-Status "  Checking environment files..." "Yellow"

    foreach ($mod in @("knowledge_engine", "orchestrator")) {
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

    $rootEnv = Join-Path $ProjectRoot ".env"
    if ($Mode -eq "docker" -and -not (Test-Path $rootEnv)) {
        Write-Status "  [!] Root .env not found (needed by docker-compose)" "Yellow"
    }

    # ---- Docker mode ----
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

        Write-Host ""
        Wait-ForService -Name "Knowledge Engine" -Port 8001
        Wait-ForService -Name "Orchestrator" -Port 8004

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

    # ---- Local mode ----
    if ($Mode -eq "local") {
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

        Start-Sleep -Seconds 5

        Write-Host ""
        foreach ($j in $jobs) {
            $jobObj = Get-Job -Id $j.Job.Id -ErrorAction SilentlyContinue
            if ($jobObj.State -eq "Failed") {
                Write-Status "  [X] $($j.Name) failed to start!" "Red"
                $output = Receive-Job -Id $j.Job.Id -ErrorAction SilentlyContinue 2>&1
                foreach ($line in $output) {
                    Write-Status "    $line" "Red"
                }
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

        if (-not $SkipFrontend) {
            Write-Host ""
            Write-Header "Starting Frontend (Next.js)"

            $frontendPath = Join-Path $ProjectRoot "frontend"
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

    # ---- Summary ----
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
        Write-Status "    AlloyCode Dashboard         -> http://localhost:3000" "Cyan"
    }

    Write-Host ""
    Write-Status "  Commands:" "Yellow"
    if ($Mode -eq "local") {
        Write-Status "    View logs   -> Receive-Job -Id <id> -Keep" "DarkGray"
        Write-Status "    List jobs   -> Get-Job" "DarkGray"
        Write-Status "    Stop all    -> .\pipeline.ps1 -Action stop" "DarkGray"
    }
    else {
        Write-Status "    View logs   -> docker-compose logs -f" "DarkGray"
        Write-Status "    Status      -> docker-compose ps" "DarkGray"
        Write-Status "    Stop all    -> .\pipeline.ps1 -Action stop -Mode docker" "DarkGray"
    }

    Write-Host ""
    Write-Status "  [OK] All systems online" "Green"
    Write-Host ""
}

# ---------- Dispatch ----------

switch ($Action) {
    "start"        { Invoke-Start }
    "stop"         { Invoke-Stop }
    "restart-orch" { Invoke-RestartOrch }
    "kill-ports"   { Invoke-KillPorts }
}
