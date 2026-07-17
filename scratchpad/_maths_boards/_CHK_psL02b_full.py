# -*- coding: utf-8 -*-
import json, re
live = json.load(open("_CHK_psL02b_live.json", encoding="utf-8"))
pd = live["practice_data"]
pre_all = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
# find pre entry for this id
ID="1a8441e6-115c-473e-a9b7-a2276e5b7faa"
pre=None
if isinstance(pre_all, list):
    for r in pre_all:
        if r.get("id")==ID: pre=r; break
elif isinstance(pre_all, dict):
    pre = pre_all.get(ID) or (pre_all.get("lessons") and next((r for r in pre_all["lessons"] if r.get("id")==ID), None))
print("pre found:", pre is not None, "| pre_all type:", type(pre_all).__name__,
      "len" , len(pre_all) if hasattr(pre_all,'__len__') else '')

findings=[]

# Proper multi-term box evaluator: pull the RHS expression right before '='
exprpat = re.compile(r'([-\d\.\s+\-−×x*÷/]+)=\s*$')
def ev(expr):
    e=expr.replace("×","*").replace("−","-").replace("÷","/").replace("x","*").strip()
    e=re.sub(r'\s+','',e)
    if not re.fullmatch(r'[-\d\.+*/]+', e): return None
    try: return eval(e)
    except: return None
def check(steps,path):
    for i,s in enumerate(steps):
        if "answer" not in s: continue
        pre_txt=(s.get("pre") or "")
        m=exprpat.search(pre_txt)
        if m:
            r=ev(m.group(1))
            if r is not None and abs(r-s["answer"])>1e-3:
                findings.append((f"{path}[{i}]", f"'{pre_txt.strip()}' -> {r} != {s['answer']}"))

pb=pd["problem_bank"]
for t in ["gold","bronze","silver"]:
    for idx,p in enumerate(pb[t]):
        check(p.get("guided_steps",[]), f"{t}[{idx}].guided_steps")
for t in ["gold","bronze","silver"]:
    check(pd["guided"]["teach"][t]["steps"], f"teach.{t}")
check(pd["guided"]["opener"]["steps"], "opener")
print("BOX ARITH mismatches:", findings)

# Preservation: compare untouched fields against pre-dump
if pre:
    prepd = pre.get("practice_data") or pre
    for fld in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(prepd.get(fld), sort_keys=True, ensure_ascii=False)
        b=json.dumps(pd.get(fld), sort_keys=True, ensure_ascii=False)
        print(f"PRESERVE {fld}: {'SAME' if a==b else 'CHANGED'}")
        if a!=b:
            print("   pre:", a[:200])
            print("   now:", b[:200])
    print("pre pd keys:", list(prepd.keys()))
