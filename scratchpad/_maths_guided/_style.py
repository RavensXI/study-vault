import json,re
live=json.load(open("_live_geometry-L06.json",encoding="utf-8"))
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue  # internal exempt
            yield from walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            yield from walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        yield path,o
emcount=0
for p,s in walk(live):
    if "—" in s or "–" in s:
        print("EM/EN DASH:",p,repr(s)); emcount+=1
    if "&" in s and re.search(r"&[a-zA-Z]+;|&#",s):
        print("HTML ENTITY:",p,repr(s))
print("emdash count:",emcount)
# check hint fields plain (no latex/html)
for tier,arr in live["problem_bank"].items():
    if not isinstance(arr,list): continue
    for i,p in enumerate(arr):
        h=p.get("hint","")
        if "\(" in h or "<" in h: print("HINT not plain",tier,i,h)
        # numeric answers
        for j,st in enumerate(p.get("guided_steps",[])):
            if "answer" in st and not isinstance(st["answer"],(int,float)):
                print("NON-NUMERIC answer",tier,i,j,st["answer"])
print("style scan done")
