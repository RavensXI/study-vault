# -*- coding: utf-8 -*-
import json
PRE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_pre_dump_maths-ocr.json"
LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK_rpL02_live.json"
ID = "330ee5b7-1c7b-4990-861a-b9de40f4c2a9"

pre = json.load(open(PRE, encoding="utf-8"))
live = json.load(open(LIVE, encoding="utf-8"))["practice_data"]

# pre may be list or dict
entry = None
if isinstance(pre, list):
    for r in pre:
        if r.get("id")==ID or r.get("slug")=="percentages-and-compound-change":
            entry = r; break
elif isinstance(pre, dict):
    if ID in pre: entry = pre[ID]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and (v.get("id")==ID or v.get("slug")=="percentages-and-compound-change"):
                entry = v; break
print("pre type:", type(pre).__name__, "| found entry:", entry is not None)
if entry is None:
    # show structure
    if isinstance(pre,list):
        print("list len", len(pre), "sample keys", list(pre[0].keys())[:10] if pre else None)
    else:
        print("dict keys sample", list(pre.keys())[:5])
    raise SystemExit

ppd = entry.get("practice_data", entry)
import json as J
for f in ("related_videos","topic_links","worked_examples"):
    a = J.dumps(ppd.get(f), sort_keys=True, ensure_ascii=False)
    b = J.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
    print(f"{f}: {'UNCHANGED' if a==b else 'CHANGED'}")
    if a!=b:
        print("  PRE :", a[:400])
        print("  LIVE:", b[:400])
