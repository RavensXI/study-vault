import json, io
live=json.load(io.open("_chk02_live.json",encoding="utf-8"))
pb=live["problem_bank"]
bad=[]
tokens=["\\(","\\)","\\frac","\\cup","\\cap","$"]
def haslatex(s):
    return any(t in s for t in tokens)
for tier in ["bronze","silver","gold"]:
    for pi,p in enumerate(pb[tier]):
        if haslatex(p.get("hint","")): bad.append(f"{tier}[{pi}].hint LaTeX")
        for si,s in enumerate(p.get("guided_steps",[])):
            for f in ["pre","post","hint"]:
                if haslatex(str(s.get(f,""))): bad.append(f"{tier}[{pi}].gs[{si}].{f} LaTeX")
print("plaintext LaTeX issues:", bad if bad else "none")
for tier in ["bronze","silver","gold"]:
    seen={}
    for pi,p in enumerate(pb[tier]):
        key=json.dumps(p["solutions"])
        seen.setdefault(key,[]).append(pi)
    dups={k:v for k,v in seen.items() if len(v)>1}
    if dups: print(f"DUP solutions {tier}: {dups}")
print("done")
