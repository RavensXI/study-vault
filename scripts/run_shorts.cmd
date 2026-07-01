@echo off
REM Daily NotebookLM short-form video batch — run by the "StudyVaultShorts" scheduled task (every 25h).
cd /d "C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox"
"C:\Users\tshau\AppData\Local\Programs\Python\Python312\python.exe" -u scripts\batch_short_videos.py --daily-cap 180 >> "%TEMP%\sv_shorts.log" 2>&1
