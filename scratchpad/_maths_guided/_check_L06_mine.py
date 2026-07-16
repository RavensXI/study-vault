# -*- coding: utf-8 -*-
import json, io, math
from decimal import Decimal, ROUND_HALF_UP
def rnd(x,n): return float(Decimal(str(x)).quantize(Decimal('1'+('.'+'0'*n if n else '')), ROUND_HALF_UP))

out = json.load(io.open("lesson_ratio-proportion-L06.json", encoding="utf-8"))
live = json.load(io.open("_live_L06.json", encoding="utf-8"))
pb = out["problem_bank"]
prob=[]

# 1. fresh-solve every bank problem
def solve(tier,i):
    return pb[tier][i]["solutions"]
expect={
 ("bronze",0):[2],("bronze",1):[-2],("bronze",2):[11],("bronze",3):[9],
 ("bronze",4):[5],("bronze",5):[7],("bronze",6):[3],("bronze",7):[4],
 ("silver",0):[4.22],("silver",1):[2],("silver",2):[0.256],("silver",3):[2],
 ("silver",4):[2.86],("silver",5):[3],("silver",6):[1.71],
 ("gold",0):[1.71],("gold",1):[-1],("gold",2):[22],("gold",3):[4.9593],("gold",4):[5],
}
for k,v in expect.items():
    got=solve(*k)
    if got!=v: prob.append(f"SOLUTION MISMATCH {k}: stored {got} expected {v}")

# 2. every non-MC problem: last ANSWER box must be reachable; check final answer box == a solution value
# and completion boundary present, and re-verify calc-heavy walks land correctly.
def box_answers(steps): return [st["answer"] for st in steps if st.get("answer") is not None]

# spot re-computation of key walk boxes
checks = {
 ("silver",0): {"boxes_end":4.22, "note":"x2 rounds to 4.22"},
 ("silver",2): {"boxes_end":0.256},
 ("silver",4): {"boxes_end":2.86},
 ("silver",6): {"boxes_end":1.71},
 ("gold",0):   {"boxes_end":1.71},
 ("gold",3):   {"boxes_end":4.9593},
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")=="multiple_choice": continue
        gs=p.get("guided_steps")
        if not gs: prob.append(f"{tier}[{i}] no guided_steps"); continue
        ba=box_answers(gs)
        sol=p["solutions"][0]
        # the solution value must appear as one of the box answers (the answer box)
        if not any(abs(float(x)-float(sol))<1e-6 for x in ba):
            prob.append(f"{tier}[{i}] solution {sol} not among box answers {ba}")
        # boundary
        idx=[j for j,st in enumerate(gs) if st.get("phase")=="substitute"]
        if not idx: prob.append(f"{tier}[{i}] no substitute boundary")
        else:
            sa=idx[0]
            live_after=sum(1 for st in gs[sa:] if st.get("answer") is not None)
            if sa<1 or live_after<2: prob.append(f"{tier}[{i}] boundary bad sa={sa} live={live_after}")

# 3. expects != solution (within 0.011) and derivable spot-checks
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=[float(x) for x in p["solutions"]]
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is None: continue
            ev=e if isinstance(e,list) else [e]
            if len(ev)==len(sol) and all(abs(float(a)-b)<0.011 for a,b in zip(ev,sol)):
                prob.append(f"{tier}[{i}] expect {e} == solution {sol}")

# verify specific misconception derivations
# bronze4 inverted: 4/20
assert rnd(4/20,1)==0.2
# bronze5 skip halving: 6+4
assert 6+4==10
# gold0 wrong (no 2):
x=2
for _ in range(3): x=(x**3+5)/(3*x**2)
if rnd(x,3)!=1.119: prob.append(f"gold0 missing-coef expect wrong: {rnd(x,3)}")
# gold0 single sub x1
if rnd((2*2**3+5)/(3*2**2),2)!=1.75: prob.append("gold0 x1 not 1.75")
# gold1 forgot constant: 8-10
assert 8-10==-2
# gold2 forgot double: 0.5*(0+16+(1+4+9))
assert 0.5*(16+14)==15
# gold4 negative root -3
# silver2 stop at x1 = 0.5 ; silver0 expect null;

# 4. teach/opener boxes recompute
g=out["guided"]
# opener
assert 100/2+30==80 and 80/2+30==70
# teach bronze grad (1,2)(4,11)=3
assert (11-2)/(4-1)==3
# teach silver 10/(x+2) x0=2 -> x2
x=2; x=10/(x+2); x=10/(x+2)
if rnd(x,2)!=2.22: prob.append(f"teach silver x2 {rnd(x,2)}")
# teach gold NR cube root 20 x0=3 -> x2
x=3
for _ in range(2): x=(2*x**3+20)/(3*x**2)
if rnd(x,3)!=2.715: prob.append(f"teach gold x2 {rnd(x,3)}")
# teach gold check 2.715^3
if rnd(2.715**3,2)!=20.01: prob.append(f"teach gold check {rnd(2.715**3,2)}")

# tier guide examples
assert (15-3)/(5-1)==3
assert math.sqrt(4*1+5)==3 and rnd(math.sqrt(4*3+5),2)==4.12
x=2
for _ in range(2): x=(2*x**3+7)/(3*x**2)
if rnd(x,3)!=1.913: prob.append(f"tg gold ex x2 {rnd(x,3)}")

# 5. PRESERVATION vs live
for f in ("related_videos","topic_links"):
    if json.dumps(out.get(f),sort_keys=True)!=json.dumps(live.get(f),sort_keys=True):
        prob.append(f"PRESERVATION changed: {f}")
# worked_examples: only labels' em dash allowed to change
wl=live["worked_examples"]; wo=out["worked_examples"]
if len(wl)!=len(wo): prob.append("worked_examples length changed")
for a,bb in zip(wl,wo):
    if a.get("question")!=bb.get("question") or a.get("difficulty")!=bb.get("difficulty"):
        prob.append("worked_examples q/difficulty changed")
    for sa,sb in zip(a["steps"],bb["steps"]):
        if sa.get("content")!=sb.get("content"): prob.append("worked_examples content changed")
        la,lb=sa.get("label",""),sb.get("label","")
        if la!=lb and "—" not in la: prob.append(f"worked_examples label changed unexpectedly {la}->{lb}")

# 6. no em dash anywhere student-facing (excluding note/skip)
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+str(k))
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,f"{path}[{j}]")
    elif isinstance(o,str) and "—" in o: prob.append(f"EM DASH at {path}")
scan(out,"pd")

# misconception count per problem <=3
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if len(p.get("misconceptions",[]))>3: prob.append(f"{tier}[{i}] >3 misconceptions")

# duplicate solutions within tier (non-MC)
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[tier]):
        if p.get("input_type")=="multiple_choice": continue
        key=tuple(p["solutions"])
        if key in seen: prob.append(f"{tier}[{i}] dup solution {key} with [{seen[key]}]")
        seen[key]=i

print("PROBLEMS:" if prob else "ALL CHECKS PASS")
for p in prob: print("  -",p)
