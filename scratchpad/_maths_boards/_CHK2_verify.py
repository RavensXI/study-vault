# -*- coding: utf-8 -*-
import json, io

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK2_eduqasL14_live.json"
PRE  = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_pre_dump_maths-eduqas.json"
ID   = "15c509ec-bdaf-466b-b9e4-1f1803fc4b3d"

live = json.load(io.open(LIVE, encoding="utf-8"))
pd = live["practice_data"]

# dump practice_data alone for validator
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK2_pd_only.json"
json.dump(pd, io.open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# find pre-dump entry
pre = json.load(io.open(PRE, encoding="utf-8"))
def find_entry(pre, ID):
    if isinstance(pre, list):
        for e in pre:
            if isinstance(e, dict) and e.get("id") == ID:
                return e
    elif isinstance(pre, dict):
        if ID in pre:
            return pre[ID]
        for k,v in pre.items():
            if isinstance(v, dict) and v.get("id")==ID:
                return v
    return None
pe = find_entry(pre, ID)
print("pre entry found:", pe is not None)
if pe is not None:
    ppd = pe.get("practice_data", pe)
    for f in ("related_videos","topic_links","worked_examples"):
        a = json.dumps(ppd.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(pd.get(f), sort_keys=True, ensure_ascii=False)
        print(f, "PRESERVED" if a==b else "CHANGED")
        if a!=b:
            print("  PRE:", a[:400])
            print("  NOW:", b[:400])
    # tier sizes
    for tier in ("bronze","silver","gold"):
        pn = len((ppd.get("problem_bank") or {}).get(tier) or [])
        nn = len((pd.get("problem_bank") or {}).get(tier) or [])
        print("tier", tier, "pre=",pn,"now=",nn)
