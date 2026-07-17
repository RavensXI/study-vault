# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_maths-aqa_algebra-L11.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []
def ck(cond, msg):
    if not cond: errs.append(msg)

# 1. final guided_steps box lands on the stored solution (single_value walks)
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        if gs:
            boxes = [s for s in gs if s.get("answer") is not None]
            sol = p["solutions"][0]
            ck(boxes[-1]["answer"] == sol, f"{tier}[{i}] last box {boxes[-1]['answer']} != sol {sol}")
            # boundary
            sub = [j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
            live_after = sum(1 for s in gs[sub[0]:] if s.get("answer") is not None) if sub else 0
            ck(bool(sub), f"{tier}[{i}] no substitute phase")
            ck(live_after>=2, f"{tier}[{i}] live_after={live_after}")

# 2. MC expects: in range 1..3, != correct idx, print option mapping
print("=== MC expect -> option mapping (eyeball) ===")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")!="multiple_choice": continue
        corr = p["solutions"][0]
        for m in p["misconceptions"]:
            e = m["expect"]
            ck(isinstance(e,int) and 0<=e<len(p["options"]), f"{tier}[{i}] expect {e} out of range")
            ck(e!=corr, f"{tier}[{i}] expect==correct idx {e}")
            opt = p["options"][e] if isinstance(e,int) and 0<=e<len(p["options"]) else "?"
            print(f"{tier}[{i}] {m['pattern']:20s} expect={e} -> {opt}")

# 3. single_value expects != solution
print("=== single_value expects ===")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")=="single_value":
            sol=p["solutions"][0]
            for m in p["misconceptions"]:
                ck(m["expect"]!=sol, f"{tier}[{i}] sv expect==sol")
                print(f"{tier}[{i}] {m['pattern']} expect={m['expect']} (sol {sol})")

# 4. teach & opener boxes recompute (independent)
def boxes(steps): return [s for s in steps if s.get("answer") is not None]
op = boxes(pd["guided"]["opener"]["steps"])
ck([b["answer"] for b in op]==[3,20], "opener boxes")
tb = boxes(pd["guided"]["teach"]["bronze"]["steps"]); ck([b["answer"] for b in tb]==[15,5,16,19],"teach bronze")
ts = boxes(pd["guided"]["teach"]["silver"]["steps"]); ck([b["answer"] for b in ts]==[8,-4,5,15],"teach silver")
tgd= boxes(pd["guided"]["teach"]["gold"]["steps"]); ck([b["answer"] for b in tgd]==[25,36,5,11],"teach gold")
ck(len(tb)>=4 and len(ts)>=4 and len(tgd)>=4,"teach box counts")

# arithmetic re-derivation
ck(8+4*3==20 and 4*3==12,"opener money")
ck(3*4+4==16 and 3*5+4==19,"teach bronze arith")
ck(5-2*(-5)==15,"teach silver arith")
ck(5**2==25 and 6**2==36,"teach gold arith")
ck(20+7==27 and 4*6==24 and 4*7==28,"S7 arith")
ck(7**2==49 and 8**2==64,"G4 arith")

# 5. no duplicate solutions among single_value within a tier
for tier in ("bronze","silver","gold"):
    sv=[tuple(p["solutions"]) for p in pb[tier] if p.get("input_type")=="single_value"]
    ck(len(sv)==len(set(sv)), f"{tier} dup single_value sols")

print("\n"+("ALL CHECKS PASS" if not errs else "ERRORS:\n"+"\n".join(errs)))
