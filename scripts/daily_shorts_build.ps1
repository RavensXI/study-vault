# Shorts build runner. Registered with Windows Task Scheduler ("StudyVaultShorts").
# Mirrors daily_explainer_build.ps1: fires HOURLY, self-gates via rolling-quota
# cooldown — only launches a fresh batch when 24h05m has elapsed since the last
# launch START (NLM quota is a rolling 24h window; the shorts batch's own daily
# cap is calendar-stamped, so this cooldown is what stops a midnight double-dip).
# A lock file prevents two wrappers overlapping; the batch also has its own
# single-instance lock as a second belt. Auth self-heals inside the batch
# (nlm login via saved Chrome profile) as of 11 Jul 2026.

$ErrorActionPreference = "Continue"
$repo = "C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox"
Set-Location $repo

$logDir = Join-Path $repo "scripts\_shorts_daily_logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}
$logFile = Join-Path $logDir ("{0}.log" -f (Get-Date -Format "yyyy-MM-dd"))
$lockFile = Join-Path $logDir "_running.lock"
$lastLaunchFile = Join-Path $logDir "_last_launch.txt"
$cooldownHours = 24.0833  # 24h05m — rolling quota window + safety buffer
$lockStaleHours = 12      # treat lock as orphaned past this (run probably crashed)
$python = "C:\Users\tshau\AppData\Local\Programs\Python\Python312\python.exe"

function Write-Log {
    param([string]$Message)
    $line = "{0} {1}" -f (Get-Date -Format "HH:mm:ss"), $Message
    Add-Content -Path $logFile -Value $line -Encoding utf8
}

function Run-Py {
    # Bounded python call (same rationale as the explainer wrapper: an unguarded
    # call can hang forever on a dead Chrome/network and wedge the wrapper).
    param(
        [string[]]$PyArgs,
        [int]$TimeoutMin = 90
    )
    Write-Log ("RUN python " + ($PyArgs -join ' ') + (" (timeout {0}m)" -f $TimeoutMin))

    $tmpOut = [System.IO.Path]::GetTempFileName()
    $tmpErr = [System.IO.Path]::GetTempFileName()
    try {
        $proc = Start-Process -FilePath $python -ArgumentList (@("-u") + $PyArgs) `
            -RedirectStandardOutput $tmpOut -RedirectStandardError $tmpErr `
            -NoNewWindow -PassThru

        $timeoutMs = $TimeoutMin * 60 * 1000
        $exited = $proc.WaitForExit($timeoutMs)

        if (-not $exited) {
            Write-Log ("TIMEOUT after {0}m - killing python PID {1}" -f $TimeoutMin, $proc.Id)
            try { $proc.Kill() } catch { Write-Log ("Kill failed: " + $_.Exception.Message) }
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

Write-Log "=== Hourly heartbeat (shorts) ==="

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

Write-Log "=== Daily shorts build START ==="

# Bail early if the queue is empty (nothing left to short), or if the batch's
# own single-instance lock is held (e.g. a manual run in flight) — in that case
# skip WITHOUT stamping the launch, so the next hourly fire tries again.
$dry = Run-Py -PyArgs @("scripts\batch_short_videos.py", "--dry-run", "--limit", "1") -TimeoutMin 15
if ($dry -match "Another run is active") {
    Write-Log "Batch already running elsewhere - skipping (no launch stamped)."
    Write-Log "=== END ==="
    exit 0
}
if ($dry -match "^0 lessons queued") {
    Write-Log "Queue empty. Done."
    Write-Log "=== END ==="
    exit 0
}

# Acquire lock + stamp launch time, then run the whole day's batch in one go.
# The batch itself sweeps orphans, self-heals auth, respects the daily cap,
# and downloads/uploads each short inline — one bounded call does everything.
New-Item -ItemType File -Path $lockFile -Force | Out-Null
(Get-Date).ToString("o") | Out-File -FilePath $lastLaunchFile -Encoding utf8 -NoNewline
Write-Log ("Lock acquired. Launch timestamp written: {0}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))

try {
    Run-Py -PyArgs @("scripts\batch_short_videos.py", "--daily-cap", "100") -TimeoutMin 300 | Out-Null
    Write-Log "=== Daily shorts build END ==="
} finally {
    Remove-Item $lockFile -Force -ErrorAction SilentlyContinue
    Write-Log "Lock released."
}
