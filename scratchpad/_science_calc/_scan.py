import json,io,re
pd=json.load(io.open("_canon_pd.json",encoding="utf-8"))
def walk(o,p):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in("note","guided_skip_reason"):continue
            walk(v,p+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o):walk(v,p+"[%d]"%i)
    elif isinstance(o,str):
        if "—" in o: print("EMDASH",p,":",repr(o[:70]))
walk(pd,"pd")
def words(s): return len([w for w in s.replace("\("," ").replace("\)"," ").split() if w])
print("method_card.content words:",words(pd["method_card"]["content"]))
print("method_card.steps:",len(pd["method_card"]["steps"]))
