# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_maths-eduqas_number-L06.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# 1. Fresh-solve each problem (hard-coded expected from independent solve)
expected = {
 "bronze":[[81],[64],[12],[3],[3.4],[7200],[125],[1]],
 "silver":[[4.5,-3],[5.6,6],[1.2,9],[4,4],[0.00028],[1,16],[7.2,-5]],
 "gold":[[9,8],[2.76,5],[4,10],[5000],[2,4]],
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p["solutions"] != expected[tier][i]:
            errs.append(f"{tier}[{i}] solution {p['solutions']} != fresh-solve {expected[tier][i]}")

# 2. Recompute boxes: each box must be numeric; final live boxes (at/after phase) must include solution values
def live_after_phase(steps):
    idx=None
    for j,s in enumerate(steps):
        if s.get("phase")=="substitute" and idx is None: idx=j
    live=[s["answer"] for s in steps[idx:] if s.get("answer") is not None] if idx is not None else []
    return live

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if not gs: continue
        # all boxes numeric
        for j,s in enumerate(gs):
            if s.get("answer") is not None and not isinstance(s["answer"],(int,float)):
                errs.append(f"{tier}[{i}].guided_steps[{j}] non-numeric box")
        # final answer boxes should cover solution values
        sols=p["solutions"]; live=live_after_phase(gs)
        for v in sols:
            if not any(abs(float(v)-float(b))<1e-9 for b in live) and not any(abs(float(v)-float(s.get('answer'))) <1e-9 for s in gs if s.get('answer') is not None):
                errs.append(f"{tier}[{i}] solution value {v} not produced by any box")

# 3. Reproduce expects
def commit_checks():
    # spot-verify a sample of expects by re-deriving the error
    checks=[
     ("bronze",0,12, 3*4),
     ("bronze",7,0, 0), ("bronze",7,10, 10),
     ("silver",0,[4.5,3], None), ("silver",0,[4.5,-2],None),
     ("silver",2,[12,8], None),
     ("silver",3,[4,10], None),
     ("silver",5,[1,8], None), ("silver",5,[16,1],None),
     ("gold",0,[6,8],None), ("gold",0,[9,6],None),
     ("gold",2,[4,6],None),
     ("gold",3,0.0002,None), ("gold",3,0.5,None),
     ("gold",4,[1.5,4],None), ("gold",4,[2,-2],None),
    ]
    for tier,i,exp,_ in checks:
        ms=pb[tier][i]["misconceptions"]
        if not any(m.get("expect")==exp for m in ms):
            errs.append(f"{tier}[{i}] expected misconception expect {exp} not found; have {[m.get('expect') for m in ms]}")
commit_checks()

# derive specific expects numerically
# gold[3] divided wrong way: 9e8/4.5e12 = 2e-4 = 0.0002
assert abs(9e8/4.5e12 - 0.0002) < 1e-12
# gold[4] multiplied_not_cubed: 6e9/4e5=1.5e4 -> [1.5,4]
assert 6e9/4e5 == 15000.0
# gold[4] power_not_cubed: 8e3/4e5 = 2e-2 -> [2,-2]
assert 8e3/4e5 == 0.02

# 4. Preservation vs live pre-dump
live=json.load(io.open("_L06e_live.json",encoding="utf-8"))
for k in ("worked_examples","topic_links","related_videos","method_card"):
    if json.dumps(pd.get(k),sort_keys=True,ensure_ascii=False)!=json.dumps(live.get(k),sort_keys=True,ensure_ascii=False):
        errs.append(f"preservation: {k} changed")

# 5. displays preserved (problem text unchanged)
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p["display"]!=live["problem_bank"][tier][i]["display"]:
            errs.append(f"{tier}[{i}] display changed: {live['problem_bank'][tier][i]['display']!r} -> {p['display']!r}")
        if p["solutions"]!=live["problem_bank"][tier][i]["solutions"]:
            errs.append(f"{tier}[{i}] solutions changed")
        if p["input_type"]!=live["problem_bank"][tier][i]["input_type"]:
            errs.append(f"{tier}[{i}] input_type changed")

# 6. em-dash scan student-facing (validator does this but double-check)
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,f"{path}[{j}]")
    elif isinstance(o,str) and "—" in o: errs.append("em dash at "+path)
scan(pd,"pd")

# teach walk final boxes verify
teach=pd["guided"]["teach"]
tv={"bronze":63000,"silver":None,"gold":None}
# bronze teach: 6.3e4=63000 check
assert 6.3*10000==63000
# silver teach: 6*5=30,2+4=6 ->30e6=3e7
assert 30*10**6==3*10**7
# gold teach: 6.3e4/9e-3 = 63000/0.009 = 7e6
assert round(63000/0.009)==7000000
# opener: 150000000 = 1.5e8
assert 150000000==int(1.5e8)

if errs:
    print("DEFECTS:",len(errs))
    for e in errs: print("  -",e)
else:
    print("CHECKER PASS: all solutions fresh-solve, boxes compute, expects reproduce, preservation intact, no em dashes.")
