# -*- coding: utf-8 -*-
"""Independent checker: fresh-solve displays, recompute boxes, reproduce expects."""
import json, io, re

pd = json.load(io.open("lesson_maths-eduqas_number-L01.json", encoding="utf-8"))
errs=[]

def latex_to_expr(d):
    s=d
    s=s.replace("\\left","").replace("\\right","")
    # fractions \dfrac{a}{b} -> (a)/(b)
    def frac(m): return "(("+m.group(1)+")/("+m.group(2)+"))"
    s=re.sub(r"\\dfrac\{([^{}]*)\}\{([^{}]*)\}", frac, s)
    s=re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", frac, s)
    # sqrt{n} -> (n)**0.5
    s=re.sub(r"\\sqrt\{([^{}]*)\}", r"(\1)**0.5", s)
    # a^b  and a^{b}
    s=re.sub(r"\^\{([^{}]*)\}", r"**(\1)", s)
    s=re.sub(r"\^(\-?\d+)", r"**(\1)", s)
    s=s.replace("\\times","*").replace("\\div","/").replace("\\cdot","*")
    s=s.replace("\\(","").replace("\\)","")
    s=s.replace("−","-").replace("×","*").replace("÷","/")
    return s

def solve(display):
    expr=latex_to_expr(display)
    return eval(expr)

# 1. fresh-solve every problem
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        got=solve(p["display"])
        want=p["solutions"][0]
        if abs(got-want)>1e-9:
            errs.append(f"{tier}[{i}] display solves to {got} but stored {want} :: {p['display']}")

# 2. recompute every guided_steps box: check final boxes land on solution;
#    also verify each numeric box's pre-arithmetic if it is a pure 'a op b =' form
def eval_pre(pre):
    # strip label words; try to evaluate the arithmetic in pre like 'Check: 23 + 8 - 24 = '
    t=pre
    t=re.sub(r"^[A-Za-z: ]*","",t)  # drop leading 'Check:' etc
    t=t.replace("−","-").replace("×","*").replace("÷","/").replace("²","**2").replace("³","**3")
    t=t.replace("=","").strip()
    # handle (−3)*(−3) style already ascii minus
    if not re.fullmatch(r"[-+*/(). 0-9]+\**\d*", t.replace(" ","")):
        return None
    try:
        return eval(t)
    except Exception:
        return None

def check_walk(steps, label, solution=None):
    boxes=[s for s in steps if s.get("answer") is not None]
    for s in steps:
        if s.get("answer") is None: continue
        v=eval_pre(s["pre"])
        if v is not None and abs(v - s["answer"])>1e-9:
            errs.append(f"{label} box pre '{s['pre'].strip()}' computes {v} but answer {s['answer']}")
    if solution is not None:
        # the solution should appear as some box answer in the walk
        vals=[b["answer"] for b in boxes]
        if solution not in vals:
            errs.append(f"{label} walk never produces solution {solution}; box answers={vals}")

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        check_walk(p["guided_steps"], f"{tier}[{i}]", p["solutions"][0])

# teach + opener boxes
for tier in ("bronze","silver","gold"):
    check_walk(pd["guided"]["teach"][tier]["steps"], f"teach.{tier}")
check_walk(pd["guided"]["opener"]["steps"], "opener")

# 3. reproduce every expect by committing the error text-described? We at least
#    verify expect != solution and expect is scalar for single_value.
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            if isinstance(e,list):
                errs.append(f"{tier}[{i}].mc[{j}] expect is list on single_value")
            elif abs(e-sol)<1e-9:
                errs.append(f"{tier}[{i}].mc[{j}] expect equals solution")

# explicit expect reproductions (commit the described error)
def approx(a,b): return abs(a-b)<1e-9
checks = {
 ("bronze",0):[(30,(6+4)*3)],
 ("bronze",1):[(6,(20-8)/2)],
 ("bronze",2):[(16,(3+5)*2)],
 ("bronze",3):[(3,24/(6+2))],
 ("bronze",4):[(0,10-(3+7))],
 ("bronze",5):[(42,((2*5)+4)*3)],
 ("bronze",6):[(3,18/(3*2))],
 ("bronze",7):[(3,(14-8)/2)],
 ("silver",0):[(23,3+5*4)],
 ("silver",1):[(23,4*2+3*5),(95,(16+3)*5)],
 ("silver",2):[(10,50-(4+6**2))],
 ("silver",3):[(2,36/((2+4)*3)),(66,((36/2)+4)*3)],
 ("silver",4):[(-14,2*(9-4**2))],
 ("silver",5):[(10,100/(5*2))],
 ("silver",6):[(45,(7+2)*(8-3))],
 ("gold",0):[(34.5,18+6/2**2+5*3),(27,(18+6)/2+5*3)],
 ("gold",1):[(5,(2**2+3**2)-4*(7-5)),(42,((2+3)**2-4)*(7-5))],
 ("gold",2):[(0.2,(3*3-7)/(2*5))],
 ("gold",3):[(-17,-(3**2)+4*(-2)),(17,(-3)**2+4*2)],
 ("gold",4):[(17,(49**0.5)+(2*3)*3-8),(37,((49**0.5)+2**3)*3-8)],
}
for (tier,idx),pairs in checks.items():
    stored=[m["expect"] for m in pb[tier][idx].get("misconceptions",[])]
    for want,derived in pairs:
        if not approx(want,derived):
            errs.append(f"{tier}[{idx}] derivation mismatch: claimed {want} vs committed-error {derived}")
        if not any(approx(want,s) for s in stored if isinstance(s,(int,float))):
            errs.append(f"{tier}[{idx}] expect {want} not present in stored {stored}")

if errs:
    print("FAIL", len(errs))
    for e in errs: print(" -",e)
else:
    print("ALL CLEAR: solves, boxes, and expects verified")
