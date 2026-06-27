"""Discover SAM (the fictional student)'s real subjects -> units -> lessons from
Supabase, applying the same `keep` filters the design-lab dashboard uses.
Writes a JSON map to the scratchpad so we can author per-unit sketch backdrops.
Run:  python scripts/_designlab_sam_discover.py
"""
import json, os, sys
from supabase import create_client

URL = os.environ["SUPABASE_URL"]; KEY = os.environ["SUPABASE_SERVICE_KEY"]
sb = create_client(URL, KEY)

# mirrors design-lab/dashboard.html STUDENT[]
STUDENT = [
    {"n": "Mathematics",        "k": "maths-ocr"},
    {"n": "English Language",   "k": "english-language-ocr"},
    {"n": "English Literature", "k": "english-literature-aqa",
     "keep": ["Macbeth", "A Christmas Carol", "An Inspector Calls", "Power & Conflict Poetry", "Unseen Poetry"]},
    {"n": "Combined Science",   "k": "science-aqa", "keepre": "Paper"},
    {"n": "History",            "k": "history-ocr",
     "keep": ["International Relations 1918-1975", "Germany 1925-1955: The People and the State",
              "Migration to Britain c.1000-c.2010", "The USA 1919-1948: The People and the State"]},
    {"n": "Geography",          "k": "geography-edexcel-b"},
    {"n": "Spanish",            "k": "spanish-edexcel"},
    {"n": "Computer Science",   "k": "computer-science"},
    {"n": "Religious Studies",  "k": "religious-studies-aqa",
     "keep": ["Christianity: Beliefs", "Christianity: Practices", "Islam: Beliefs", "Islam: Practices",
              "Theme A: Relationships & Families", "Theme B: Religion & Life",
              "Theme D: Peace & Conflict", "Theme E: Crime & Punishment"]},
]

out = {}
for s in STUDENT:
    res = (sb.table("lessons")
           .select("lesson_number, title, units!inner(slug, name, subjects!inner(slug, school_id))")
           .eq("status", "live").is_("units.subjects.school_id", "null")
           .eq("units.subjects.slug", s["k"]).limit(900).execute())
    rows = res.data or []
    keep = s.get("keep"); keepre = s.get("keepre")
    if keep:
        rows = [r for r in rows if r["units"]["name"] in keep]
    elif keepre:
        rows = [r for r in rows if keepre in r["units"]["name"]]
    byu = {}
    for r in rows:
        u = r["units"]; sl = u["slug"]
        byu.setdefault(sl, {"slug": sl, "name": u["name"], "lessons": []})
        byu[sl]["lessons"].append({"no": r["lesson_number"], "t": r["title"]})
    units = list(byu.values())
    if keep:
        units.sort(key=lambda u: keep.index(u["name"]) if u["name"] in keep else 99)
    else:
        units.sort(key=lambda u: u["name"])
    for u in units:
        u["lessons"].sort(key=lambda L: L["no"])
    out[s["k"]] = {"name": s["n"], "units": [
        {"slug": u["slug"], "name": u["name"], "count": len(u["lessons"]),
         "titles": [L["t"] for L in u["lessons"]]} for u in units]}
    print(f'{s["k"]:28} {len(units)} units, {sum(len(u["lessons"]) for u in units)} lessons')

dest = os.path.join(os.environ.get("TEMP", "/tmp"), "sam_units.json")
# also drop a copy next to the design lab for the generator
local = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scratch_sam_units.json")
for p in (dest, local):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
print("wrote", local)
