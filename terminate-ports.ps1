#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Quickly terminates processes listening on specific network ports.

.DESCRIPTION
    A utility script to find and kill processes bound to local TCP/UDP ports.
    Defaults to ports used by AlloyCode (8004, 8001, 3000).

.PARAMETER Ports
    An array of port numbers to terminate.
    Example: .\terminate-ports.ps1 -Ports 8080, 5000

.PARAMETER All
    If switch is present, finds and terminates ALL active local TCP listeners 
    above port 1024 (user-space). Use with caution.

.EXAMPLE
    .\terminate-ports.ps1
    Clears ports 8004, 8001, and 3000.

.EXAMPLE
    .\terminate-ports.ps1 -Ports 9000
    Kills any process listening on port 9000.
#>

param(
    [int[]]$Ports = @(8004, 8001, 3000),
    [switch]$All
)

$ErrorActionPreference = "Stop"

function Write-Status {
    param([string]$Message, [string]$Color = "White")
    Write-Host "  $Message" -ForegroundColor $Color
}

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "  " + ("=" * 40) -ForegroundColor Cyan
    Write-Host "    $Text" -ForegroundColor Cyan
    Write-Host "  " + ("=" * 40) -ForegroundColor Cyan
    Write-Host ""
}

Write-Header "Port Termination Utility"

if ($All) {
    Write-Status "Identifying ALL active user-space ports..." "Yellow"
    $activeConns = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | 
                   Where-Object { $_.LocalPort -gt 1024 -and $_.LocalAddress -eq '0.0.0.0' -or $_.LocalAddress -eq '::' -or $_.LocalAddress -eq '127.0.0.1' }
    $Ports = $activeConns.LocalPort | Select-Object -Unique
}

if ($Ports.Count -eq 0) {
    Write-Status "No target ports specified or found." "DarkGray"
    exit 0
}

$foundCount = 0
$killedCount = 0

foreach ($port in $Ports) {
    # Get unique process IDs listening on this port
    $pids = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | 
            Select-Object -ExpandProperty OwningProcess -Unique

    if ($pids) {
        $foundCount++
        foreach ($p in $pids) {
            try {
                $proc = Get-Process -Id $p -ErrorAction SilentlyContinue
                if ($proc) {
                    $procName = $proc.ProcessName
                    if ($procName -cmatch "System|Idle|svchost") {
                        Write-Status "Skipping system process $procName on port $port" "Yellow"
                        continue
                    }
                    
                    Write-Status "Terminating $procName (PID $p) on port $port..." "Red"
                    Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
                    $killedCount++
                }
            }
            catch {
                # Process might have closed on its own
            }
        }
    }
}

Write-Host ""
if ($killedCount -gt 0) {
    Write-Status "Success! Terminated $killedCount process(es) across $foundCount port(s)." "Green"
}
else {
    Write-Status "No active processes found on specified ports." "DarkGray"
}
Write-Host ""
