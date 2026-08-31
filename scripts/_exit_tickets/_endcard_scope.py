# When did endcard trimming stop working, and how many clips are affected?
import glob
import os
import re

D = r'C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scripts\_shorts_daily_logs'
tot_skip = tot_trim = 0
first_bad = None
for f in sorted(glob.glob(os.path.join(D, '*.log'))):
    t = open(f, encoding='utf-8', errors='replace').read()
    skip = len(re.findall(r'endcard trim skipped', t))
    # a successful trim prints the new duration / trimmed marker
    trim = len(re.findall(r'endcard trimmed|trimmed \d|\(trimmed', t))
    day = os.path.basename(f)[:10]
    if skip or trim:
        print(f'{day}  skipped {skip:4d}  trimmed {trim:4d}')
    tot_skip += skip
    tot_trim += trim
    if skip and not trim and first_bad is None:
        first_bad = day
print()
print(f'TOTAL across all logs: skipped {tot_skip}, trimmed {tot_trim}')
print('first all-skip day:', first_bad)
