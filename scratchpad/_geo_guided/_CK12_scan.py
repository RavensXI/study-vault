import json,re
live=json.load(open('_CK12_live.json',encoding='utf-8'))
out=[]
pb=live["problem_bank"]
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        gs=p.get("guided_steps")
        if not gs: out.append("%s[%d] NO guided_steps skip=%s"%(t,i,p.get("guided_skip_reason")))
        else:
            boxes=[s for s in gs if "answer" in s]
            ph=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
            after=len([s for s in gs[ph[0]:] if "answer" in s]) if ph else -1
            before=len([s for s in gs[:ph[0]] if "answer" in s]) if ph else -1
            bad=[a["answer"] for a in boxes if not isinstance(a["answer"],(int,float))]
            first=gs[0]
            out.append("%s[%d] boxes=%d phase@%s before=%d after=%d nonnum=%s"%(t,i,len(boxes),ph,before,after,bad))
            if gs[-1].get("done") is None and "answer" in gs[-1]: out.append("   last box no done note")
        for m in p.get("misconceptions") or []:
            if "check" in m: out.append("   %s[%d] SURVIVING check=%s"%(t,i,m["check"]))
            if "expect" not in m: out.append("   %s[%d] missing expect"%(t,i))
# em dash scan
def walk(o,path=""):
    if isinstance(o,str):
        if "—" in o or "–" in o: out.append("EMDASH at %s: %s"%(path,o[:80]))
    elif isinstance(o,dict):
        for k,v in o.items(): walk(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): walk(v,path+"[%d]"%j)
walk(live)
open('_CK12_scan.txt','w',encoding='utf-8').write("\n".join(out))
print("\n".join(out))
