# -*- coding: utf-8 -*-
import json
ID="74e144eb-d320-44e4-afed-c9a263b3af36"
live=json.load(open("_CHK_graphsL05_LIVE.json",encoding="utf-8"))

# em dash sweep over student-facing strings (exclude internal 'note')
findings=[]
def walk(obj,path):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k=="note": continue
            walk(v,f"{path}.{k}")
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            walk(v,f"{path}[{i}]")
    elif isinstance(obj,str):
        if "—" in obj:
            findings.append(("EMDASH",path,obj[:80]))
walk(live,"root")

# preservation vs pre-dump
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
# find entry for this id
entry=None
if isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    elif "lessons" in pre:
        for l in pre["lessons"]:
            if l.get("id")==ID: entry=l.get("practice_data"); break
elif isinstance(pre,list):
    for l in pre:
        if l.get("id")==ID: entry=l.get("practice_data"); break
print("pre entry found:",entry is not None)
if entry is not None:
    for f in ["related_videos","topic_links","worked_examples"]:
        old=json.dumps(entry.get(f),sort_keys=True)
        new=json.dumps(live.get(f),sort_keys=True)
        print(f"PRESERVE {f}: {'SAME' if old==new else 'CHANGED'}")
        if old!=new:
            print("  OLD:",old[:300])
            print("  NEW:",new[:300])
    print("pre keys:",sorted(entry.keys()))
    print("live keys:",sorted(live.keys()))

print("\nEM DASH findings:",len(findings))
for f in findings: print(f)
