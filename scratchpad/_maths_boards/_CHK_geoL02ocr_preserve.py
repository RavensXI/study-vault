# -*- coding: utf-8 -*-
import json
ID="7134e062-5209-4de5-894e-c315dc3ee9d0"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre may be dict keyed by id, or list of rows
entry=None
if isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and (v.get("id")==ID or v.get("slug")=="area-and-perimeter"):
                entry=v; break
elif isinstance(pre,list):
    for r in pre:
        if r.get("id")==ID or r.get("slug")=="area-and-perimeter":
            entry=r; break
print("found entry:",entry is not None, "type:",type(entry).__name__)
if entry is None:
    print("KEYS sample:", list(pre.keys())[:5] if isinstance(pre,dict) else "list len "+str(len(pre)))
    raise SystemExit
pd_pre = entry.get("practice_data", entry)
live=json.load(open("_CHK_geoL02ocr_live.json",encoding="utf-8"))
for f in ["related_videos","topic_links","worked_examples","method_card"]:
    a=pd_pre.get(f); b=live.get(f)
    same = json.dumps(a,sort_keys=True,ensure_ascii=False)==json.dumps(b,sort_keys=True,ensure_ascii=False)
    print(f"{f}: preserved={same}")
    if not same:
        print("  PRE :",json.dumps(a,ensure_ascii=False)[:600])
        print("  LIVE:",json.dumps(b,ensure_ascii=False)[:600])
# tier sizes / solutions / input_type / calculator preserved
pbp=pd_pre.get("problem_bank",{}); pbl=live.get("problem_bank",{})
for t in ["bronze","silver","gold"]:
    lp=pbl.get(t,[]); pp=pbp.get(t,[])
    print(f"{t}: pre {len(pp)} live {len(lp)}")
    for i in range(min(len(pp),len(lp))):
        if pp[i].get("solutions")!=lp[i].get("solutions"):
            print(f"  {t}[{i}] SOLUTION CHANGED pre={pp[i].get('solutions')} live={lp[i].get('solutions')}")
        if pp[i].get("input_type")!=lp[i].get("input_type"):
            print(f"  {t}[{i}] input_type changed")
        if pp[i].get("calculator")!=lp[i].get("calculator"):
            print(f"  {t}[{i}] calculator changed pre={pp[i].get('calculator')} live={lp[i].get('calculator')}")
