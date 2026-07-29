# -*- coding: utf-8 -*-
"""Build the platform hero-regeneration worklist from the vision-audit ledger.

Included (free-tier subjects only):
  - every C-grade (wrong image)
  - every confirmed-dead hero (404)
  - within-subject duplicates: keep the best-graded lesson per image
    (A > B > C, then lowest lesson number), regenerate the rest
School-bespoke subjects are written to a separate report for Tom.

Output: scratchpad/_hero_regen_worklist.json  (+ _hero_school_report.json)
"""
import io
import json
import os
import sys
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

SCRATCH = os.path.join(
    r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault",
    r"b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
LEDGER = os.path.join(SCRATCH, "_hero_vision_audit.jsonl")

by_id = {}
with io.open(LEDGER, encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        by_id[r["lesson_id"]] = r
recs = list(by_id.values())

work = {}   # lesson_id -> record + reason
school_report = []

def add(r, reason):
    if r.get("school"):
        school_report.append({**{k: r[k] for k in
                             ("subject", "unit", "n", "title", "url")},
                              "reason": reason, "shows": r.get("shows", "")})
        return
    if r["lesson_id"] not in work:
        work[r["lesson_id"]] = {**r, "reason": reason}

# 1. wrong images + dead links
for r in recs:
    if r["grade"] == "C":
        add(r, "wrong-image")
    elif r["grade"] == "FETCH_FAIL" and "404" in r.get("error", ""):
        add(r, "dead-link")

# 2. within-subject duplicates — keep the best one
groups = defaultdict(list)
for r in recs:
    if r["grade"] in "ABC":
        groups[(r["subject"], r["url"])].append(r)
for (subj, url), members in groups.items():
    if len(members) < 2:
        continue
    members.sort(key=lambda r: ("ABC".index(r["grade"]), r["n"]))
    for r in members[1:]:
        add(r, "duplicate")

rows = sorted(work.values(), key=lambda r: (r["subject"], r["unit"], r["n"]))
out = os.path.join(SCRATCH, "_hero_regen_worklist.json")
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=1, ensure_ascii=False)
rep = os.path.join(SCRATCH, "_hero_school_report.json")
with io.open(rep, "w", encoding="utf-8") as f:
    json.dump(school_report, f, indent=1, ensure_ascii=False)

from collections import Counter
print("regen worklist:", len(rows), dict(Counter(r["reason"] for r in rows)))
print("subjects:", len({r['subject'] for r in rows}))
print("school-bespoke report (no auto-write):", len(school_report))
