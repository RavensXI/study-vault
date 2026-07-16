import json,re
pd=json.load(open("_live_algebra_L10.json",encoding="utf-8"))
pb=pd["problem_bank"]
def scan(obj,path):
    hits=[]
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k in ("chart",):
                hits.append((path+"."+k,"CHART"))
            if isinstance(v,str) and "<svg" in v:
                hits.append((path+"."+k,"SVG"))
            hits+=scan(v,path+"."+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            hits+=scan(v,f"{path}[{i}]")
    return hits
allhits=scan(pd,"pd")
for h in allhits: print(h[1],h[0])
print("---TIERS---")
for t in ("bronze","silver","gold"):
    probs=pb.get(t,[])
    print(t,len(probs))
