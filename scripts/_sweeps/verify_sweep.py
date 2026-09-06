"""Independent re-derivation: re-read every LIVE lesson and count what the
sweep was supposed to remove. Does not reuse the sweep's own bookkeeping."""
import json, os, re, sys, urllib.request, collections
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep_labels as S

U, K = os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"]
H = {"apikey": K, "Authorization": "Bearer " + K}
def g(p):
    return json.loads(urllib.request.urlopen(urllib.request.Request(f"{U}/rest/v1/{p}", headers=H), timeout=180).read())

rows, off = [], 0
while True:
    b = g(f"lessons?status=eq.live&select=id,exam_tip_html,practice_questions&order=id&limit=300&offset={off}")
    rows += b
    if len(b) < 300: break
    off += 300
inv_q = house_q = 0
fam = collections.Counter()
house_pat = re.compile(r"(?<![A-Za-z0-9\-])(Top band|Upper-mid band|Mid band|Lower-mid band|Low band)")
for r in rows:
    for q in (r.get("practice_questions") or []):
        if not isinstance(q, dict) or not isinstance(q.get("marks"), str): continue
        m = q["marks"]
        if S.INV_RE.search(m): inv_q += 1
        if house_pat.search(m): house_q += 1
        wl=[]
        new,_n = S.sweep2(m, wl, {"f":"marks"})
        if new != m: fam[("marks","STILL-REWRITABLE")] += 1
        for e in wl: fam[("marks", e["reason"])] += 1
    t = r.get("exam_tip_html")
    if isinstance(t, str):
        wl=[]
        new,_n = S.sweep2(t, wl, {"f":"tip"})
        if new != t: fam[("exam_tip","STILL-REWRITABLE")] += 1
        for e in wl: fam[("exam_tip", e["reason"])] += 1
print(f"live lessons re-read: {len(rows)}")
print(f"questions still carrying an invented band label: {inv_q}")
print(f"questions carrying a house band label:           {house_q}")
print("residual sweep-2 state (re-running the sweep on live text):")
for k,v in sorted(fam.items(), key=lambda kv:-kv[1]): print(f"   {v:4d}  {k[0]}: {k[1]}")
