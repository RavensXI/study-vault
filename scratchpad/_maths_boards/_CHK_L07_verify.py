import json, re

live = json.load(open("_CHK_L07_live.json", encoding="utf-8"))

# 1. em dash scan across all student-facing strings
def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            # note fields exempt
            if k == "note":
                continue
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o

emdash = []
for p,s in walk(live):
    if "—" in s or "–" in s:
        emdash.append((p,s))
print("=== EM/EN DASH HITS ===")
for p,s in emdash:
    print(p, repr(s[:80]))
print("count", len(emdash))

# 2. preservation vs pre-dump
try:
    pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
except Exception as e:
    print("predump load err", e)
    pre = None

if pre is not None:
    # find entry for this lesson id
    ID = "e16ccba1-6dc0-4321-835b-98ec18acce00"
    entry = None
    if isinstance(pre, dict):
        if ID in pre:
            entry = pre[ID]
        else:
            for k,v in pre.items():
                if isinstance(v, dict) and (v.get("id")==ID):
                    entry = v; break
    elif isinstance(pre, list):
        for v in pre:
            if isinstance(v,dict) and v.get("id")==ID:
                entry = v; break
    print("=== PREDUMP ENTRY FOUND:", entry is not None)
    if entry is not None:
        pd_pre = entry.get("practice_data", entry)
        for fld in ["related_videos","topic_links","worked_examples"]:
            a = json.dumps(pd_pre.get(fld), sort_keys=True, ensure_ascii=False)
            b = json.dumps(live.get(fld), sort_keys=True, ensure_ascii=False)
            print(f"[{fld}] preserved:", a==b)
            if a!=b:
                print("  PRE:", a[:300])
                print("  NOW:", b[:300])
        print("predump top keys:", list(pd_pre.keys()))
