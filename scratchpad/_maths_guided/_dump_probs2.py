import json
pd=json.load(open("_live_algebra_L10.json",encoding="utf-8"))
pb=pd["problem_bank"]
out=[]
for t in ("bronze","silver","gold"):
    out.append("="*70); out.append("TIER "+t)
    for i,p in enumerate(pb[t]):
        out.append("-"*50)
        out.append(f"[{i}] input_type={p.get('input_type')} calc={p.get('calculator')}")
        out.append("DISPLAY: "+repr(p.get('display')))
        out.append("SOLUTIONS: "+repr(p.get('solutions')))
        out.append("HINT: "+repr(p.get('hint')))
open("_probs_dump.txt","w",encoding="utf-8").write("\n".join(out))
print("done")
