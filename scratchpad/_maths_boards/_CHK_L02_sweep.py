import json,re
live=json.load(open("_CHK_L02_livefresh.json",encoding="utf-8"))["practice_data"]
issues=[]
# 1. em dash sweep in student-facing strings (exclude internal 'note')
def walk(obj,path):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k=='note': continue
            walk(v,path+"."+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj): walk(v,path+f"[{i}]")
    elif isinstance(obj,str):
        if '—' in obj or '–' in obj:
            issues.append(f"EM/EN DASH at {path}: {obj[:60]}")
walk(live,"root")

# 2. numeric-only boxes in guided_steps/teach/opener
def check_boxes(steps,path):
    for i,s in enumerate(steps):
        if 'answer' in s:
            a=s['answer']
            if not isinstance(a,(int,float)):
                issues.append(f"NON-NUMERIC box {path}[{i}] answer={a!r}")
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(live['problem_bank'][tier]):
        if 'guided_steps' in p: check_boxes(p['guided_steps'],f"{tier}[{i}].guided_steps")
    check_boxes(live['guided']['teach'][tier]['steps'],f"teach.{tier}")
check_boxes(live['guided']['opener']['steps'],"opener")

# 3. completion boundary: >=1 box before phase, >=2 live boxes at/after phase
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(live['problem_bank'][tier]):
        gs=p.get('guided_steps',[])
        boxidx=[j for j,s in enumerate(gs) if 'answer' in s]
        phase=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
        if p.get('input_type')=='multiple_choice': continue
        if not phase:
            issues.append(f"{tier}[{i}] NO phase boundary")
            continue
        ph=phase[0]
        before=[j for j in boxidx if j<ph]
        after=[j for j in boxidx if j>=ph]
        if len(before)<1: issues.append(f"{tier}[{i}] <1 box before phase")
        if len(after)<2: issues.append(f"{tier}[{i}] <2 live boxes at/after phase (got {len(after)})")

print("ISSUES:",len(issues))
for x in issues: print("  ",x)
