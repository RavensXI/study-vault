import json,os,re
d=os.path.dirname(os.path.abspath(__file__))
live=json.load(open(os.path.join(d,"_iv12_live.json"),encoding="utf-8"))
pre=json.load(open(os.path.join(d,"_iv12_pre.json"),encoding="utf-8"))["pd"]
def walk(o,p=""):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,p+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,p+"[%d]"%i)
    elif isinstance(o,str):
        if re.search(r"\bmarks?\b",o): yield p,o
for p,s in walk(live): print("LIVE",p,":",s[:200])
print("=== exam_context pre:", json.dumps(pre.get("exam_context"),ensure_ascii=False))
print("=== exam_context live:", json.dumps(live.get("exam_context"),ensure_ascii=False))
# worked_examples diff
import difflib
a=json.dumps(pre.get("worked_examples"),ensure_ascii=False,indent=1).splitlines()
b=json.dumps(live.get("worked_examples"),ensure_ascii=False,indent=1).splitlines()
for l in difflib.unified_diff(a,b,lineterm="",n=0): print(l)
print("=== method_card pre:", json.dumps(pre.get("method_card"),ensure_ascii=False)[:1500])
