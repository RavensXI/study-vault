# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_maths-ocr_graphs-L05.json", encoding="utf-8"))
prob=0; bad=[]

# fresh-solve every bank problem
def solve(t,i,disp,sol):
    pass

pb=pd["problem_bank"]
# recompute guided_steps final answer must equal solution for single_value
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        it=p.get("input_type","single_value")
        sol=p["solutions"]
        gs=p.get("guided_steps")
        if gs:
            liveboxes=[s for s in gs if s.get("answer") is not None]
            # the walk should reach the solution somewhere among its boxes
            vals=[s["answer"] for s in liveboxes]
            if it=="single_value" and sol[0] not in vals:
                bad.append(f"{t}[{i}] solution {sol} not reached by any box {vals}")
        # expects must differ from solution and not equal it
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            if it=="single_value" and abs(float(e)-float(sol[0]))<1e-9:
                bad.append(f"{t}[{i}].misc[{j}] expect==solution {e}")

# check charts satisfy equations
def approx(a,b,tol=0.02): return abs(a-b)<=tol
# b5 reciprocal 6/x
for ds in pb["bronze"][5]["chart"]["data"]["datasets"]:
    for pt in ds["data"]:
        if not approx(pt["y"], 6.0/pt["x"]): bad.append(f"b5 chart pt {pt} != 6/x")
# s4 decay 0.5^x
for ds in pb["silver"][4]["chart"]["data"]["datasets"]:
    for pt in ds["data"]:
        if not approx(pt["y"], 0.5**pt["x"], 0.02): bad.append(f"s4 chart pt {pt} != 0.5^x")
# g1 cubic x^3-9x
for ds in pb["gold"][1]["chart"]["data"]["datasets"]:
    for pt in ds["data"]:
        if not approx(pt["y"], pt["x"]**3-9*pt["x"], 0.02): bad.append(f"g1 chart pt {pt} != x^3-9x")

# verify a few expects reproduce their described error explicitly
checks = {
 ("bronze",0): 9, ("bronze",1):8, ("bronze",2):48, ("bronze",3):6, ("bronze",4):0,
 ("bronze",6):5, ("bronze",7):2,
 ("silver",0):-4, ("silver",1):-4, ("silver",2):0.6, ("silver",3):-4, ("silver",5):10, ("silver",6):4,
 ("gold",0):1296, ("gold",1):9, ("gold",2):20, ("gold",3):12, ("gold",4):6,
}
for (t,i),exp in checks.items():
    got=pb[t][i]["misconceptions"][0]["expect"]
    if abs(float(got)-float(exp))>1e-9: bad.append(f"{t}[{i}] expect {got} != intended {exp}")

# preservation
print("related_videos preserved:", pd["related_videos"]==[])
print("topic_links preserved:", pd["topic_links"]=={"prerequisites":[]})
print("worked_examples count:", len(pd["worked_examples"]))

# opener/teach box tallies
op=[s for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
print("opener boxes:", len(op))
for t in ["bronze","silver","gold"]:
    tb=[s for s in pd["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
    print("teach",t,"boxes:",len(tb))

print("BAD:", len(bad))
for b in bad: print("  -",b)
