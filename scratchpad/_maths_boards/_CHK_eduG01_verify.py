import json, re

ID="112923c0-364e-4701-91d9-280e7859d6d3"
live=json.load(open("_CHK_eduG01_live.json",encoding="utf-8"))
pd=live["practice_data"]

# ---- preservation vs pre-dump ----
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# pre could be list of rows or dict keyed by id
row=None
if isinstance(pre,list):
    for r in pre:
        if r.get("id")==ID: row=r; break
elif isinstance(pre,dict):
    row=pre.get(ID) or (pre if pre.get("id")==ID else None)
print("pre row found:", row is not None)
if row:
    ppd=row.get("practice_data",row)
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'SAME' if a==b else 'CHANGED'}")
        if a!=b:
            print("  PRE:",a[:400])
            print("  NEW:",b[:400])

# ---- em dash scan in student-facing strings ----
def walk(o,path=""):
    out=[]
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue  # internal exempt
            out+=walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            out+=walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o or "–" in o:
            out.append((path,o))
    return out
dashes=walk(pd)
print("\nEM/EN DASHES:", len(dashes))
for p,s in dashes: print("  ",p,repr(s[:80]))

# ---- boundary check on bank guided_steps ----
print("\nBOUNDARY CHECK:")
for tier in ["bronze","silver","gold"]:
    for i,prob in enumerate(pd["problem_bank"][tier]):
        gs=prob.get("guided_steps")
        it=prob.get("input_type")
        if not gs:
            print(f"  {tier}[{i}] no guided_steps (input_type={it})")
            continue
        # locate phase
        boxidx=[j for j,s in enumerate(gs) if "answer" in s]
        phaseidx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not phaseidx:
            print(f"  {tier}[{i}] NO phase tag")
            continue
        ph=phaseidx[0]
        before_boxes=[j for j in boxidx if j<ph]
        at_after_boxes=[j for j in boxidx if j>=ph]
        flag=""
        if len(before_boxes)<1: flag+=" <1-before!"
        if len(at_after_boxes)<2: flag+=" <2-after!"
        print(f"  {tier}[{i}] boxes_before={len(before_boxes)} boxes_at/after={len(at_after_boxes)}{flag}")
