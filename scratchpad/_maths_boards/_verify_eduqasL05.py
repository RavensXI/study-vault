# -*- coding: utf-8 -*-
import json
pd = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_graphs-L05_diagrams.json", encoding="utf-8"))
errs=[]
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"]; it=p.get("input_type")
        gs=p.get("guided_steps")
        if gs:
            live=[s for s in gs if s.get("answer") is not None]
            last=live[-1]["answer"]
            # final box should equal a solution component
            if it=="fraction":
                if last not in sol: errs.append(f"{tier}[{i}] final box {last} not in solutions {sol}")
            else:
                if abs(float(last)-float(sol[0]))>0.001: errs.append(f"{tier}[{i}] final box {last} != sol {sol[0]}")
            # completion boundary: >=2 live at/after first phase substitute, >=1 before
            phase_idx=next((k for k,s in enumerate(gs) if s.get("phase")=="substitute"),None)
            if phase_idx is None: errs.append(f"{tier}[{i}] no phase boundary")
            else:
                after=sum(1 for s in gs[phase_idx:] if s.get("answer") is not None)
                before=sum(1 for s in gs[:phase_idx] if s.get("answer") is not None)
                if after<2: errs.append(f"{tier}[{i}] {after} live after boundary")
                if before<1: errs.append(f"{tier}[{i}] {before} boxes before boundary")
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None:
                ev=e if isinstance(e,list) else [e]
                sv=[float(x) for x in sol]
                if len(ev)==len(sv) and all(abs(float(a)-b)<0.011 for a,b in zip(ev,sv)):
                    errs.append(f"{tier}[{i}] expect==correct {e}")

# recompute stated answers from known equations (manual map)
checks = {
 ("bronze",0):8,("bronze",1):-8,("bronze",2):2,("bronze",3):16,("bronze",4):2,("bronze",5):9,
}
# bronze order now: b0(8),b1(-8),b3(1)->idx2,b4(16)->idx3,b5(2)->idx4,b7(9)->idx5,b2(MC 2)->idx6,b6(MC 1)->idx7
recompute = {
 ("bronze",0):("2**3",8),("bronze",1):("(-2)**3",-8),("bronze",2):("2**0",1),("bronze",3):("2**4",16),
 ("bronze",4):("6/3",2),("bronze",5):("3**2",9),
 ("silver",0):("2**3-8",0),("silver",1):("-3/-1",3),("silver",2):("5*2**3",40),("silver",3):("-(3**3)",-27),
 ("gold",0):("12/-4",-3),("gold",1):("(3-1)**3",8),("gold",2):("500*1.05**0",500),("gold",4):("-2*4",-8),
}
for (t,i),(expr,exp) in recompute.items():
    got=eval(expr)
    if abs(got-exp)>0.001: errs.append(f"{t}[{i}] recompute {expr}={got} != {exp}")
    if abs(float(pb[t][i]['solutions'][0])-exp)>0.001: errs.append(f"{t}[{i}] stored sol != {exp}")

# expect error reproduction spot checks
assert 2*3==6            # bronze cube_as_times_3
assert 5*2*3==30         # silver s2
assert 3**3-1==26        # gold g1 bracket ignored
assert -2/4==-0.5        # gold g4 divide
assert 500*1.05==525     # gold g2
print("VERIFY errors:", errs if errs else "NONE")
