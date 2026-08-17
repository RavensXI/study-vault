# Podcast build runner. Registered with Windows Task Scheduler
# ("StudyVault - Daily Podcast Build"). Fires hourly; self-gates via the
# same rolling-quota cooldown as the explainer wrapper. Seeded to launch
# ~06:00 daily - clear of shorts (01:00-05:00, sandbox worktree) and
# explainers (14:00-18:00): nlm auth flows contest Chrome, and the podcast
# state file is a whole-file overwrite, so exactly ONE podcast batch may
# run at a time. This wrapper is now the only sanctioned launcher; manual
# batch_podcasts.py runs must first check for this wrapper's lock.
#
# Selection: --live-only --unit-complete --all-subjects. Podcasts generate
# only for lessons students can see, only once EVERY lesson in the unit is
# live (the prompt frames the lesson inside the finished unit - "3rd of 7",
# sibling titles, "still to come"), and new boards are picked up newest-
# first the morning after Tom flips the last lesson in a unit.

$ErrorActionPreference = "Continue"
$repo = "C:\Users\tshau\Documents\Study Vault"
Set-Location $repo

$logDir = Join-Path $repo "scripts\_podcast_daily_logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}
$logFile = Join-Path $logDir ("{0}.log" -f (Get-Date -Format "yyyy-MM-dd"))
$lockFile = Join-Path $logDir "_running.lock"
$lastLaunchFile = Join-Path $logDir "_last_launch.txt"
$cooldownHours = 23.9167  # 23h55m - catches the SAME hourly slot daily (24h05m drifted +1h/day)
$lockStaleHours = 7.5      # the task's ExecutionTimeLimit is PT7H, so no instance
                           # can live longer - an older lock is definitionally orphaned
$dailyCap = 60             # NLM audio quota is ~200/day; 60 keeps the run inside the morning window

function Write-Log {
    param([string]$Message)
    $line = "{0} {1}" -f (Get-Date -Format "HH:mm:ss"), $Message
    Add-Content -Path $logFile -Value $line -Encoding utf8
}

function Run-Py {
    # Bounded python call (same rationale as the explainer wrapper: an
    # unguarded call can hang forever on a dead Chrome/network and wedge
    # the wrapper until the stale-lock gate clears).
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

Write-Log "=== Hourly heartbeat (podcasts) ==="

# Health probe: if the last launch was 1-4h ago, verify audio is actually
# cooking in the notebooks (catches silent no-op launches; alerts via
# Resend, max once per day per stream).
if (Test-Path $lastLaunchFile) {
    $sinceLaunch = (Get-Date) - [DateTime]::Parse((Get-Content $lastLaunchFile -Raw).Trim())
    if ($sinceLaunch.TotalHours -ge 1 -and $sinceLaunch.TotalHours -le 4) {
        Write-Log "Running NLM health probe (podcast stream)..."
        Run-Py -PyArgs @("scripts\nlm_health_probe.py", "--stream", "podcast") -TimeoutMin 8 | Out-Null
    }
}

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

Write-Log "=== Daily podcast build START ==="

# Backlog before, for the verified recount at the end. (The sweep counts
# ALL live lessons missing podcasts; the batch additionally gates on
# unit-complete, so "still pending" may legitimately stay above zero.)
$backlog = -1
$sweepOut = Run-Py -PyArgs @("scripts\_podcast_sweep.py", "--total") -TimeoutMin 10
foreach ($ln in $sweepOut) { if ($ln -match '^\s*(\d+)\s*$') { $backlog = [int]$Matches[1]; break } }
Write-Log ("Sweep backlog before: {0} live lessons missing podcasts." -f $backlog)

# Bail early if the queue is empty so we don't burn launch time
$dry = Run-Py -PyArgs @("scripts\batch_podcasts.py", "--limit", "$dailyCap", "--live-only", "--unit-complete", "--all-subjects", "--dry-run") -TimeoutMin 15
if ($dry -match "No lessons pending") {
    Write-Log "Queue empty (after unit-complete gate). Done."
    Write-Log "=== END ==="
    exit 0
}

# Acquire lock + stamp launch time before kicking off Phase 1
New-Item -ItemType File -Path $lockFile -Force | Out-Null
(Get-Date).ToString("o") | Out-File -FilePath $lastLaunchFile -Encoding utf8 -NoNewline
Write-Log ("Lock acquired. Launch timestamp written: {0}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))

try {

# Phase 1: launch up to $dailyCap generations (~1.5-2 min each)
Write-Log "Phase 1: launching..."
Run-Py -PyArgs @("scripts\batch_podcasts.py", "--limit", "$dailyCap", "--live-only", "--unit-complete", "--all-subjects") -TimeoutMin 180 | Out-Null

# Phase 2: poll up to 3 hours, downloading completed jobs as they come in.
$maxLoops = 18
$pollIntervalSec = 600  # 10 min

for ($i = 1; $i -le $maxLoops; $i++) {
    Start-Sleep -Seconds $pollIntervalSec

    Write-Log ("Phase 2 loop {0}/{1}: status check" -f $i, $maxLoops)
    $status = Run-Py -PyArgs @("scripts\batch_podcasts.py", "--status") -TimeoutMin 15

    # Exit when nothing is still cooking. (?<!\d) guards the zero:
    # a bare "0 still in progress" match is a SUBSTRING and also matches
    # "10 still in progress" / "60 still in progress".
    if (($status -match "No in-progress jobs") -or ($status -match "(?<!\d)0 still in progress")) {
        Write-Log "Nothing still cooking. Final download pass."
        Run-Py -PyArgs @("scripts\batch_podcasts.py", "--download", "--cleanup") -TimeoutMin 150 | Out-Null
        break
    }

    # Download any completed so far (20s inter-file pacing inside the batch)
    Run-Py -PyArgs @("scripts\batch_podcasts.py", "--download", "--cleanup") -TimeoutMin 150 | Out-Null
}

# Verified count = backlog shrinkage re-measured from Supabase (catches
# the old "--download didn't write Supabase" failure by construction)
$sweepAfter = Run-Py -PyArgs @("scripts\_podcast_sweep.py", "--total") -TimeoutMin 10
$after = $backlog
foreach ($ln in $sweepAfter) { if ($ln -match '^\s*(\d+)\s*$') { $after = [int]$Matches[1]; break } }
Write-Log ("Podcasts made+verified: {0} ({1} still pending)" -f ([Math]::Max(0, $backlog - $after)), $after)

Write-Log "=== Daily podcast build END ==="

} finally {
    Remove-Item $lockFile -Force -ErrorAction SilentlyContinue
    Write-Log "Lock released."
}
