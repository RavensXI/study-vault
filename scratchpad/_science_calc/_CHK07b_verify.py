import json, math
pd = json.load(open("_CHK07b_canon.json", encoding="utf-8"))
# Fresh-solve each problem independently by re-deriving from display intent.
solves = {
 # gold
 ("gold",0): 0+math.sqrt(2*3*150),      # v^2=2*3*150 -> v
 ("gold",1): 400/8,                       # 20^2/(2*4)
 ("gold",2): 0.5*6*15 + 2*15 + 0.5*6*15,  # graph
 ("gold",3): (24.5**2)/(2*9.8),           # height
 ("gold",4): round(math.sqrt(15**2 + 2*3*100),1),
 ("gold",5): (4+10)/2*3 + 10*7,
 # bronze
 ("bronze",0): 600/40,
 ("bronze",1): (25-5)/10,
 ("bronze",2): 4*30,
 ("bronze",3): abs((10-30)/4),
 ("bronze",4): 60/15,
 ("bronze",5): 340*0.5,
 ("bronze",6): 18/6,
 ("bronze",7): 500/20,
 # silver
 ("silver",0): 54000/1800,
 ("silver",1): abs((0-30)/5),
 ("silver",2): 0.5*10*20 + 10*20,
 ("silver",3): (8+20)/2*4,
 ("silver",4): (0+4*3)/2*3,
 ("silver",5): 90000/3600,
}
errs=[]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        stored=p["solutions"][0]
        mine=solves[(tier,i)]
        if abs(stored-mine) > 1e-6:
            errs.append(f"{tier}[{i}] stored={stored} mine={mine}")
        # check expects outside accept window
        acc=p.get("accept",0)
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is not None and abs(e-stored)<=acc:
                errs.append(f"{tier}[{i}].misconceptions[{j}] DEAD expect={e} within accept {acc} of {stored}")
print("SOLUTION/EXPECT ERRORS:", errs if errs else "NONE")

# Verify every guided_steps final box lands on solution and boxes are internally consistent
def check_walk(steps, label, sol=None):
    for k,s in enumerate(steps):
        if "answer" in s and not isinstance(s["answer"],(int,float)):
            errs.append(f"{label}[{k}] non-numeric answer")
# just report walks presence
w=[]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        gs=p.get("guided_steps",[])
        boxes=[s for s in gs if "answer" in s]
        haspivot=any(s.get("phase")=="substitute" for s in gs)
        live_after=0; seen=False
        for s in gs:
            if s.get("phase")=="substitute": seen=True
            if seen and "answer" in s: live_after+=1
        if not haspivot: w.append(f"{tier}[{i}] no phase")
        if live_after<2: w.append(f"{tier}[{i}] <2 live boxes ({live_after})")
print("WALK STRUCTURE:", w if w else "all have phase + >=2 live boxes")
