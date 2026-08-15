# -*- coding: utf-8 -*-
"""Music MC misconception drafts — DESK ONLY, never --apply.

Runs enrich_mc.py in dry-run mode for each music practice unit and collects
each _canary_preview.json into _music_draft_{unit}.json. Errors are printed
in full and the loop BREAKS on credit/5xx failures rather than serenely
continuing (the 14 Aug fleet lesson: a grep-filtered loop hid 33 failures).
"""
import io
import os
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
UNITS = ["western-classical-1650-1910", "score-reading", "listening-skills",
         "aos-listening"]
FATAL = ("credit balance", "insufficient_quota", "overloaded", "529", "522")

for unit in UNITS:
    print("=== %s ===" % unit, flush=True)
    r = subprocess.run([sys.executable, os.path.join(HERE, "enrich_mc.py"),
                        "--subject", "music-aqa", "--unit", unit],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    tail = (r.stdout or "")[-1200:]
    print(tail, flush=True)
    if r.returncode != 0:
        print("FAILED (exit %d). stderr tail:" % r.returncode)
        print((r.stderr or "")[-1500:])
        low = ((r.stdout or "") + (r.stderr or "")).lower()
        if any(f in low for f in FATAL):
            print("FATAL error pattern — stopping the loop.")
            sys.exit(2)
        continue
    src = os.path.join(HERE, "_canary_preview.json")
    dst = os.path.join(HERE, "_music_draft_%s.json" % unit)
    if os.path.exists(src):
        shutil.copy(src, dst)
        print("saved ->", dst, "(%d bytes)" % os.path.getsize(dst))
    else:
        print("WARN: no preview produced for", unit)
print("ALL UNITS DONE")
