import json, math
live=json.load(open('_RECHK_live.json',encoding='utf-8'))
pb=live['problem_bank']
issues=[]

def r2(x):return round(x,2)
def r1(x):return round(x,1)

# recompute intermediate trig boxes referenced by 2dp
checks = {
 ('gold-teach','2/9->0.22'): (round(2/9,2),0.22),
 ('gold-teach','atan(2/9)'): (r1(math.degrees(math.atan(2/9))),12.5),
 ('gold-teach','tan12.5'): (r2(math.tan(math.radians(12.5))),0.22),
 ('gold-teach','sqrt85'): (r1(math.sqrt(85)),9.2),
 ('silver-teach','9/12'): (round(9/12,2),0.75),
 ('silver-teach','atan.75'): (r1(math.degrees(math.atan(0.75))),36.9),
 ('silver-teach','90-36.9'): (round(90-36.9,1),53.1),
 ('silver-teach','tan36.9'): (r2(math.tan(math.radians(36.9))),0.75),
 ('gold4','tan32'): (r2(math.tan(math.radians(32))),0.62),
 ('gold4','50tan32'): (r1(50*math.tan(math.radians(32))),31.2),
 ('gold4','31.2/50'): (r2(31.2/50),0.62),
 ('silver0','5/12'): (r2(5/12),0.42),
 ('silver0','tan22.6'): (r2(math.tan(math.radians(22.6))),0.42),
 ('silver1','tan40'): (r2(math.tan(math.radians(40))),0.84),
 ('silver1','8.4/10'): (r2(8.4/10),0.84),
 ('silver2','sin30'): (0.5,0.5),
 ('silver2','7/0.5'): (7/0.5,14),
 ('silver3','8/10'): (0.8,0.8),
 ('silver3','cos36.9'): (r2(math.cos(math.radians(36.9))),0.80),
 ('silver5','cos50'): (r2(math.cos(math.radians(50))),0.64),
 ('silver5','9.6/15'): (r2(9.6/15),0.64),
 ('silver6','7/25'): (r2(7/25),0.28),
 ('silver6','sin16.3'): (r2(math.sin(math.radians(16.3))),0.28),
 ('opener','9+16'): (25,25),
 ('opener','sqrt25'): (5,5),
}
for (k,lbl),(comp,stored) in checks.items():
    if abs(comp-stored)>1e-9:
        issues.append(f"{k} {lbl}: recomputed {comp} != box {stored}")

# verify each bank problem's guided_steps final numeric boxes land on solution
def final_land(tier):
    for i,p in enumerate(pb[tier]):
        if p.get('input_type')=='multiple_choice': continue
        gs=p.get('guided_steps',[])
        sol=p['solutions'][0]
        # find the box whose answer equals sol (the main answer box, pre-check)
        answers=[s.get('answer') for s in gs if 'answer' in s]
        if sol not in answers:
            issues.append(f"{tier}[{i}] solution {sol} not among guided box answers {answers}")
        # phase boundary check
        phases=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
        if not phases:
            issues.append(f"{tier}[{i}] no phase:substitute boundary")
        else:
            b=phases[0]
            live_boxes_after=sum(1 for s in gs[b:] if 'answer' in s)
            boxes_before=sum(1 for s in gs[:b] if 'answer' in s)
            if boxes_before<1: issues.append(f"{tier}[{i}] <1 box before boundary")
            if live_boxes_after<2: issues.append(f"{tier}[{i}] <2 live boxes at/after boundary ({live_boxes_after})")
for t in ['gold','silver','bronze']: final_land(t)

# em dash scan on student-facing strings
import re
def scan(obj,path=''):
    if isinstance(obj,str):
        if '—' in obj or '–' in obj:
            # allow inside note fields handled by caller
            issues.append(f"DASH at {path}: {obj[:50]}")
    elif isinstance(obj,dict):
        for k,v in obj.items():
            if k=='note': continue
            scan(v,path+'.'+k)
    elif isinstance(obj,list):
        for j,v in enumerate(obj): scan(v,f"{path}[{j}]")
scan(live)

print("BOX/STRUCTURE ISSUES:", len(issues))
for i in issues: print(" -",i)
