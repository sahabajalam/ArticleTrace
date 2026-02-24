#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Stops all three core modules of the EU AI Regulatory Compliance Engine

.DESCRIPTION
    This script stops all running services across the three core modules

.PARAMETER Mode
    Shutdown mode: "docker" or "local"
    Default: docker

.EXAMPLE
    .\stop-all-modules.ps1
    .\stop-all-modules.ps1 -Mode local
#>

param(
    [ValidateSet("docker", "local")]
    [string]$Mode = "docker"
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

$ProjectRoot = $PSScriptRoot

Write-Header "Stopping All Modules"

$modules = @(
    @{ Name = "core_1"; Path = Join-Path $ProjectRoot "core_1" },
    @{ Name = "core_2"; Path = Join-Path $ProjectRoot "core_2_knowledge_base" },
    @{ Name = "core_3"; Path = Join-Path $ProjectRoot "core_3" }
)

if ($Mode -eq "docker") {
    foreach ($module in $modules) {
        Write-ColorOutput "Stopping $($module.Name)..." "Yellow"
        Push-Location $module.Path
        try {
            docker-compose down
            Write-ColorOutput "✓ $($module.Name) stopped" "Green"
        }
        catch {
            Write-ColorOutput "✗ Error stopping $($module.Name): $_" "Red"
        }
        finally {
            Pop-Location
        }
    }
}
elseif ($Mode -eq "local") {
    Write-ColorOutput "Stopping all UV background jobs..." "Yellow"
    Get-Job | Stop-Job
    Get-Job | Remove-Job
    Write-ColorOutput "✓ All background jobs stopped" "Green"
}

Write-ColorOutput "`n✓ All modules stopped successfully`n" "Green"
