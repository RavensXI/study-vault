import json,io,re
live=json.load(open("_CHK_rpL06_live.json",encoding="utf-8"))["practice_data"]

# 1. em-dash scan in student-facing strings (exclude internal 'note' fields)
def walk(o,path=""):
    hits=[]
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            hits+=walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): hits+=walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o: hits.append(("EMDASH",path,o[:80]))
    return hits
emd=walk(live)
print("EM-DASH hits:",len(emd))
for h in emd: print("  ",h)

# 2. non-numeric box answers check
bad=[]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        for k,s in enumerate(p.get("guided_steps") or []):
            if "answer" in s and not isinstance(s["answer"],(int,float)):
                bad.append((f"{tier}[{i}].guided_steps[{k}]",s["answer"]))
for tier in ["bronze","silver","gold"]:
    t=live["guided"]["teach"].get(tier,{})
    for k,s in enumerate(t.get("steps",[])):
        if "answer" in s and not isinstance(s["answer"],(int,float)):
            bad.append((f"teach.{tier}[{k}]",s["answer"]))
print("NON-NUMERIC boxes:",bad)

# 3. preservation vs pre-dump
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
ID="4e8ba0ab-6dca-4615-98e2-2fac39408f5c"
def findpre(d):
    if isinstance(d,list):
        for e in d:
            if isinstance(e,dict) and e.get("id")==ID: return e
    if isinstance(d,dict):
        if ID in d: return d[ID]
        for e in d.values():
            if isinstance(e,dict) and e.get("id")==ID: return e
    return None
pe=findpre(pre)
print("PRE found:",pe is not None, "| pre-dump type:", type(pre).__name__, "len" , len(pre) if hasattr(pre,'__len__') else '')
if pe:
    ppd=pe.get("practice_data",pe)
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(ppd.get(f),ensure_ascii=False,sort_keys=True)
        b=json.dumps(live.get(f),ensure_ascii=False,sort_keys=True)
        print(f"  {f}: {'SAME' if a==b else 'CHANGED'}  (pre {len(str(ppd.get(f)))} chars / live {len(str(live.get(f)))} chars)")
