import json, io
live=json.load(io.open("_live_graphs-L01.json",encoding="utf-8"))["practice_data"]
pre=json.load(io.open("_pre_dump_maths-ocr.json",encoding="utf-8"))
ID="89689a46-7251-4c2a-900e-5fdc240dafd3"
def findpre(pre):
    if isinstance(pre,dict):
        if pre.get("id")==ID or pre.get("lesson_id")==ID: return pre
        for v in pre.values():
            r=findpre(v)
            if r: return r
    elif isinstance(pre,list):
        for v in pre:
            r=findpre(v)
            if r: return r
    return None
pe=findpre(pre); ppd=pe.get("practice_data",pe)
ppb=ppd["problem_bank"]; lpb=live["problem_bank"]
out=io.open("_cc.txt","w",encoding="utf-8")
def P(*a): print(*a,file=out)
for t,i in [("silver",4),("silver",5)]:
    P("="*50); P(f"{t}[{i}]")
    P(" PRE display:", ppb[t][i].get("display"))
    P(" LIVE display:", lpb[t][i].get("display"))
    P(" PRE sol:", ppb[t][i].get("solutions"), " LIVE sol:", lpb[t][i].get("solutions"))
# duplicate check within each live tier
P("\n### live within-tier solution duplicates ###")
for t in ["bronze","silver","gold"]:
    sols=[tuple(p.get("solutions",[])) for p in lpb[t]]
    P(t, sols)
    seen={}
    for idx,s in enumerate(sols):
        seen.setdefault(s,[]).append(idx)
    for s,idxs in seen.items():
        if len(idxs)>1: P("  DUP",s,"at",idxs)
P("\n### worked_examples PRE ###")
P(json.dumps(ppd.get("worked_examples"),ensure_ascii=False,indent=1))
P("\n### worked_examples LIVE ###")
P(json.dumps(live.get("worked_examples"),ensure_ascii=False,indent=1))
out.close(); print("ok")
