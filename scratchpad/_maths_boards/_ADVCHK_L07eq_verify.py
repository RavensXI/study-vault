# -*- coding: utf-8 -*-
import json

ID = "5ead70d6-f265-4790-86b5-573b9b16606a"
live = json.load(open("_ADVCHK_L07eq_live.json", encoding="utf-8"))
pre_all = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))

# find pre entry
pre = None
if isinstance(pre_all, list):
    for r in pre_all:
        if r.get("id") == ID:
            pre = r.get("practice_data"); break
elif isinstance(pre_all, dict):
    if ID in pre_all:
        pre = pre_all[ID]
        if isinstance(pre, dict) and "practice_data" in pre:
            pre = pre["practice_data"]
    else:
        # maybe keyed by slug
        for k,v in pre_all.items():
            if isinstance(v, dict) and v.get("id")==ID:
                pre = v.get("practice_data"); break
print("pre found:", pre is not None)
if pre is None:
    print("pre_all type:", type(pre_all))
    if isinstance(pre_all, dict):
        print("keys sample:", list(pre_all.keys())[:5])
    elif isinstance(pre_all, list):
        print("list len", len(pre_all), "first keys:", list(pre_all[0].keys()) if pre_all else None)
else:
    for fld in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pre.get(fld), sort_keys=True, ensure_ascii=False) == json.dumps(live.get(fld), sort_keys=True, ensure_ascii=False)
        print(f"{fld}: preserved={same}")
        if not same:
            print("  PRE :", json.dumps(pre.get(fld), ensure_ascii=False)[:300])
            print("  LIVE:", json.dumps(live.get(fld), ensure_ascii=False)[:300])

# em-dash scan of student-facing strings
def walk(o, path=""):
    hits=[]
    if isinstance(o, dict):
        for k,v in o.items():
            if k=="note":  # internal exempt
                continue
            hits += walk(v, path+"."+k)
    elif isinstance(o, list):
        for i,v in enumerate(o):
            hits += walk(v, path+f"[{i}]")
    elif isinstance(o, str):
        if "—" in o or "–" in o:
            hits.append((path, o))
    return hits
emd = walk(live)
print("\nEM/EN-DASH hits (excl note):", len(emd))
for p,s in emd:
    print("  ", p, "::", s[:120])

# HTML entity scan in plain-text-ish fields
import re
ent = re.findall(r"&[a-zA-Z]+;|&#\d+;", json.dumps(live, ensure_ascii=False))
print("\nHTML entities anywhere:", set(ent))
