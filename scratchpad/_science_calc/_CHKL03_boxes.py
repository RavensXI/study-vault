import json,re
pd=json.load(open("_L03_canon_live.json"))["practice_data"]
issues=[]
# Extract trailing "A op B = " arithmetic from pre and check == answer
pat=re.compile(r'([0-9][0-9\.,]*)\s*([×÷\+−x*/-])\s*([0-9][0-9\.,]*)\s*=\s*$')
def num(s): return float(s.replace(',',''))
def evalop(a,op,b):
    if op in '×x*': return a*b
    if op in '÷/': return a/b
    if op=='+': return a+b
    if op in '−-': return a-b
def scan_steps(steps,path):
    for j,s in enumerate(steps):
        if 'answer' not in s: continue
        pre=s.get('pre','')
        ans=s['answer']
        m=pat.search(pre)
        if m:
            a,op,b=num(m.group(1)),m.group(2),num(m.group(3))
            r=evalop(a,op,b)
            if abs(r-ans)>0.005:
                issues.append(f"BOX ARITH {path}[{j}]: '{pre.strip()}' -> {r} but answer={ans}")
        # else: box not a simple A op B form; skip (verified manually)
# problem banks
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pd['problem_bank'][tier]):
        scan_steps(p.get('guided_steps',[]),f"{tier}[{i}].gs")
# teach
for t,w in pd['guided']['teach'].items():
    scan_steps(w['steps'],f"teach.{t}")
# opener
scan_steps(pd['guided']['opener']['steps'],"opener")
print("BOX ARITH ISSUES:",len(issues))
for x in issues: print("  ",x)

# completion boundary: >=1 step before phase, >=2 live boxes at/after
def boundary(steps,path):
    boxes=[(j,s) for j,s in enumerate(steps) if 'answer' in s]
    pidx=[j for j,s in enumerate(steps) if s.get('phase')=='substitute']
    if not pidx:
        issues.append(f"NO PHASE {path}"); return
    p0=min(pidx)
    before=[j for j,s in boxes if j<p0]
    after=[j for j,s in boxes if j>=p0]
    if len(before)<1: issues.append(f"BOUNDARY <1 before {path}")
    if len(after)<2: issues.append(f"BOUNDARY <2 after {path} (after={len(after)})")
b2=[]
issues2=[]
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pd['problem_bank'][tier]):
        st=p.get('guided_steps')
        if st:
            boxes=[(j,s) for j,s in enumerate(st) if 'answer' in s]
            pidx=[j for j,s in enumerate(st) if s.get('phase')=='substitute']
            if not pidx: issues2.append(f"NO PHASE {tier}[{i}]"); continue
            p0=min(pidx)
            before=sum(1 for j,s in boxes if j<p0)
            after=sum(1 for j,s in boxes if j>=p0)
            if before<1: issues2.append(f"<1before {tier}[{i}]")
            if after<2: issues2.append(f"<2after {tier}[{i}] after={after}")
print("BOUNDARY ISSUES:",len(issues2))
for x in issues2: print("  ",x)
