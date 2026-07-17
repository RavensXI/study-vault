import json, re
from sympy import symbols, Eq, solve, sympify, sqrt
x,y,k=symbols('x y k')
pd=json.load(open("_CHK_L10_live.json",encoding="utf-8"))
pb=pd["problem_bank"]

def strip_svg(d):
    d=re.sub(r'<svg.*?</svg>','',d,flags=re.S)
    d=re.sub(r'<span.*?</span>','',d,flags=re.S)
    return d

def latex_eqs(disp):
    # extract \( ... \) chunks
    return re.findall(r'\\((.*?)\\)',disp)

def to_expr(s):
    s=s.replace('^','**')
    s=re.sub(r'(\d)([xyk])',r'\1*\2',s)
    s=re.sub(r'([xyk])([xyk])',r'\1*\2',s)
    return s

for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(pb[tier]):
        disp=strip_svg(p["display"])
        sols=p["solutions"]
        eqs=latex_eqs(disp)
        try:
            parsed=[]
            for e in eqs:
                if '=' not in e: continue
                l,r=e.split('=')
                parsed.append(Eq(sympify(to_expr(l)),sympify(to_expr(r))))
            if 'tangent' in disp:
                # G4 special: x^2 - kx +1=0 disc=0, positive k
                continue
            xs=solve(parsed,[x,y],dict=True)
            got=sorted(set(round(float(d[x]),6) for d in xs if x in d))
            want=sorted(round(float(v),6) for v in sols)
            ok = got==want
            print(f"{tier}[{i}] disp_x={got} stored={want} {'OK' if ok else '*** MISMATCH ***'}")
        except Exception as ex:
            print(f"{tier}[{i}] PARSE-ERR {ex} eqs={eqs}")
