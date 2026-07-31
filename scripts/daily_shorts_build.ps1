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
$cooldownHours = 23.9167  # 23h55m — catches the SAME hourly slot daily (24h05m drifted +1h/day) — rolling quota window + safety buffer
$lockStaleHours = 12      # treat lock as orphaned past this (run probably crashed)
$python = "C:\Users\tshau\AppData\Local\Programs\Python\Python312\python.exe"

function Write-Log {
    param([string]$Message)
    $line = "{0} {1}" -f (Get-Date -Format "HH:mm:ss"), $Message
    Add-Content -Path $logFile -Value $line -Encoding utf8
}

# Email alert via Resend (same creds the app's bug-report/subject-request use).
# No-ops quietly if the env vars are not set in the task's environment.
function Send-Alert {
    param([string]$Subject, [string]$Body)
    $k = $env:RESEND_API_KEY; $to = $env:NOTIFY_TO; $frm = $env:NOTIFY_FROM
    if (-not ($k -and $to -and $frm)) { Write-Log "Alert skipped: RESEND_API_KEY/NOTIFY_TO/NOTIFY_FROM not set in task env."; return }
    try {
        $payload = @{ from = $frm; to = @($to); subject = $Subject; text = $Body } | ConvertTo-Json
        Invoke-RestMethod -Method Post -Uri "https://api.resend.com/emails" `
            -Headers @{ Authorization = "Bearer $k" } -ContentType "application/json" -Body $payload | Out-Null
        Write-Log ("Alert sent: " + $Subject)
    } catch { Write-Log ("Alert send failed: " + $_.Exception.Message) }
}
$authFlag = Join-Path $logDir "_auth_alerted.flag"   # one alert per auth-outage episode, cleared on next success

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
# Auth expired: the batch's own self-heal (retried) could not restore it. Do NOT
# stamp the launch — that would burn the whole 24h cooldown on a dead session (as
# on 24 Jul 2026). Skipping unstamped means the NEXT hourly heartbeat retries, so
# the run resumes within an hour of auth coming back. Alert once per episode.
if ($dry -match "AUTH EXPIRED") {
    Write-Log "NotebookLM auth EXPIRED (self-heal failed). Skipping WITHOUT stamping launch - retries next hour, no day lost."
    if (-not (Test-Path $authFlag)) {
        Send-Alert "StudyVault shorts: NotebookLM auth expired" "The daily shorts batch can't run - NotebookLM auth expired and the saved-profile self-heal did not restore it. Run 'nlm login' on the shorts machine. The task retries every hour and resumes automatically once auth is back - no day is lost while it's down."
        New-Item -ItemType File -Path $authFlag -Force | Out-Null
    }
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
    # ── Stage 1: PODCASTS (priority over shorts) ──────────────────────────
    # Live free-tier lessons missing our "Lesson Podcast" — usually zero.
    # A new subject enters this sweep automatically the day its lessons flip
    # to live; nobody has to remember to fire a batch. Conservative budget
    # model: one shared 100/day NLM pool (downgraded-Ultra tier) — if audio
    # and video prove to be separate pools, drop the subtraction below.
    $nlmBudget = 100
    $podcastsMade = 0
    $sweepOut = Run-Py -PyArgs @("scripts\_podcast_sweep.py", "--total") -TimeoutMin 10
    $backlog = 0
    foreach ($ln in $sweepOut) { if ($ln -match '^\s*(\d+)\s*$') { $backlog = [int]$Matches[1]; break } }
    if ($backlog -gt 0) {
        Write-Log ("PODCAST backlog: {0} live lessons - podcasts run first today." -f $backlog)
        # batch_podcasts' bare sweep walks a stale hardcoded SUBJECT_ORDER, so
        # the dispatcher must name each subject explicitly from the sweep.
        $sweepJson = Run-Py -PyArgs @("scripts\_podcast_sweep.py", "--json") -TimeoutMin 10
        $subjects = @()
        foreach ($ln in $sweepJson) {
            if ($ln -match '^\s*\{') { $subjects = (ConvertFrom-Json $ln).subjects; break }
        }
        $left = $nlmBudget
        foreach ($subj in $subjects) {
            if ($left -le 0) { break }
            $take = [Math]::Min([int]$subj.pending, $left)
            Write-Log ("PODCASTS: {0} - requesting {1}" -f $subj.slug, $take)
            Run-Py -PyArgs @("scripts\batch_podcasts.py", "--subject", $subj.slug, "--live-only", "--limit", "$take") -TimeoutMin 90 | Out-Null
            $left -= $take
        }
        for ($i = 0; $i -lt 15; $i++) {
            Start-Sleep -Seconds 300
            $st = Run-Py -PyArgs @("scripts\batch_podcasts.py", "--status") -TimeoutMin 15
            if (($st -match "No in-progress jobs") -or ($st -match ", 0 still in progress")) { break }
        }
        Run-Py -PyArgs @("scripts\batch_podcasts.py", "--download", "--cleanup") -TimeoutMin 120 | Out-Null
        # verified count = backlog shrinkage re-measured from Supabase (catches
        # the old "--download didn't write Supabase" failure by construction)
        $sweepAfter = Run-Py -PyArgs @("scripts\_podcast_sweep.py", "--total") -TimeoutMin 10
        $after = $backlog
        foreach ($ln in $sweepAfter) { if ($ln -match '^\s*(\d+)\s*$') { $after = [int]$Matches[1]; break } }
        $podcastsMade = [Math]::Max(0, $backlog - $after)
        Write-Log ("PODCASTS made+verified: {0} ({1} still pending for tomorrow)" -f $podcastsMade, $after)
    }

    # ── Stage 2: SHORTS with whatever budget remains ─────────────────────
    $shortsCap = [Math]::Max(0, $nlmBudget - $podcastsMade)
    if ($shortsCap -eq 0) {
        Write-Log "NLM budget fully consumed by podcasts - no shorts today."
        $main = @()
    } else {
        $main = Run-Py -PyArgs @("scripts\batch_short_videos.py", "--daily-cap", "$shortsCap") -TimeoutMin 300
    }
    if ($main -match "AUTH EXPIRED") {
        # Auth died AFTER the dry-run passed (rare). Rewind the launch stamp so the
        # next hourly heartbeat retries instead of waiting a full 24h.
        Write-Log "Auth expired MID-RUN. Rewinding launch stamp so the next hour retries."
        Remove-Item $lastLaunchFile -Force -ErrorAction SilentlyContinue
        if (-not (Test-Path $authFlag)) {
            Send-Alert "StudyVault shorts: NotebookLM auth expired mid-run" "The daily shorts batch stopped part-way - NotebookLM auth expired mid-run. Run 'nlm login' on the shorts machine. The task retries next hour and resumes automatically once auth is back."
            New-Item -ItemType File -Path $authFlag -Force | Out-Null
        }
    } else {
        Remove-Item $authFlag -Force -ErrorAction SilentlyContinue   # healthy run: clear any prior auth-outage alert
    }
    # Post-pass: map recall questions onto tonight's new shorts (headless
    # `claude -p` on the subscription, deterministic fallback inside) and
    # extract their poster frames. Delta-based and idempotent — if it fails,
    # tomorrow's run catches up; it never affects the batch above.
    Run-Py -PyArgs @("scripts\_shorts_postpass.py") -TimeoutMin 45 | Out-Null
    Write-Log "=== Daily shorts build END ==="
} finally {
    Remove-Item $lockFile -Force -ErrorAction SilentlyContinue
    Write-Log "Lock released."
}
