# -*- coding: utf-8 -*-
import json
d=json.load(open('_canon_b5d94e42c2.json',encoding='utf-8'))
pb=d['problem_bank']
errs=[]
def close(a,b,t): return abs(float(a)-float(b))<=t
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
        sol=p['solutions'][0]; acc=p.get('accept') or 0.005
        if not close(sol,exp,max(acc,1e-9)): errs.append(f"{tier}[{i}] SOL {sol}!={exp}")
        if p.get('unit')!=eu: errs.append(f"{tier}[{i}] UNIT {p.get('unit')!r}!={eu}")
        for m in p.get('misconceptions',[]):
            e=m.get('expect')
            if e is not None and abs(float(e)-float(sol))<=acc:
                errs.append(f"{tier}[{i}] DEAD EXPECT {e} in accept {acc} of {sol}")
        # completion boundary: >=1 non-say step before first phase-substitute box, >=2 live boxes at/after
        gs=p.get('guided_steps',[])
        boxidx=[j for j,s in enumerate(gs) if 'answer' in s]
        phase_boxes=[j for j in boxidx if gs[j].get('phase')=='substitute']
        if gs:
            if not phase_boxes: errs.append(f"{tier}[{i}] no phase-substitute box")
            else:
                first=min(j for j,s in enumerate(gs) if s.get('phase')=='substitute')
                before=[j for j in boxidx if j<first]
                after=[j for j in boxidx if j>=first]
                if len(before)<1: errs.append(f"{tier}[{i}] no live box before boundary")
                if len(after)<2: errs.append(f"{tier}[{i}] <2 live boxes after boundary")
print("problems:",sum(len(pb[t]) for t in ['bronze','silver','gold']))
print("ERRORS" if errs else "ALL CLEAN")
for e in errs: print("  ",e)
