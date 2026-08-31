import glob
import os
import re

D = r'C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scripts\_shorts_daily_logs'
for f in sorted(glob.glob(os.path.join(D, '2026-0*.log')))[-14:]:
    t = open(f, encoding='utf-8', errors='replace').read()
    skip = len(re.findall(r'endcard trim skipped', t))
    cut = len(re.findall(r'endcard trimmed|trimmed endcard|endcard cut|trimming endcard', t))
    print(os.path.basename(f)[:10], 'skipped', skip, '| trimmed', cut)
