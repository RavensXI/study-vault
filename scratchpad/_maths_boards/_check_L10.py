import json, re

live = json.load(open(r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_maths-ocr_algebra-L10.json", encoding="utf-8"))
pre_all = json.load(open(r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_pre_dump_maths-ocr.json", encoding="utf-8"))

# find pre-dump entry for this lesson
lid = "dd0172cd-6a81-41c6-ae9b-98de9328eb77"
pre = None
if isinstance(pre_all, list):
    for row in pre_all:
        if row.get("id") == lid:
            pre = row.get("practice_data"); break
elif isinstance(pre_all, dict):
    # maybe keyed
    if lid in pre_all:
        pre = pre_all[lid].get("practice_data", pre_all[lid])
    else:
        for k,v in pre_all.items():
            if isinstance(v, dict) and v.get("id")==lid:
                pre = v.get("practice_data"); break
print("pre found:", pre is not None)
if pre:
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pre.get(f), sort_keys=True) == json.dumps(live.get(f), sort_keys=True)
        print(f"preserve {f}: {'SAME' if same else 'CHANGED'}")
    # method_card may be trimmed
    print("pre method_card keys:", list(pre.get("method_card",{}).keys()) if pre.get("method_card") else None)

# em dash scan in student-facing strings
def walk(o, path=""):
    hits=[]
    if isinstance(o, dict):
        for k,v in o.items():
            if k=="note":  # internal exempt
                continue
            hits+=walk(v, path+"/"+k)
    elif isinstance(o, list):
        for i,v in enumerate(o):
            hits+=walk(v, path+f"[{i}]")
    elif isinstance(o, str):
        if "—" in o:
            hits.append((path,o))
    return hits
ed = walk(live)
print("em dashes:", len(ed))
for p,s in ed: print("  ", p, s[:60])
