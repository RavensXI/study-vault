# -*- coding: utf-8 -*-
import json
ID="ca643606-adf3-40c8-a4dd-8dfb8c25a21f"
live=json.load(open("_MYCHK_live.json",encoding="utf-8"))
dump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
entry=[e for e in dump if e.get("id")==ID][0]
pre=entry["practice_data"]
pw=pre["worked_examples"]; lw=live["worked_examples"]
for i,(a,b) in enumerate(zip(pw,lw)):
    print(f"WE[{i}] question same:", a["question"]==b["question"])
    for j,(sa,sb) in enumerate(zip(a["steps"],b["steps"])):
        if sa.get("content")!=sb.get("content"):
            print(f"  step{j} CONTENT DIFF:\n    PRE:{sa.get('content')}\n    LIVE:{sb.get('content')}")
        if sa.get("label")!=sb.get("label"):
            print(f"  step{j} label: PRE={sa.get('label')!r} LIVE={sb.get('label')!r}")

# em-dash sweep across all student-facing strings
print("\n=== EM DASH / en-dash sweep (student-facing) ===")
import re
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue  # internal exempt
            walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o: print("EM DASH at",path,":",o[:80])
hits=[]
walk(live)
print("(none above = clean)")
