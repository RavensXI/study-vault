import json, re

base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
ID = "e0a5f715-f25c-4afd-b0c1-c71ea7f743e3"

live = json.load(open(base+"_CHK_L13_live.json", encoding="utf-8"))

# find pre-dump entry
pre = json.load(open(base+"_pre_dump_maths-aqa.json", encoding="utf-8"))
print("pre-dump type:", type(pre))
entry = None
if isinstance(pre, list):
    for e in pre:
        if e.get("id") == ID:
            entry = e; break
elif isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID]
    else:
        for k,v in pre.items():
            if isinstance(v, dict) and v.get("id")==ID:
                entry = v; break
print("found pre entry:", entry is not None)
if entry is not None:
    pd_pre = entry.get("practice_data", entry)
    print("pre keys:", list(pd_pre.keys()) if isinstance(pd_pre,dict) else "?")
    for f in ["related_videos","topic_links","worked_examples"]:
        a = json.dumps(pd_pre.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f"  {f}: {'SAME' if a==b else 'DIFF'}")
        if a!=b:
            print("    PRE:", a[:400])
            print("    LIVE:", b[:400])

# em dash scan across all student-facing strings
emdash = "—"
hits = []
def walk(o, path):
    if isinstance(o, dict):
        for k,v in o.items():
            if k == "note": continue
            walk(v, path+"."+k)
    elif isinstance(o, list):
        for i,v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if emdash in o:
            hits.append((path, o))
walk(live, "root")
print("\nEM DASH hits:", len(hits))
for p,s in hits:
    print("  ", p, repr(s[:80]))

# check external refs in SVG / scripts
svg_issues=[]
def walk2(o, path):
    if isinstance(o, dict):
        for k,v in o.items(): walk2(v, path+"."+k)
    elif isinstance(o, list):
        for i,v in enumerate(o): walk2(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if "<svg" in o:
            for bad in ["http://","https://","<script","xlink:href","url("]:
                if bad in o:
                    svg_issues.append((path, bad))
walk2(live, "root")
print("\nSVG external-ref issues:", svg_issues)
