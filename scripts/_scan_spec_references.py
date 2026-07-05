"""Platform-wide scan for exam-board spec references in lesson content —
policy: NO lesson may cite spec points/codes (legal-exposure minimisation).
High-precision patterns only ('design specification' in D&T etc. must NOT
match): explicit 'spec reference/point', spec-code citations, board codes.
Read-only; prints per-subject counts + sample contexts.
"""
import json, os, re, sys, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": KEY, "Authorization": "Bearer " + KEY}

PAT = re.compile(
    r"\bspec(?:ification)?\s+(?:ref(?:erence)?s?|points?|sections?)\b"      # spec reference / spec point
    r"|\bspec\s+\d\.\d"                                                      # spec 1.2
    r"|\b(?:J27[67]|J834|J836|J31[0-9]|J25\d|J26\d|J625|C660U|C100QS|1MA1|1BS0|1HI0|8035|8464|846[123]|8552|8585|8062|8182|8700|8702|8692|8662|8652|8542|8271)\b",
    re.I)

FIELDS = ["content_html", "description", "practice_questions", "knowledge_checks", "flashcard_questions"]

def page(off):
    sel = "id,lesson_number," + ",".join(FIELDS) + ",units(slug,subjects(slug,school_id))"
    u = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?select={sel}&order=id&limit=200&offset={off}"
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=120))

hits, samples = {}, []
off = 0
while True:
    rows = page(off)
    if not rows: break
    for r in rows:
        for f in FIELDS:
            v = r.get(f)
            if v is None: continue
            t = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
            ms = list(PAT.finditer(t))
            if not ms: continue
            sub = (r.get("units") or {}).get("subjects") or {}
            key = f"{sub.get('slug','?')}{'[school]' if sub.get('school_id') else ''}"
            hits.setdefault(key, {}).setdefault(f, 0)
            hits[key][f] += len(ms)
            if len(samples) < 40:
                m = ms[0]
                ctx = re.sub("<[^>]+>", "", t[max(0, m.start()-70):m.end()+50]).replace("\n", " ")
                samples.append(f"{key}/{(r.get('units') or {}).get('slug','?')}/L{r.get('lesson_number')} [{f}]: …{ctx}…")
    if len(rows) < 200: break
    off += 200

print("=== per-subject spec-reference hits ===")
for k in sorted(hits):
    print(k, json.dumps(hits[k]))
print(f"\nsubjects affected: {len(hits)} | total hits: {sum(sum(v.values()) for v in hits.values())}")
print("\n=== samples ===")
for s in samples:
    print(" ", s[:200])
