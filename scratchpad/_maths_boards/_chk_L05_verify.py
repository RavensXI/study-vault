import json, re
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
live = json.load(open(base+"_LIVE_L05.json", encoding="utf-8"))

# ---- Preservation vs pre-dump ----
pre = json.load(open(base+"_pre_dump_maths-aqa.json", encoding="utf-8"))
ID = "d2ed09e5-eea7-4e13-a9b6-2437ace7f664"
entry = None
if isinstance(pre, dict):
    # could be keyed by id or list under a key
    if ID in pre: entry = pre[ID]
    else:
        for k,v in pre.items():
            if isinstance(v, dict) and v.get("id")==ID: entry=v; break
            if isinstance(v, list):
                for it in v:
                    if isinstance(it,dict) and it.get("id")==ID: entry=it; break
elif isinstance(pre, list):
    for it in pre:
        if isinstance(it,dict) and it.get("id")==ID: entry=it; break
print("pre-dump entry found:", entry is not None)
if entry is not None:
    pdpre = entry.get("practice_data", entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        a = json.dumps(pdpre.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f"PRESERVE {f}: {'SAME' if a==b else 'CHANGED'}")
        if a!=b:
            print("  PRE :", a[:400])
            print("  LIVE:", b[:400])
    print("pre-dump top keys:", list(pdpre.keys()))

# ---- Em dash scan in student-facing strings ----
EM = "—"
hits=[]
def walk(o, path):
    if isinstance(o, dict):
        for k,v in o.items():
            if k=="note": continue  # internal exempt
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o): walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if EM in o: hits.append(path)
walk(live, "root")
print("EM DASH hits:", hits)

# ---- charts/svg present? ----
def find_fig(o, path, out):
    if isinstance(o,dict):
        if "chart" in o: out.append(path+".chart")
        for k,v in o.items(): find_fig(v,f"{path}.{k}",out)
    elif isinstance(o,list):
        for i,v in enumerate(o): find_fig(v,f"{path}[{i}]",out)
    elif isinstance(o,str) and "<svg" in o: out.append(path+"(svg)")
figs=[]; find_fig(live,"root",figs)
print("FIGURES:", figs if figs else "none")
