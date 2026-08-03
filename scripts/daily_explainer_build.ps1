# Explainer-video build runner. Registered with Windows Task Scheduler.
# Fires hourly. Self-gates via rolling-quota cooldown: only launches a fresh
# batch when at least 24h05m has elapsed since the last launch (NLM quota is
# rolling 24h, so anchoring on launch START + 5min buffer ensures the slots
# we burned yesterday have refilled). A lock file prevents two wrappers from
# running concurrently (state file is not race-safe).

$ErrorActionPreference = "Continue"
$repo = "C:\Users\tshau\Documents\Study Vault"
Set-Location $repo

$logDir = Join-Path $repo "scripts\_explainer_daily_logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}
$logFile = Join-Path $logDir ("{0}.log" -f (Get-Date -Format "yyyy-MM-dd"))
$lockFile = Join-Path $logDir "_running.lock"
$lastLaunchFile = Join-Path $logDir "_last_launch.txt"
$cooldownHours = 23.9167  # 23h55m - catches the SAME hourly slot daily (24h05m drifted +1h/day; shorts wrapper learned this first)
$lockStaleHours = 12       # treat lock as orphaned past this (run probably crashed)

function Write-Log {
    param([string]$Message)
    $line = "{0} {1}" -f (Get-Date -Format "HH:mm:ss"), $Message
    Add-Content -Path $logFile -Value $line -Encoding utf8
}

function Run-Py {
    # Bounded python call. The unguarded `& python` inline-call would hang forever if
    # python blocked on Chrome auth or a network call (burned us 11-12 Jun + 12-13 Jun:
    # wrapper sat on a dead child for 13h until the stale-lock gate cleared).
    # Start-Process gives us a process handle we can WaitForExit with a timeout on,
    # and we drain its captured stdout/stderr into the log either way.
    param(
        [string[]]$PyArgs,
        [int]$TimeoutMin = 90
    )
    Write-Log ("RUN python " + ($PyArgs -join ' ') + (" (timeout {0}m)" -f $TimeoutMin))

    $tmpOut = [System.IO.Path]::GetTempFileName()
    $tmpErr = [System.IO.Path]::GetTempFileName()

    try {
        $proc = Start-Process -FilePath "python" -ArgumentList $PyArgs `
            -RedirectStandardOutput $tmpOut -RedirectStandardError $tmpErr `
            -NoNewWindow -PassThru

        $timeoutMs = $TimeoutMin * 60 * 1000
        $exited = $proc.WaitForExit($timeoutMs)

        if (-not $exited) {
            Write-Log ("TIMEOUT after {0}m - killing python PID {1}" -f $TimeoutMin, $proc.Id)
            try { $proc.Kill() } catch { Write-Log ("Kill failed: " + $_.Exception.Message) }
            # Brief grace so kill flushes child handles
            Start-Sleep -Seconds 3
        } else {
            Write-Log ("python exited with code {0}" -f $proc.ExitCode)
        }

        $stdout = if (Test-Path $tmpOut) { Get-Content $tmpOut } else { @() }
        $stderr = if (Test-Path $tmpErr) { Get-Content $tmpErr } else { @() }
        $output = @($stdout) + @($stderr)

        foreach ($line in $output) {
            Add-Content -Path $logFile -Value ("    " + $line) -Encoding utf8
        }
        return $output
    } finally {
        Remove-Item -Path $tmpOut, $tmpErr -Force -ErrorAction SilentlyContinue
    }
}

Write-Log "=== Hourly heartbeat ==="

# Gate 1: another wrapper still in flight?
if (Test-Path $lockFile) {
    $lockAge = (Get-Date) - (Get-Item $lockFile).LastWriteTime
    if ($lockAge.TotalHours -lt $lockStaleHours) {
        Write-Log ("Lock present (age {0:F1}h). Previous run still active - skipping." -f $lockAge.TotalHours)
        exit 0
    }
    Write-Log ("Lock is stale (age {0:F1}h > {1}h). Removing." -f $lockAge.TotalHours, $lockStaleHours)
    Remove-Item $lockFile -Force -ErrorAction SilentlyContinue
}

# Gate 2: cooldown window from last launch
if (Test-Path $lastLaunchFile) {
    $lastLaunch = [DateTime]::Parse((Get-Content $lastLaunchFile -Raw).Trim())
    $elapsed = (Get-Date) - $lastLaunch
    if ($elapsed.TotalHours -lt $cooldownHours) {
        $remaining = $cooldownHours - $elapsed.TotalHours
        Write-Log ("Cooldown active. Last launch {0:F1}h ago; need {1:F1}h. {2:F1}h remaining - skipping." -f $elapsed.TotalHours, $cooldownHours, $remaining)
        exit 0
    }
    Write-Log ("Cooldown clear. Last launch {0:F1}h ago." -f $elapsed.TotalHours)
} else {
    Write-Log "No prior launch recorded - first run."
}

Write-Log "=== Daily explainer build START ==="

# Bail early if queue is empty so we don't burn API time
$dry = Run-Py -PyArgs @("scripts\batch_explainer_videos.py", "--daily-cap", "35", "--dry-run") -TimeoutMin 10
if ($dry -match "No lessons pending") {
    Write-Log "Queue empty. Done."
    Write-Log "=== END ==="
    exit 0
}

# Acquire lock + stamp launch time before kicking off Phase 1
New-Item -ItemType File -Path $lockFile -Force | Out-Null
(Get-Date).ToString("o") | Out-File -FilePath $lastLaunchFile -Encoding utf8 -NoNewline
Write-Log ("Lock acquired. Launch timestamp written: {0}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))

try {

# Phase 1: launch up to 180 new generations
Write-Log "Phase 1: launching..."
Run-Py -PyArgs @("scripts\batch_explainer_videos.py", "--daily-cap", "35") | Out-Null

# Phase 2: poll up to 4 hours, downloading completed jobs as they come in.
# Smoke test showed ~20 min cook time for 10 lessons; 180 should land well under 1h.
# 4h ceiling protects against runaway state if NLM stalls.
$maxLoops = 24
$pollIntervalSec = 600  # 10 min

for ($i = 1; $i -le $maxLoops; $i++) {
    Start-Sleep -Seconds $pollIntervalSec

    Write-Log ("Phase 2 loop {0}/{1}: status check" -f $i, $maxLoops)
    $status = Run-Py -PyArgs @("scripts\batch_explainer_videos.py", "--status") -TimeoutMin 10

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

} finally {
    Remove-Item $lockFile -Force -ErrorAction SilentlyContinue
    Write-Log "Lock released."
}
