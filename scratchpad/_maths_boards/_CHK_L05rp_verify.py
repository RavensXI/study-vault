import json, re, math

live = json.load(open("_CHK_L05rp_live.json", encoding="utf-8"))
pd = live["practice_data"]

# ---- preservation vs pre-dump ----
predump = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
# find matching entry
ID = "ddbb6863-36ab-4898-8090-16df440a9d85"
pre = None
if isinstance(predump, list):
    for e in predump:
        if e.get("id") == ID:
            pre = e; break
elif isinstance(predump, dict):
    pre = predump.get(ID) or (predump.get("practice_data") and predump)
print("predump type", type(predump).__name__, "keys" , (list(predump.keys())[:5] if isinstance(predump,dict) else len(predump)))
if pre:
    ppd = pre.get("practice_data", pre)
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(ppd.get(f), sort_keys=True, ensure_ascii=False) == json.dumps(pd.get(f), sort_keys=True, ensure_ascii=False)
        print(f"PRESERVE {f}: {'OK' if same else 'CHANGED'}")
        if not same:
            print("  pre:", json.dumps(ppd.get(f), ensure_ascii=False)[:300])
            print("  now:", json.dumps(pd.get(f), ensure_ascii=False)[:300])
else:
    print("NO PREDUMP ENTRY FOUND for", ID)

# ---- em dash scan in student-facing ----
def walk(o, path=""):
    out=[]
    if isinstance(o, dict):
        for k,v in o.items():
            if k=="note": continue
            out+=walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            out+=walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if "—" in o or "–" in o:
            out.append((path,o))
    return out
dashes = walk(pd)
print("EM/EN DASHES:", len(dashes))
for p,s in dashes: print("  ",p, repr(s[:80]))
