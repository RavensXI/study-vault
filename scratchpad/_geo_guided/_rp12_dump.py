import json,os
d=os.path.dirname(os.path.abspath(__file__))
pd=json.load(open(os.path.join(d,"_rp12_live.json"),encoding="utf-8"))
out=[]
def w(s=""): out.append(s)
w("EXAM_CONTEXT: "+json.dumps(pd.get("exam_context"),ensure_ascii=False))
pb=pd["problem_bank"]
for k,v in pb.items():
    if not isinstance(v,list):
        w("%s = %s"%(k,json.dumps(v,ensure_ascii=False)))
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        w("="*70)
        w("%s[%d] type=%s"%(t,i,p.get("input_type")))
        w("  display: "+str(p.get("display")))
        w("  image: "+str(p.get("image")))
        w("  ruler: "+json.dumps(p.get("ruler"),ensure_ascii=False))
        w("  options: "+json.dumps(p.get("options"),ensure_ascii=False))
        w("  solutions: "+json.dumps(p.get("solutions"),ensure_ascii=False))
        w("  hint: "+str(p.get("hint")))
        for j,m in enumerate(p.get("misconceptions") or []):
            w("  misc[%d]: %s"%(j,json.dumps(m,ensure_ascii=False)))
        for j,s in enumerate(p.get("guided_steps") or []):
            w("  gs[%d]: %s"%(j,json.dumps(s,ensure_ascii=False)))
        for kk in p:
            if kk not in ("input_type","display","image","ruler","options","solutions","hint","misconceptions","guided_steps"):
                w("  +%s: %s"%(kk,json.dumps(p[kk],ensure_ascii=False)[:300]))
open(os.path.join(d,"_rp12_dump.txt"),"w",encoding="utf-8").write("\n".join(out))
print(len(out))
