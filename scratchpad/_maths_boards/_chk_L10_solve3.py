import json, re
from sympy import symbols, Eq, solve, sympify
x,y,k=symbols('x y k')
pd=json.load(open("_CHK_L10_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
def strip_svg(d):
    d=re.sub(r'<svg.*?</svg>','',d,flags=re.S)
    d=re.sub(r'<span.*?</span>','',d,flags=re.S)
    return d
def to_expr(s):
    s=s.strip().replace('^','**')
    s=re.sub(r'(\d)\s*([xyk])',r'\1*\2',s)
    s=re.sub(r'([xyk])\s*([xyk])',r'\1*\2',s)
    return s
def eqs_of(disp):
    return re.findall(r'\\(([^()]*?)\\)',disp)

results=[]
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(pb[tier]):
        disp=strip_svg(p["display"])
        sols=sorted(round(float(v),6) for v in p["solutions"])
        raw=eqs_of(disp)
        if 'tangent' in disp or 'positive value of k' in disp:
            # G4: y=kx+2 tangent to y=x^2+3 -> x^2 -kx+1=0 disc 0
            sol_k=solve(Eq(k**2-4,0),k)
            got=[float(s) for s in sol_k if float(s)>0]
            print(f"{tier}[{i}] TANGENT k={got} stored={p['solutions']} {'OK' if got==[float(v) for v in p['solutions']] else '***MISMATCH***'}")
            continue
        parsed=[]
        for e in raw:
            if '=' not in e: continue
            l,r=e.split('=')
            parsed.append(Eq(sympify(to_expr(l)),sympify(to_expr(r))))
        xs=solve(parsed,[x,y],dict=True)
        got=sorted(set(round(float(d[x]),6) for d in xs if x in d))
        ok=got==sols
        print(f"{tier}[{i}] fresh_x={got} stored={sols} {'OK' if ok else '***MISMATCH***'}  eqs={raw}")
