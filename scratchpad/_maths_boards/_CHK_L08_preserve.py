import json

ID = "47a41e5d-3d22-45fd-a1c0-b29405585d87"
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
live = json.load(open("_CHK_L08_live.json", encoding="utf-8"))

# find pre entry
entry = None
if isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID]
    elif "lessons" in pre:
        for l in pre["lessons"]:
            if l.get("id") == ID:
                entry = l.get("practice_data"); break
    else:
        # maybe keyed by id -> {practice_data}
        for k,v in pre.items():
            if isinstance(v, dict) and v.get("id")==ID:
                entry = v.get("practice_data"); break
elif isinstance(pre, list):
    for l in pre:
        if l.get("id") == ID:
            entry = l.get("practice_data"); break

if entry is None:
    print("PRE ENTRY NOT FOUND. top-level type:", type(pre))
    if isinstance(pre, dict):
        print("keys sample:", list(pre.keys())[:5])
    if isinstance(pre, list):
        print("list len", len(pre), "sample keys:", list(pre[0].keys()) if pre else None)
    raise SystemExit

# if entry is the full row, get practice_data
if "practice_data" in entry and "problem_bank" not in entry:
    entry = entry["practice_data"]

print("PRE keys:", sorted(entry.keys()))
print("LIVE keys:", sorted(live.keys()))

for f in ["related_videos", "topic_links"]:
    same = entry.get(f) == live.get(f)
    print(f"{f}: preserved={same}")
    if not same:
        print("  PRE:", json.dumps(entry.get(f))[:300])
        print("  LIVE:", json.dumps(live.get(f))[:300])

# worked_examples may be trimmed by spec; compare
print("worked_examples PRE:", json.dumps(entry.get("worked_examples"))[:500])
print("worked_examples same:", entry.get("worked_examples")==live.get("worked_examples"))

# pre problem_bank solutions vs live
def sols(d):
    pb=d.get("problem_bank",{})
    out={}
    for t in ["bronze","silver","gold"]:
        out[t]=[p.get("solutions") for p in pb.get(t,[])]
    return out
print("PRE sols:", sols(entry))
print("LIVE sols:", sols(live))
# pre displays
def disp(d):
    pb=d.get("problem_bank",{})
    out={}
    for t in ["bronze","silver","gold"]:
        out[t]=[p.get("display") for p in pb.get(t,[])]
    return out
pd=disp(entry); ld=disp(live)
for t in ["bronze","silver","gold"]:
    for i,(a,b) in enumerate(zip(pd[t],ld[t])):
        # strip svg for comparison of text
        import re
        ta=re.sub(r'<svg.*?</svg>','',a or '',flags=re.S)
        tb=re.sub(r'<svg.*?</svg>','',b or '',flags=re.S)
        if ta.strip()!=tb.strip():
            print(f"DISPLAY TEXT CHANGED {t}[{i}]:")
            print("  PRE:", ta.strip()[:200])
            print("  LIVE:", tb.strip()[:200])
