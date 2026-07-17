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
    # replace latex delimiters with | and split
    d=disp.replace('\(','|').replace('\)','|')
    parts=d.split('|')
    return [pp for i,pp in enumerate(parts) if i%2==1 and '=' in pp]

allok=True
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(pb[tier]):
        disp=strip_svg(p["display"])
        sols=sorted(round(float(v),6) for v in p["solutions"])
        if 'tangent' in disp or 'value of k' in disp:
            got=[float(s) for s in solve(Eq(k**2-4,0),k) if float(s)>0]
            ok=got==[float(v) for v in p["solutions"]]
            print(f"{tier}[{i}] TANGENT k={got} stored={p['solutions']} {'OK' if ok else '***MISMATCH***'}")
            allok&=ok; continue
        raw=eqs_of(disp)
        parsed=[]
        for e in raw:
            l,r=e.split('=')
            parsed.append(Eq(sympify(to_expr(l)),sympify(to_expr(r))))
        xs=solve(parsed,[x,y],dict=True)
        got=sorted(set(round(float(d[x]),6) for d in xs if x in d))
        ok=got==sols
        allok&=ok
        print(f"{tier}[{i}] fresh_x={got} stored={sols} {'OK' if ok else '***MISMATCH***'}")
print("ALL SOLUTIONS OK" if allok else "SOLUTION ERRORS PRESENT")
