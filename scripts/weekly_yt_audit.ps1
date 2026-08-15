# Weekly YouTube link audit (Tom, 16 Aug: "put that as a weekly sweep/audit").
# Runs the full site-wide check; on dead links (exit 1) emails via Resend when
# the keys are present in the task's environment (same store the shorts alert
# uses). The report always lands in scripts\_yt_audit_report.md.
$repo = "C:\Users\tshau\Documents\Study Vault"
Set-Location $repo
$out = & python "$repo\scripts\audit_youtube_links.py" 2>&1
$code = $LASTEXITCODE
$tail = ($out | Select-Object -Last 3) -join "`n"
Add-Content -Path "$repo\scripts\_yt_audit_runs.log" -Encoding utf8 -Value ("[{0}] exit {1} | {2}" -f (Get-Date -Format s), $code, ($out | Select-Object -Last 1))

if ($code -ne 0 -and $env:RESEND_API_KEY -and $env:NOTIFY_TO -and $env:NOTIFY_FROM) {
  $body = @{ from = $env:NOTIFY_FROM; to = @($env:NOTIFY_TO);
             subject = "StudyVault: weekly YouTube audit found dead links";
             text = "The weekly sweep found dead links.`n`n$tail`n`nFull report: scripts\_yt_audit_report.md" } | ConvertTo-Json
  try {
    Invoke-RestMethod -Uri "https://api.resend.com/emails" -Method Post `
      -Headers @{ Authorization = "Bearer $($env:RESEND_API_KEY)" } `
      -ContentType "application/json" -Body $body | Out-Null
  } catch {}
}
exit $code
