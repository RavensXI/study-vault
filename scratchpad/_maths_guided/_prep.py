# -*- coding: utf-8 -*-
"""Fan-out prep: (1) verify the Unity/free two-for-one claim for maths Edexcel,
(2) fresh rollback dump of all 48 maths-edexcel practice_data rows,
(3) emit the lesson work-list (key -> id) minus algebra-L09."""
import json, io, os, sys, urllib.request

sys.stdout.reconfigure(errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]

def get(path):
    r = urllib.request.Request(SUPA + path,
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    return json.load(urllib.request.urlopen(r))

# (1) all maths-ish subjects and their school scoping
subs = get("/rest/v1/subjects?or=(slug.ilike.*math*,name.ilike.*math*)&select=id,slug,name,school_id")
print("maths subjects:")
for s in subs:
    print("  ", s["slug"], "| school_id:", s["school_id"], "|", s["name"])

# (2) fresh dump of maths-edexcel
med = [s for s in subs if s["slug"] == "maths-edexcel"][0]
rows = get("/rest/v1/lessons?select=id,lesson_number,title,practice_data,units!inner(slug,subject_id)"
           "&units.subject_id=eq." + med["id"] + "&order=lesson_number")
rows = [r for r in rows if r["units"]["subject_id"] == med["id"]]
out = os.path.join(ROOT, "scratchpad", "_maths_guided", "_pre_fanout_dump.json")
io.open(out, "w", encoding="utf-8").write(json.dumps(rows, ensure_ascii=False))
print("dumped", len(rows), "lessons ->", out)

# (3) work-list
wl = {}
for r in rows:
    k = r["units"]["slug"] + "-L%02d" % r["lesson_number"]
    if k != "algebra-L09":
        wl[k] = {"id": r["id"], "title": r["title"], "unit": r["units"]["slug"], "n": r["lesson_number"]}
io.open(os.path.join(ROOT, "scratchpad", "_maths_guided", "_worklist.json"), "w",
        encoding="utf-8").write(json.dumps(wl, ensure_ascii=False, indent=1))
print("worklist:", len(wl), "lessons")
units = {}
for k, v in wl.items():
    units[v["unit"]] = units.get(v["unit"], 0) + 1
print("units:", json.dumps(units))
