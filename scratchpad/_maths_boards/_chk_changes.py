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
            r=findpre(v);
            if r: return r
    return None
pe=findpre(pre); ppd=pe.get("practice_data",pe)
ppb=ppd["problem_bank"]; lpb=live["problem_bank"]
for t,i in [("bronze",1),("bronze",2),("bronze",4),("silver",4),("silver",5)]:
    print("="*50)
    print(f"{t}[{i}]")
    print(" PRE display:", ppb[t][i].get("display"))
    print(" LIVE display:", lpb[t][i].get("display"))
    print(" PRE sol:", ppb[t][i].get("solutions"), " LIVE sol:", lpb[t][i].get("solutions"))
print("\n\n### worked_examples PRE ###")
print(json.dumps(ppd.get("worked_examples"),ensure_ascii=False,indent=1)[:2000])
print("\n### worked_examples LIVE ###")
print(json.dumps(live.get("worked_examples"),ensure_ascii=False,indent=1)[:2000])
