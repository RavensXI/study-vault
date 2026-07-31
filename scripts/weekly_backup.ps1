# StudyVault weekly backup ("StudyVaultBackup" scheduled task, Sundays 03:00).
# 1) Supabase tables + auth list + git bundle + business folder + memory
#    -> OneDrive (versioned, 30-day recycle bin)
# 2) rclone sync of all three R2 buckets -> Backblaze B2 mirror
#    (bucket has 30-day COMPLIANCE object lock: deletions stay recoverable
#    even with the key, so a bad sync can never destroy the mirror)
$ErrorActionPreference = "Continue"
$repo = "C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox"
Set-Location $repo
$logDir = Join-Path $repo "scripts\_backup_logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$log = Join-Path $logDir ("{0}.log" -f (Get-Date -Format "yyyy-MM-dd"))
function L { param([string]$m) Add-Content -Path $log -Value ("{0} {1}" -f (Get-Date -Format "HH:mm:ss"), $m) }

L "=== weekly backup START ==="
$python = "C:\Users\tshau\AppData\Local\Programs\Python\Python312\python.exe"
& $python "scripts\_backup_studyvault.py" *>> $log
L "supabase/onedrive stage done"

$rclone = Get-ChildItem "C:\Users\tshau\AppData\Local\Microsoft\WinGet\Packages" -Recurse -Filter rclone.exe -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
if (-not $rclone) { L "rclone NOT FOUND - R2 mirror skipped"; L "=== END ==="; exit 1 }
foreach ($b in @("studyvault-images", "studyvault-audio", "studyvault-video")) {
    L ("rclone sync {0}" -f $b)
    & $rclone sync ("r2:{0}" -f $b) ("b2:studyvault-mirror-2026/{0}" -f $b) `
        --transfers 8 --checkers 16 --fast-list --b2-hard-delete=false --stats-one-line --stats 5m *>> $log
    L ("{0} exit code {1}" -f $b, $LASTEXITCODE)
}
L "=== weekly backup END ==="
