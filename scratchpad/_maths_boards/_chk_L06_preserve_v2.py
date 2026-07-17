# -*- coding: utf-8 -*-
import json, sys
io=sys.stdout
live = json.load(open("_chk_L06_live_v2.json", encoding="utf-8"))
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))

# pre may be dict keyed by id or key, or a list
ID="0a7ff82d-058f-480c-86fe-63a16ac98dc5"
entry=None
if isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    elif "algebra-L06" in pre: entry=pre["algebra-L06"]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID:
                entry=v; break
            if isinstance(v,dict) and ("problem_bank" in v or "practice_data" in v):
                pass
        if entry is None:
            io.write("pre keys sample: "+str(list(pre.keys())[:10])+"\n")
elif isinstance(pre,list):
    for v in pre:
        if v.get("id")==ID: entry=v;break
if entry is None:
    io.write("NO pre entry found automatically\n"); sys.exit()
# entry could wrap practice_data
ppd = entry.get("practice_data", entry)
io.write("pre practice_data top keys: "+str(list(ppd.keys()))+"\n")
for f in ["related_videos","topic_links","worked_examples"]:
    a=json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)
    b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    io.write(f"{f}: {'SAME' if a==b else 'DIFFERENT'}\n")
    if a!=b:
        io.write("  PRE : "+a[:400]+"\n")
        io.write("  LIVE: "+b[:400]+"\n")
# also report pre problem count vs live for sanity
for tier in ["bronze","silver","gold"]:
    pn=len(ppd.get("problem_bank",{}).get(tier,[])) if "problem_bank" in ppd else "?"
    ln=len(live["problem_bank"][tier])
    io.write(f"{tier}: pre={pn} live={ln}\n")
