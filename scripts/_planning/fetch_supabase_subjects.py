"""Read-only pull of the subjects table (+ live lesson counts) for build planning."""
import json, os, urllib.parse, urllib.request

URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Accept": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))


def rest(table, query):
    out, offset = [], 0
    while True:
        u = f"{URL}/rest/v1/{table}?{query}&limit=1000&offset={offset}"
        req = urllib.request.Request(u, headers=H)
        page = json.load(urllib.request.urlopen(req, timeout=120))
        out += page
        if len(page) < 1000:
            return out
        offset += 1000


subjects = rest("subjects", "select=id,slug,name,exam_board,spec_code,school_id,status")
schools = rest("schools", "select=id,name,slug")
units = rest("units", "select=id,subject_id")
lessons = rest("lessons", "select=id,unit_id,status")

u2s = {u["id"]: u["subject_id"] for u in units}
counts = {}
for l in lessons:
    sid = u2s.get(l["unit_id"])
    if not sid:
        continue
    c = counts.setdefault(sid, {"total": 0, "live": 0})
    c["total"] += 1
    if l.get("status") == "live":
        c["live"] += 1
for s in subjects:
    c = counts.get(s["id"], {"total": 0, "live": 0})
    s["lessons_total"] = c["total"]
    s["lessons_live"] = c["live"]

json.dump({"subjects": subjects, "schools": schools},
          open(os.path.join(HERE, "_supabase_subjects.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
free = [s for s in subjects if not s["school_id"]]
print(f"subjects={len(subjects)} free-tier={len(free)} units={len(units)} lessons={len(lessons)}")
print(f"free-tier lessons total={sum(s['lessons_total'] for s in free)}")
