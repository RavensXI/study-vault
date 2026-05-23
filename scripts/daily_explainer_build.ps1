# Daily explainer-video build runner. Registered with Windows Task Scheduler.
# Fires once a day at 08:00. Launches up to 180 new generations, then polls
# status/downloads in a loop until everything in flight has shipped.

$ErrorActionPreference = "Continue"
$repo = "C:\Users\tshau\Documents\Study Vault"
Set-Location $repo

$logDir = Join-Path $repo "scripts\_explainer_daily_logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}
$logFile = Join-Path $logDir ("{0}.log" -f (Get-Date -Format "yyyy-MM-dd"))

function Write-Log {
    param([string]$Message)
    $line = "{0} {1}" -f (Get-Date -Format "HH:mm:ss"), $Message
    Add-Content -Path $logFile -Value $line -Encoding utf8
}

function Run-Py {
    param([string[]]$PyArgs)
    Write-Log ("RUN python " + ($PyArgs -join ' '))
    $output = & python @PyArgs 2>&1
    foreach ($line in $output) {
        Add-Content -Path $logFile -Value ("    " + $line) -Encoding utf8
    }
    return $output
}

Write-Log "=== Daily explainer build START ==="

# Bail early if queue is empty so we don't burn API time
$dry = Run-Py -PyArgs @("scripts\batch_explainer_videos.py", "--daily-cap", "180", "--dry-run")
if ($dry -match "No lessons pending") {
    Write-Log "Queue empty. Done."
    Write-Log "=== END ==="
    exit 0
}

# Phase 1: launch up to 180 new generations
Write-Log "Phase 1: launching..."
Run-Py -PyArgs @("scripts\batch_explainer_videos.py", "--daily-cap", "180") | Out-Null

# Phase 2: poll up to 4 hours, downloading completed jobs as they come in.
# Smoke test showed ~20 min cook time for 10 lessons; 180 should land well under 1h.
# 4h ceiling protects against runaway state if NLM stalls.
$maxLoops = 24
$pollIntervalSec = 600  # 10 min

for ($i = 1; $i -le $maxLoops; $i++) {
    Start-Sleep -Seconds $pollIntervalSec

    Write-Log ("Phase 2 loop {0}/{1}: status check" -f $i, $maxLoops)
    $status = Run-Py -PyArgs @("scripts\batch_explainer_videos.py", "--status")

    # Exit when nothing is still cooking. Two phrasings:
    #   "No in-progress jobs"   → state has zero active jobs at all
    #   "0 still in progress"   → everything that was active is now either
    #                              completed or marked failed (terminal)
    if (($status -match "No in-progress jobs") -or ($status -match "0 still in progress")) {
        Write-Log "Nothing still cooking. Final download pass."
        Run-Py -PyArgs @("scripts\batch_explainer_videos.py", "--download", "--cleanup") | Out-Null
        break
    }

    # Download any completed so far
    Run-Py -PyArgs @("scripts\batch_explainer_videos.py", "--download", "--cleanup") | Out-Null
}

Write-Log "=== Daily explainer build END ==="
