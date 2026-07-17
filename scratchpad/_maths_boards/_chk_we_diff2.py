import json
ID="89689a46-7251-4c2a-900e-5fdc240dafd3"
live=json.load(open("_chk_gL01_live.json",encoding="utf-8"))["practice_data"]
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
entry=pre[ID] if isinstance(pre,dict) and ID in pre else next(v for v in (pre.values() if isinstance(pre,dict) else pre) if v.get("id")==ID)
pd=entry.get("practice_data",entry)
pwe=pd["worked_examples"]; lwe=live["worked_examples"]
for i,(p,l) in enumerate(zip(pwe,lwe)):
    for j,(ps,ls) in enumerate(zip(p["steps"],l["steps"])):
        if ps.get("label")!=ls.get("label"):
            print(f"we[{i}].steps[{j}].label: PRE={ps['label']!r} LIVE={ls['label']!r}")
        if ps.get("content")!=ls.get("content"):
            print(f"we[{i}].steps[{j}].content DIFF")
    if p.get("question")!=l.get("question"): print(f"we[{i}].question DIFF")
print("counts:",len(pwe),len(lwe))
