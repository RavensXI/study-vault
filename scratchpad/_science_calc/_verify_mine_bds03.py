# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("lesson_biology-data-skills-L03@86a105121c.json", encoding="utf-8"))
errs = []

# fresh independent solutions
truth = {
 ("bronze",0): 34/6,   # 5.6667 rounds 5.67
 ("bronze",1): (250-200)/200*100,
 ("bronze",2): (240-300)/300*100,
 ("bronze",3): 15/5,
 ("bronze",4): 3*(50/1),
 ("bronze",5): (15-5)/5*100,
 ("silver",0): (45/10)*(200/1),
 ("silver",1): (180-240)/240*100,
 ("silver",2): (12/5)*(100/0.5),
 ("silver",3): (427-350)/350*100,
 ("gold",0): (40/8)*(400/0.5),
 ("gold",1): (7.8-3)/3*100,
 ("gold",2): ((9*800)-(12*800))/(12*800)*100,
}
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol = p["solutions"][0]
        t = truth[(tier,i)]
        tol = p.get("accept", 0.01)
        if abs(sol - t) > max(tol, 0.011):
            errs.append("%s[%d] stored %s vs fresh %.4f" % (tier,i,sol,t))
        # expects outside accept window
        for j,mc in enumerate(p.get("misconceptions") or []):
            e = mc.get("expect")
            if e is not None:
                if abs(e - sol) <= max(tol,0.011):
                    errs.append("%s[%d].misc[%d] expect %s inside accept of %s" % (tier,i,j,e,sol))
        # recompute every guided box by evaluating the arithmetic in pre where possible; instead trust final box == sol
        gs = p.get("guided_steps") or []
        boxes = [s for s in gs if s.get("answer") is not None]
        # last computational box before check often equals sol; verify at least one box equals sol
        vals = [s["answer"] for s in boxes]
        if not any(abs(v - sol) <= 0.02 for v in vals):
            errs.append("%s[%d] no guided box lands on solution %s (boxes %s)" % (tier,i,sol,vals))

# manually recompute each guided box arithmetic
def approx(a,b): return abs(a-b) <= 0.02
checks = {
 ("bronze",0): [("add",4+7+5+6+4+8,34),("cnt",6,6),("div",round(34/6,2),5.67),("chk",round(5.67*6,2),34.02)],
 ("bronze",1): [(50,250-200,50),(0.25,50/200,0.25),(25,0.25*100,25),(50,0.25*200,50)],
 ("bronze",2): [(-60,240-300,-60),(-0.2,-60/300,-0.2),(-20,-0.2*100,-20),(-60,-0.2*300,-60)],
 ("bronze",3): [(15,3+2+4+3+3,15),(5,5,5),(3,15/5,3),(15,3*5,15)],
 ("bronze",4): [(50,50/1,50),(150,3*50,150),(3,150/50,3)],
 ("bronze",5): [(10,15-5,10),(2,10/5,2),(200,2*100,200),(10,2*5,10)],
 ("silver",0): [(45,3+5+4+6+3+5+4+4+6+5,45),(4.5,45/10,4.5),(200,200/1,200),(900,4.5*200,900),(4.5,900/200,4.5)],
 ("silver",1): [(-60,180-240,-60),(-0.25,-60/240,-0.25),(-25,-0.25*100,-25),(-60,-0.25*240,-60)],
 ("silver",2): [(12,2+3+1+4+2,12),(2.4,12/5,2.4),(200,100/0.5,200),(480,2.4*200,480),(2.4,480/200,2.4)],
 ("silver",3): [(77,427-350,77),(0.22,77/350,0.22),(22,0.22*100,22),(77,0.22*350,77)],
 ("gold",0): [(40,5+3+6+4+5+7+4+6,40),(5,40/8,5),(800,400/0.5,800),(4000,5*800,4000),(10,5/0.5,10),(4000,10*400,4000)],
 ("gold",1): [(4.8,7.8-3,4.8),(1.6,4.8/3,1.6),(160,1.6*100,160),(4.8,1.6*3,4.8)],
 ("gold",2): [(9600,12*800,9600),(7200,9*800,7200),(-2400,7200-9600,-2400),(-0.25,-2400/9600,-0.25),(-25,-0.25*100,-25),(-25,(9-12)/12*100,-25)],
}
for k,rows in checks.items():
    for stored,computed,expect_disp in rows:
        if not approx(computed, expect_disp):
            errs.append("box arithmetic %s: computed %.4f != %s" % (k,computed,expect_disp))

# cross-check each guided box answer matches my computed expected sequence
for k,rows in checks.items():
    tier,i = k
    gs = pb[tier][i]["guided_steps"]
    boxes = [s["answer"] for s in gs if s.get("answer") is not None]
    exp = [r[2] for r in rows]
    if len(boxes) != len(exp):
        errs.append("%s box count %d != expected %d" % (k,len(boxes),len(exp)))
    else:
        for idx,(b,e) in enumerate(zip(boxes,exp)):
            if not approx(b,e):
                errs.append("%s box[%d] stored %s != expected %s" % (k,idx,b,e))

print("ERRORS:" if errs else "ALL CLEAN")
for e in errs: print("  -", e)
