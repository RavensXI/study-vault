import json, re

LID = "55a5af04-f88a-4be7-b4c0-7f89c607e266"
live = json.load(open("_CHK_algL03_live.json", encoding="utf-8"))

# ---- em dash scan (student-facing) ----
EM = "—"
def walk(o, path):
    hits = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "note":  # internal exempt
                continue
            hits += walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            hits += walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if EM in o:
            hits.append(path)
    return hits
print("EM DASHES:", walk(live, "root"))

# ---- expect mapping for all MC problems ----
pb = live["problem_bank"]
issues = []
for tier in ["bronze","silver","gold"]:
    for idx, p in enumerate(pb[tier]):
        if p.get("input_type") != "multiple_choice":
            issues.append(f"{tier}[{idx}] not MC")
            continue
        opts = p["options"]
        sol = p["solutions"]
        if sol != [0]:
            issues.append(f"{tier}[{idx}] solutions={sol} (expected [0]?)")
        # duplicate options detection
        norm = [re.sub(r"\s","",o) for o in opts]
        if len(set(norm)) != len(norm):
            # find dup pairs
            dd = {}
            for i,n in enumerate(norm):
                dd.setdefault(n,[]).append(i)
            dups = {k:v for k,v in dd.items() if len(v)>1}
            issues.append(f"{tier}[{idx}] DUP OPTIONS {dups} disp={p['display']}")
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            if e is None: continue
            if not (0 <= e < len(opts)):
                issues.append(f"{tier}[{idx}] expect {e} out of range")
print("STRUCTURAL ISSUES:")
for i in issues: print(" ", i)

# ---- preservation vs pre-dump ----
pre = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
# find entry
entry = None
if isinstance(pre, dict):
    if LID in pre:
        entry = pre[LID]
    else:
        for k,v in pre.items():
            if isinstance(v, dict) and v.get("id")==LID:
                entry=v; break
elif isinstance(pre, list):
    for v in pre:
        if v.get("id")==LID: entry=v; break
print("PRE ENTRY FOUND:", entry is not None)
if entry is not None:
    ppd = entry.get("practice_data", entry)
    for field in ["related_videos","topic_links","worked_examples"]:
        a = json.dumps(ppd.get(field), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(field), sort_keys=True, ensure_ascii=False)
        print(f"  {field}: {'SAME' if a==b else 'CHANGED'}")
        if a!=b:
            print("    PRE :", a[:400])
            print("    LIVE:", b[:400])
    print("  PRE top keys:", list(ppd.keys()))
