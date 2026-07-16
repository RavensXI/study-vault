# -*- coding: utf-8 -*-
"""Board fan-out prep: worklists + rollback dumps for maths-aqa / maths-ocr /
maths-eduqas, plus a structure comparison against maths-edexcel."""
import json, io, os, sys, urllib.request

sys.stdout.reconfigure(errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]

def get(path):
    r = urllib.request.Request(SUPA + path,
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    return json.load(urllib.request.urlopen(r))

subs = {s["slug"]: s["id"] for s in get("/rest/v1/subjects?slug=in.(maths-aqa,maths-ocr,maths-eduqas)&select=id,slug")}
for slug, sid in subs.items():
    rows = get("/rest/v1/lessons?select=id,lesson_number,title,practice_data,units!inner(slug,subject_id)"
               "&units.subject_id=eq." + sid + "&order=lesson_number")
    rows = [r for r in rows if r["units"]["subject_id"] == sid]
    io.open(os.path.join(HERE, "_pre_dump_%s.json" % slug), "w", encoding="utf-8").write(json.dumps(rows, ensure_ascii=False))
    wl = {}
    units = {}
    sim = []
    for r in rows:
        k = r["units"]["slug"] + "-L%02d" % r["lesson_number"]
        wl[k] = {"id": r["id"], "title": r["title"], "unit": r["units"]["slug"], "n": r["lesson_number"]}
        units[r["units"]["slug"]] = units.get(r["units"]["slug"], 0) + 1
        if "simultaneous" in (r["title"] or "").lower():
            sim.append(k + " : " + r["title"])
    io.open(os.path.join(HERE, "_worklist_%s.json" % slug), "w", encoding="utf-8").write(json.dumps(wl, ensure_ascii=False, indent=1))
    print(slug, "->", len(rows), "lessons | units:", json.dumps(units))
    print("   simultaneous-equations lessons:", sim)
