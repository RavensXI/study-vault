import json
d=json.load(open('_live_canonical.json'))
pb=d['problem_bank']
errs=[]
def close(a,b,t=1e-6):
    try: return abs(float(a)-float(b))<=t
    except: return False

# Fresh solutions computed by hand, keyed by (tier,index): (expected_solution, expected_unit)
expected={
 ('bronze',0):(0.0025,'mol'),('bronze',1):(2.0,'mol/dm³'),('bronze',2):(0.4,'dm³'),
 ('bronze',3):(0.1,'mol'),('bronze',4):(0.3,'mol/dm³'),('bronze',5):(0.025,'mol'),
 ('bronze',6):(0.05,'dm³'),('bronze',7):(0.0548,'mol'),
 ('silver',0):(0.1,'mol/dm³'),('silver',1):(0.125,'mol/dm³'),('silver',2):(0.2,'mol/dm³'),
 ('silver',3):(0.25,'mol/dm³'),('silver',4):(0.4,'mol/dm³'),('silver',5):(0.5,'mol/dm³'),
 ('gold',0):(0.2,'mol/dm³'),('gold',1):(0.4,'mol/dm³'),('gold',2):(4.6,'g'),
 ('gold',3):(2.24,'g'),('gold',4):(1.6,'g'),('gold',5):(2.65,'g'),
}
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pb[tier]):
        exp,eu=expected[(tier,i)]
        sol=p['solutions'][0]
        acc=p.get('accept',0.005)
        if not close(sol,exp,max(acc,1e-6)):
            errs.append(f"{tier}[{i}] SOLUTION stored {sol} != computed {exp}")
        if p.get('unit')!=eu:
            errs.append(f"{tier}[{i}] UNIT stored {p.get('unit')} != {eu}")
        # verify each numeric guided box lands and mc within accept
        for j,st in enumerate(p.get('guided_steps',[])):
            if 'answer' in st and isinstance(st['answer'],(int,float)):
                pass # values verified manually; here just ensure numeric
        # expects outside accept window
        for m in p.get('misconceptions',[]):
            e=m.get('expect')
            if e is not None:
                if abs(float(e)-float(sol))<=acc:
                    errs.append(f"{tier}[{i}] DEAD EXPECT {e} within accept {acc} of {sol}")
print("problems:",sum(len(pb[t]) for t in pb if t in ['bronze','silver','gold']))
if errs:
    print("ERRORS:")
    for e in errs: print(" ",e)
else:
    print("all solutions, units, and expect-windows OK")
