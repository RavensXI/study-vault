# -*- coding: utf-8 -*-
"""Live subject/lesson census straight from Supabase.

    python scripts/audit_subject_status.py            # summary
    python scripts/audit_subject_status.py --subjects # per-subject live lesson counts

This is the canonical source for the counts snapshot in CLAUDE.md -
re-run it and re-stamp the date whenever the doc's numbers are updated.
"""
import io
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import date

SB = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ["SUPABASE_ANON_KEY"]

sys.stdout.reconfigure(encoding="utf-8")


def get(path):
    req = urllib.request.Request(
        SB + path, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def paged(path):
    rows, off = [], 0
    while True:
        page = get("%s&order=id&limit=1000&offset=%d" % (path, off))
        rows += page
        if len(page) < 1000:
            return rows
        off += 1000


subs = get("/rest/v1/subjects?select=id,slug,name,school_id,status&limit=300")
schools = {s["id"]: s["name"] for s in get("/rest/v1/schools?select=id,name")}
sub_info = {s["id"]: s for s in subs}
unit_sub = {u["id"]: u["subject_id"]
            for u in paged("/rest/v1/units?select=id,subject_id")}
lessons = paged("/rest/v1/lessons?select=unit_id,status")

tier_all, tier_live, status_all = Counter(), Counter(), Counter()
per_subject_live = Counter()
for r in lessons:
    s = sub_info.get(unit_sub.get(r["unit_id"]))
    t = "orphan" if not s else (
        "free" if not s["school_id"] else schools.get(s["school_id"], "?"))
    tier_all[t] += 1
    status_all[r["status"]] += 1
    if r["status"] == "live":
        tier_live[t] += 1
        if s:
            per_subject_live[s["slug"]] += 1

free_live_subjects = sorted(
    s["slug"] for s in subs
    if not s["school_id"] and s["status"] == "live")

print("=== StudyVault census, %s ===" % date.today().isoformat())
print("lessons total: %d   by status: %s" % (len(lessons), dict(status_all)))
print("lessons by tier (all): %s" % dict(tier_all))
print("lessons by tier (live): %s" % dict(tier_live))
print("free-tier subjects live: %d" % len(free_live_subjects))
for name in sorted(set(schools.values())):
    n = sum(1 for s in subs
            if s["school_id"] and schools.get(s["school_id"]) == name
            and s["status"] != "archived")
    print("%s subjects (non-archived): %d" % (name, n))

if "--subjects" in sys.argv:
    print()
    for slug in sorted(per_subject_live, key=per_subject_live.get, reverse=True):
        print("%5d  %s" % (per_subject_live[slug], slug))
