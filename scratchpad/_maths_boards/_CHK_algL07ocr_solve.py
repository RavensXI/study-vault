import json, re, math
from fractions import Fraction as F
pd=json.load(open("_CHK_algL07ocr_live.json",encoding="utf-8"))
def parse_side(s):
    s=s.replace('−','-').replace(' ','').replace('(','').replace(')','')
    terms=re.findall(r'[+-]?[^+-]+', s)
    d={0:F(0),1:F(0),2:F(0)}
    for t in terms:
        if not t: continue
        m=re.match(r'([+-]?)(\d*)x\^2$', t)
        if m:
            sign=-1 if m.group(1)=='-' else 1
            c=int(m.group(2)) if m.group(2) else 1
            d[2]+=sign*c; continue
        m=re.match(r'([+-]?)(\d*)x$', t)
        if m:
            sign=-1 if m.group(1)=='-' else 1
            c=int(m.group(2)) if m.group(2) else 1
            d[1]+=sign*c; continue
        m=re.match(r'([+-]?)(\d+)$', t)
        if m:
            sign=-1 if m.group(1)=='-' else 1
            d[0]+=sign*int(m.group(2)); continue
        raise ValueError("term parse fail: "+t)
    return d
def solve_display(disp):
    inner=re.search(r'\\((.*?)\\)', disp).group(1)
    inner=inner.replace(chr(92),"")
    L,R=inner.split('=')
    dl=parse_side(L); dr=parse_side(R)
    a=dl[2]-dr[2]; b=dl[1]-dr[1]; c=dl[0]-dr[0]
    disc=b*b-4*a*c
    sq=math.isqrt(int(disc))
    if sq*sq!=int(disc): return (a,b,c),None
    r1=F(-b+sq,2*a); r2=F(-b-sq,2*a)
    return (a,b,c),sorted([r1,r2])
errs=[]
for tier in ['gold','bronze','silver']:
    for i,p in enumerate(pd['problem_bank'][tier]):
        (abc),roots=solve_display(p['display'])
        if roots is None:
            errs.append(f"{tier}[{i}] irrational! {p['display']}"); continue
        stored=sorted([F(str(x)) for x in p['solutions']])
        if roots!=stored:
            errs.append(f"{tier}[{i}] {p['display']}: solved={[str(r) for r in roots]} stored={p['solutions']}")
        for r in roots:
            if r.denominator not in (1,2,4,5,10):
                errs.append(f"{tier}[{i}] messy root {r} in {p['display']}")
print("SOLVE MISMATCHES:" if errs else "ALL DISPLAYS SOLVE TO STORED SOLUTIONS (clean)")
for e in errs: print(" ",e)
for tier in ['gold','bronze','silver']:
    seen={}
    for i,p in enumerate(pd['problem_bank'][tier]):
        k=tuple(sorted(p['solutions']))
        if k in seen: print(f"DUP answer {tier}: idx {seen[k]} & {i} -> {p['solutions']}")
        seen[k]=i
    disps=[p['display'] for p in pd['problem_bank'][tier]]
    if len(set(disps))!=len(disps): print(f"DUP display in {tier}")
print("solve-check done")
