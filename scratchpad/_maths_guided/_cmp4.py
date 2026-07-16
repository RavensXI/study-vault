import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="68997180-8486-4551-ab42-0a1b98384336"
live=json.load(open("_live_L01.json",encoding="utf-8"))
dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
def locate(o):
    if isinstance(o,dict):
        if o.get("id")==ID: return o
        for v in o.values():
            r=locate(v)
            if r: return r
    if isinstance(o,list):
        for x in o:
            r=locate(x)
            if r: return r
    return None
pre=locate(dump)["practice_data"]
# normalize em dash to colon-ish and compare worked_examples labels
def norm(s): return s.replace(" — ", ": ")
pw=pre["worked_examples"]; lw=live["worked_examples"]
diffs=[]
for i,(a,b) in enumerate(zip(pw,lw)):
    for j,(sa,sb) in enumerate(zip(a["steps"],b["steps"])):
        if norm(sa["label"])!=sb["label"]:
            diffs.append((i,j,"label",sa["label"],sb["label"]))
        if sa["content"]!=sb["content"]:
            diffs.append((i,j,"content",sa["content"],sb["content"]))
    if a["question"]!=b["question"]: diffs.append((i,"q",a["question"],b["question"]))
    if a.get("difficulty")!=b.get("difficulty"): diffs.append((i,"diff"))
print("worked_examples non-emdash diffs:", diffs)

# scan all student-facing strings for em dash
import re
def scan(o,path=""):
    out=[]
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            out+=scan(v,path+"/"+k)
    elif isinstance(o,list):
        for i,x in enumerate(o):
            out+=scan(x,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o or "–" in o: out.append((path,o))
    return out
print("EM DASHES in live (excl note):", scan(live))

# check all box answers numeric
def boxes(o,path=""):
    bad=[]
    if isinstance(o,dict):
        if "answer" in o and not isinstance(o["answer"],(int,float)):
            bad.append((path,o["answer"]))
        for k,v in o.items(): bad+=boxes(v,path+"/"+k)
    elif isinstance(o,list):
        for i,x in enumerate(o): bad+=boxes(x,f"{path}[{i}]")
    return bad
print("NON-NUMERIC answers:", boxes(live))
