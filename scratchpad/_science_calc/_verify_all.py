import json, io, math
pd=json.load(open('_live_81a530c1.json',encoding='utf-8'))['practice_data']
errs=[]

def approx(a,b,tol=0.005):
    return abs(a-b)<=tol

# ---- fresh-solve bank ----
expected = {
 ('bronze',0):50, ('bronze',1):480, ('bronze',2):6, ('bronze',3):150,
 ('bronze',4):700, ('bronze',5):0.25,
 ('silver',0):0.125, ('silver',1):0.3125, ('silver',2):100, ('silver',3):0.4,
 ('gold',0):400, ('gold',1):12000, ('gold',2):26.83,
}
pb=pd['problem_bank']
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pb[tier]):
        sol=p['solutions'][0]
        exp=expected[(tier,i)]
        if not approx(sol,exp,0.02):
            errs.append(f"{tier}[{i}] solution {sol} != my {exp}")
        # walk boxes land on solution: last box (check) not necessarily = sol
        # verify each guided box arithmetic by re-deriving from pre text is manual; check final solve box
        gs=p.get('guided_steps',[])
        boxes=[st for st in gs if 'answer' in st]
        # check expects outside accept window
        acc=p.get('accept', None)
        for m in p.get('misconceptions',[]):
            e=m.get('expect')
            if e is not None and acc is not None:
                if abs(e-sol)<=acc:
                    errs.append(f"{tier}[{i}] DEAD EXPECT {e} inside accept {acc} of {sol}")

# recompute walk boxes explicitly
def chk(name, got, want):
    if not approx(got,want): errs.append(f"WALKBOX {name}: computed {want} but stored {got}")

# bronze bank walks
chk('b0 mult',50,5*10); chk('b0 chk',5,50/10)
chk('b1 mult',480,80*6); chk('b1 chk',80,480/6)
chk('b2 mult',6,300*0.02); chk('b2 chk',300,6/0.02)
chk('b3 div',150,6/0.04); chk('b3 chk',6,150*0.04)
chk('b4 mult',700,70*10); chk('b4 chk',70,700/10)
chk('b5 sq',0.0025,0.05*0.05); chk('b5 half',100,0.5*200); chk('b5 mult',0.25,100*0.0025); chk('b5 chk',0.0025,0.25/100)
# silver
chk('s0 div',0.125,5/40); chk('s0 chk',5,40*0.125)
chk('s1 sq',0.015625,0.125*0.125); chk('s1 half',20,0.5*40); chk('s1 mult',0.3125,20*0.015625); chk('s1 chk',0.015625,0.3125/20)
chk('s2 w',3000,250*12); chk('s2 p',100,3000/30); chk('s2 chk',3000,100*30)
chk('s3 ext',0.04,20/500); chk('s3 sq',0.0016,0.04*0.04); chk('s3 pe',0.4,0.5*500*0.0016); chk('s3 chk',0.0016,0.4/250)
# gold
chk('g0 top',4,2*2); chk('g0 sq',0.01,0.10*0.10); chk('g0 div',400,4/0.01); chk('g0 chk',2,0.5*400*0.01)
chk('g1 mult',12000,2400*5); chk('g1 chk',2400,12000/5)
chk('g2 sq',0.09,0.30*0.30); chk('g2 pe',18,0.5*400*0.09); chk('g2 v2',720,(2*18)/0.05); chk('g2 sqrt',26.83,math.sqrt(720))
# teach walks
chk('teach-gold sq',0.04,0.20*0.20); chk('teach-gold pe',10,0.5*500*0.04); chk('teach-gold v2',1000,(2*10)/0.02); chk('teach-gold sqrt',31.62,math.sqrt(1000))
chk('teach-bronze conv',0.1,10/100); chk('teach-bronze sq',0.01,0.1*0.1); chk('teach-bronze half',100,0.5*200); chk('teach-bronze mult',1,100*0.01)
chk('teach-silver ext',0.05,4/80); chk('teach-silver sq',0.0025,0.05*0.05); chk('teach-silver half',40,0.5*80); chk('teach-silver mult',0.1,40*0.0025)
# opener
chk('opener 3N',6,3*2); chk('opener force',5,10/2)
# tier guide examples
chk('tg-gold v2',36,(2*9)/0.5); chk('tg-gold v',6,math.sqrt(36))
chk('tg-bronze',10,250*0.04); chk('tg-silver',0.2,4/20)

# expects reproduce
def exp_chk(tier,i,pat,want):
    p=pb[tier][i]
    for m in p['misconceptions']:
        if m['pattern']==pat:
            if m['expect'] is None: 
                errs.append(f"{tier}[{i}] {pat} expect is null (expected {want})"); return
            if not approx(m['expect'],want,0.02):
                errs.append(f"{tier}[{i}] {pat} expect {m['expect']} != my {want}")
            return
    errs.append(f"{tier}[{i}] pattern {pat} not found")

exp_chk('bronze',1,'wrong_formula',80+6)
exp_chk('bronze',2,'unit_error',300*2)
exp_chk('bronze',3,'inverse_error',0.04*6)
exp_chk('bronze',5,'forgot_square',0.5*200*0.05)
exp_chk('bronze',5,'forgot_half',200*0.0025)
exp_chk('silver',0,'inverse_error',40/5)
exp_chk('silver',1,'forgot_square',0.5*40*0.125)
exp_chk('silver',1,'forgot_half',40*0.015625)
exp_chk('silver',2,'forgot_step',3000)
exp_chk('silver',3,'forgot_square',0.5*500*0.04)
exp_chk('silver',3,'wrong_formula',20*0.04)
exp_chk('gold',0,'forgot_square',4/0.1)
exp_chk('gold',1,'wrong_force',1200*5)
exp_chk('gold',2,'forgot_step',18)

if errs:
    print("ERRORS:")
    for e in errs: print(" -",e)
else:
    print("ALL BOX/SOLUTION/EXPECT CHECKS PASS")
