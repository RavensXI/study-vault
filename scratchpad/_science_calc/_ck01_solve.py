import json, io, math
pd=json.load(io.open("_ck01_row0.json",encoding="utf-8"))
pb=pd["problem_bank"]
errs=[]
def approx(a,b,tol): return abs(a-b)<=tol+1e-9
# fresh independent solve for each problem
solvers={
 # bronze
 ("bronze",0): 0.5*2*3**2,
 ("bronze",1): 5*10*4,
 ("bronze",2): 50*3,
 ("bronze",3): 600/20,
 ("bronze",4): 0.5*10*4**2,
 ("bronze",5): 3*10*2,
 ("bronze",6): 1500/5,
 ("bronze",7): 30*4,
 ("silver",0): 0.5*1200*20**2,
 ("silver",1): 500*12,
 ("silver",2): 75*10*6,
 ("silver",3): math.sqrt(2*10/0.2),
 ("silver",4): 200*10*15/30,
 ("silver",5): math.sqrt(2*(600*10*20)/600),
 ("gold",0): math.sqrt(2*(800*10*45)/800),
 ("gold",1): (0.5*1200*30**2)/50,
 ("gold",2): 120*10*8/6,
 ("gold",3): 90/(0.5*10),
 ("gold",4): 60*10*3/4,
}
for (t,i),val in solvers.items():
    p=pb[t][i]
    sol=p["solutions"][0]; acc=p.get("accept",0)
    if not approx(val,sol,acc):
        errs.append(f"{t}[{i}] fresh={val} stored={sol} acc={acc} MISMATCH")
    # check every guided_step box lands and expects outside window
    for j,m in enumerate(p.get("misconceptions",[])):
        e=m.get("expect")
        if e is not None and approx(e,sol,acc):
            errs.append(f"{t}[{i}].misconceptions[{j}] DEAD expect={e} inside accept window of {sol}±{acc}")
print("SOLVE/EXPECT CHECK")
for e in errs: print("  ",e)
if not errs: print("  all solutions match and all expects outside accept window")

# verify guided_step box internal arithmetic where pre is an expression "a OP b = "
import re
box_errs=[]
def collect(steps,ctx):
    for k,s in enumerate(steps):
        if "answer" in s and isinstance(s.get("pre"),str):
            pre=s["pre"].strip()
            m=re.match(r'^(.*?)=\s*$',pre)
            # try to eval expression left of '='
            expr=pre.rstrip("= ").strip()
            # extract trailing arithmetic after last ':' if present
            if ":" in expr: expr=expr.split(":")[-1].strip()
            expr2=expr.replace("×","*").replace("÷","/").replace("²","**2")
            # handle sqrt symbol
            sq=re.match(r'^√\s*([\d.]+)$',expr2)
            try:
                if sq:
                    v=math.sqrt(float(sq.group(1)))
                elif re.match(r'^[\d\.\+\-\*\/\(\)\s]+$',expr2):
                    v=eval(expr2)
                else:
                    continue
                if abs(v-s["answer"])>0.005:
                    box_errs.append(f"{ctx}[{k}] '{pre}' evals {v} but answer={s['answer']}")
            except Exception:
                pass
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        collect(p.get("guided_steps",[]),f"{t}[{i}].guided_steps")
for tier in ["bronze","silver","gold"]:
    collect(pd["guided"]["teach"][tier]["steps"],f"teach.{tier}")
collect(pd["guided"]["opener"]["steps"],"opener")
print("BOX ARITH CHECK")
for e in box_errs: print("  ",e)
if not box_errs: print("  all parseable boxes compute to their stored answer")
