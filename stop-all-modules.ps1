#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Stops the full AlloyCode Compliance Engine pipeline (backend + frontend)

.DESCRIPTION
    Gracefully shuts down all running services:
    - Docker mode: runs docker-compose down from the project root (stops
      orchestrator, knowledge engine, Weaviate, postgres, redis).
    - Local mode: stops all PowerShell background jobs (UV + npm) AND the
      Weaviate container that was started by start-all-modules.ps1. Pass
      -SkipInfra to leave Weaviate running for a subsequent start.

.PARAMETER Mode
    Shutdown mode: "docker" or "local"
    Default: local

.PARAMETER SkipInfra
    Local mode only: do NOT stop the Weaviate container. Useful when you
    plan to restart the backend without a cold vector-store boot.
    Default: false

.EXAMPLE
    .\stop-all-modules.ps1
    .\stop-all-modules.ps1 -Mode docker
    .\stop-all-modules.ps1 -Mode local -SkipInfra
#>

param(
    [ValidateSet("docker", "local")]
    [string]$Mode = "local",

    [switch]$SkipInfra
)

$ErrorActionPreference = "Stop"

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

$ProjectRoot = $PSScriptRoot

Write-Header "AlloyCode Compliance Engine - Shutdown"
Write-Status "  Mode: $Mode" "Yellow"
Write-Host ""

if ($Mode -eq "docker") {
    # Stop all containers from root docker-compose
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

    # Stop frontend job if running
    $frontendJobs = Get-Job -ErrorAction SilentlyContinue | Where-Object { $_.State -eq "Running" }
    if ($frontendJobs) {
        Write-Status "  Stopping frontend job(s)..." "Yellow"
        $frontendJobs | Stop-Job
        $frontendJobs | Remove-Job -Force
        Write-Status "  [OK] Frontend job(s) stopped" "Green"
    }
}
elseif ($Mode -eq "local") {
    $runningJobs = Get-Job -ErrorAction SilentlyContinue | Where-Object { $_.State -eq "Running" -or $_.State -eq "NotStarted" }

    if ($runningJobs.Count -eq 0) {
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

    # Clean up all jobs (running + completed)
    $allJobs = Get-Job -ErrorAction SilentlyContinue
    if ($allJobs) {
        $allJobs | Remove-Job -Force -ErrorAction SilentlyContinue
        Write-Status "  [OK] Job history cleared" "Green"
    }

    # Kill any lingering processes on the known ports
    $ports = @(8004, 8001, 3000)
    foreach ($port in $ports) {
        $procs = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue |
                 Where-Object { $_.State -eq "Listen" } |
                 Select-Object -ExpandProperty OwningProcess -Unique

        foreach ($p in $procs) {
            try {
                $proc = Get-Process -Id $p -ErrorAction SilentlyContinue
                if ($proc -and $proc.ProcessName -ne "System") {
                    Write-Status "    Killing $($proc.ProcessName) (PID $p) on port $port" "DarkGray"
                    Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
                }
            }
            catch {
                # Process may have already exited
            }
        }
    }

    # Stop the Weaviate container that start-all-modules.ps1 brought up.
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
