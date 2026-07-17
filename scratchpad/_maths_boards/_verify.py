import json, re
pd=json.load(open("lesson_geometry-L01.json",encoding="utf-8"))
def val(opt):
    m=re.findall(r'-?\d+', opt)
    return int(m[0]) if m else None
pb=pd["problem_bank"]
bad=0
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        opts=[val(o) for o in p["options"]]
        sol=p["solutions"][0]
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is None: continue
            if e==sol:
                print("EXPECT==SOL",tier,i,m["pattern"]); bad+=1
            if not (0<=e<len(opts)):
                print("EXPECT OOR",tier,i,m["pattern"]); bad+=1
print("expect checks done, bad=",bad)
# opener/teach boxes recompute sanity print
g=pd["guided"]
print("opener answers:",[s.get("answer") for s in g["opener"]["steps"] if s.get("answer") is not None])
for t in ("bronze","silver","gold"):
    print("teach",t,[s.get("answer") for s in g["teach"][t]["steps"] if s.get("answer") is not None])
