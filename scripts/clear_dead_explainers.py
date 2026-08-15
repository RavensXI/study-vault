# -*- coding: utf-8 -*-
"""Clear the 27 dead psychology-edexcel + history-aqa explainer jobs
(Tom, 16 Aug: "yeah clear them").

Why: a job pinned in_progress blocks the queue from ever re-creating that
lesson's explainer (2 Aug podcast precedent). These 27 burned all refires on
notebooks that swallow every create. Removing the entries lets the next
hourly wrapper run build FRESH notebooks. The 12 music jobs stay pinned on
purpose — they hold music out of the queue until Tom's review flips the
lessons live (verified inert: refires=3, nothing fired in 4+ days of hourly
runs).

Pre-checked: none of the 39 lessons has any video on the site.

Waits for the 'StudyVault - Daily Explainer Build' task to exit first so the
batch's end-of-run state save cannot clobber this edit.
"""
import json
import shutil
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
STATE = r"C:\Users\tshau\Documents\Study Vault\scripts\_batch_explainer_state.json"
CLEAR_PREFIXES = ("psychology-edexcel/", "history-aqa/")


def task_running():
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "(Get-ScheduledTask -TaskName 'StudyVault - Daily Explainer Build').State"],
        capture_output=True, text=True)
    return "Running" in (r.stdout or "")


waited = 0
while task_running():
    if waited >= 3600:
        print("ABORT: wrapper still running after 60 min — not touching state")
        sys.exit(1)
    time.sleep(20)
    waited += 20
print("wrapper idle after %ds wait" % waited)

with open(STATE, encoding="utf-8") as f:
    st = json.load(f)
before = len(st["jobs"])
stuck = [j for j in st["jobs"] if j.get("status") == "in_progress"]
clear = [j for j in stuck if j["label"].startswith(CLEAR_PREFIXES)]
keep_music = [j for j in stuck if j["label"].startswith("music-aqa/")]
print("in_progress: %d | clearing: %d | music held: %d"
      % (len(stuck), len(clear), len(keep_music)))
assert len(clear) == 27, "expected 27 psych/history jobs, found %d" % len(clear)
assert len(keep_music) == 12, "expected 12 music jobs, found %d" % len(keep_music)

bak = STATE + ".bak-20260816-clear27"
shutil.copy(STATE, bak)
cleared_ids = {id(j) for j in clear}
st["jobs"] = [j for j in st["jobs"] if id(j) not in cleared_ids]
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(st, f)

with open(STATE, encoding="utf-8") as f:
    chk = json.load(f)
left = [j for j in chk["jobs"] if j.get("status") == "in_progress"]
print("after: %d jobs (was %d); in_progress now %d, all music: %s"
      % (len(chk["jobs"]), before, len(left),
         all(j["label"].startswith("music-aqa/") for j in left)))
print("backup:", bak)
print("DONE — the next hourly wrapper run re-queues the 27 on fresh notebooks")
