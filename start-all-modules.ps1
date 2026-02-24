#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Starts all three core modules of the EU AI Regulatory Compliance Engine

.DESCRIPTION
    This script orchestrates the startup of all three core modules:
    - core_1: AI Model Governance & Compliance Monitoring (Port 8002)
    - core_2: GraphRAG Legal Research Engine (Port 8001)
    - core_3: EU AI Act Compliance Automation Agent (Port 8000)

.PARAMETER Mode
    Startup mode: "docker" (uses docker-compose) or "local" (uses UV)
    Default: docker

.PARAMETER Detached
    Run containers in detached mode (background)
    Default: true

.EXAMPLE
    .\start-all-modules.ps1
    .\start-all-modules.ps1 -Mode local
    .\start-all-modules.ps1 -Detached $false
#>

param(
    [ValidateSet("docker", "local")]
    [string]$Mode = "docker",
    
    [bool]$Detached = $true
)

$ErrorActionPreference = "Stop"

# Colors for output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Header {
    param([string]$Text)
    Write-ColorOutput "`n========================================" "Cyan"
    Write-ColorOutput $Text "Cyan"
    Write-ColorOutput "========================================`n" "Cyan"
}

# Project root directory
$ProjectRoot = $PSScriptRoot

Write-Header "EU AI Regulatory Compliance Engine - Startup Script"

# Check prerequisites
if ($Mode -eq "docker") {
    Write-ColorOutput "Checking Docker..." "Yellow"
    try {
        docker --version | Out-Null
        docker-compose --version | Out-Null
        Write-ColorOutput "✓ Docker is installed" "Green"
    }
    catch {
        Write-ColorOutput "✗ Docker is not installed or not running" "Red"
        Write-ColorOutput "Please install Docker Desktop: https://www.docker.com/products/docker-desktop" "Yellow"
        exit 1
    }
}
elseif ($Mode -eq "local") {
    Write-ColorOutput "Checking UV..." "Yellow"
    try {
        uv --version | Out-Null
        Write-ColorOutput "✓ UV is installed" "Green"
    }
    catch {
        Write-ColorOutput "✗ UV is not installed" "Red"
        Write-ColorOutput "Install UV: https://docs.astral.sh/uv/" "Yellow"
        exit 1
    }
}

# Module definitions
$modules = @(
    @{
        Name = "core_1"
        Description = "AI Model Governance & Compliance Monitoring"
        Port = 8002
        Path = Join-Path $ProjectRoot "core_1"
        Color = "Magenta"
    },
    @{
        Name = "core_2"
        Description = "GraphRAG Legal Research Engine"
        Port = 8001
        Path = Join-Path $ProjectRoot "core_2_knowledge_base"
        Color = "Blue"
    },
    @{
        Name = "core_3"
        Description = "EU AI Act Compliance Automation Agent"
        Port = 8000
        Path = Join-Path $ProjectRoot "core_3"
        Color = "Green"
    }
)

# Check if .env files exist
Write-Header "Checking Environment Files"
foreach ($module in $modules) {
    $envFile = Join-Path $module.Path ".env"
    $envExample = Join-Path $module.Path ".env.example"
    
    if (-not (Test-Path $envFile)) {
        if (Test-Path $envExample) {
            Write-ColorOutput "⚠ .env not found for $($module.Name), copying from .env.example" "Yellow"
            Copy-Item $envExample $envFile
        }
        else {
            Write-ColorOutput "⚠ No .env or .env.example found for $($module.Name)" "Yellow"
        }
    }
    else {
        Write-ColorOutput "✓ .env file exists for $($module.Name)" "Green"
    }
}

# Start modules
if ($Mode -eq "docker") {
    Write-Header "Starting Modules with Docker Compose"
    
    $detachedFlag = if ($Detached) { "-d" } else { "" }
    
    foreach ($module in $modules) {
        Write-ColorOutput "`nStarting $($module.Name): $($module.Description)" $module.Color
        Write-ColorOutput "Path: $($module.Path)" "Gray"
        Write-ColorOutput "Port: $($module.Port)" "Gray"
        
        Push-Location $module.Path
        try {
            if ($Detached) {
                docker-compose up -d
            }
            else {
                # Start in background with Start-Process for non-detached mode
                Start-Process -FilePath "docker-compose" -ArgumentList "up" -NoNewWindow
            }
            Write-ColorOutput "✓ $($module.Name) started successfully" "Green"
        }
        catch {
            Write-ColorOutput "✗ Failed to start $($module.Name): $_" "Red"
        }
        finally {
            Pop-Location
        }
        
        Start-Sleep -Seconds 2
    }
    
    Write-Header "Deployment Summary"
    Write-ColorOutput "All modules are starting up..." "Green"
    Write-ColorOutput "`nModule Endpoints:" "Cyan"
    foreach ($module in $modules) {
        Write-ColorOutput "  • $($module.Description): http://localhost:$($module.Port)" $module.Color
    }
    
    Write-ColorOutput "`nUseful Commands:" "Yellow"
    Write-ColorOutput "  • View logs: docker-compose logs -f [service-name]" "Gray"
    Write-ColorOutput "  • Stop all: .\stop-all-modules.ps1" "Gray"
    Write-ColorOutput "  • Check status: docker-compose ps" "Gray"
    
    Write-ColorOutput "`nNote: Services may take 30-60 seconds to be fully ready" "Yellow"
}
elseif ($Mode -eq "local") {
    Write-Header "Starting Modules with UV (Local Development)"
    
    $jobs = @()
    
    foreach ($module in $modules) {
        Write-ColorOutput "`nStarting $($module.Name): $($module.Description)" $module.Color
        Write-ColorOutput "Path: $($module.Path)" "Gray"
        Write-ColorOutput "Port: $($module.Port)" "Gray"
        
        # Determine the main module to run
        $mainModule = switch ($module.Name) {
            "core_1" { "src.api.main:app" }
            "core_2" { "src.api.main:app" }
            "core_3" { "src.api.main:app" }
        }
        
        # Start the server in a new PowerShell window
        $scriptBlock = {
            param($path, $mainModule, $port, $name)
            Set-Location $path
            $env:PYTHONUNBUFFERED = "1"
            Write-Host "Starting $name on port $port..." -ForegroundColor Yellow
            uv run uvicorn $mainModule --reload --port $port
        }
        
        $job = Start-Job -ScriptBlock $scriptBlock -ArgumentList $module.Path, $mainModule, $module.Port, $module.Name
        $jobs += @{
            Name = $module.Name
            Job = $job
            Port = $module.Port
        }
        
        Write-ColorOutput "✓ $($module.Name) job started (Job ID: $($job.Id))" "Green"
        Start-Sleep -Seconds 1
    }
    
    Write-Header "Deployment Summary"
    Write-ColorOutput "All modules are running as background jobs" "Green"
    Write-ColorOutput "`nModule Endpoints:" "Cyan"
    foreach ($module in $modules) {
        Write-ColorOutput "  • $($module.Description): http://localhost:$($module.Port)" $module.Color
    }
    
    Write-ColorOutput "`nBackground Jobs:" "Yellow"
    foreach ($jobInfo in $jobs) {
        Write-ColorOutput "  • $($jobInfo.Name) (Job ID: $($jobInfo.Job.Id))" "Gray"
    }
    
    Write-ColorOutput "`nUseful Commands:" "Yellow"
    Write-ColorOutput "  • View job output: Receive-Job -Id <job-id> -Keep" "Gray"
    Write-ColorOutput "  • Stop all jobs: Get-Job | Stop-Job; Get-Job | Remove-Job" "Gray"
    Write-ColorOutput "  • Check job status: Get-Job" "Gray"
}

Write-ColorOutput "`n✓ Startup complete!" "Green"
Write-ColorOutput "Press Ctrl+C to stop monitoring`n" "Yellow"
