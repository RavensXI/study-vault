import json, io, re
pd=json.load(io.open("_CHK_L09_live.json",encoding="utf-8"))
pb=pd["problem_bank"]

def parse_eqs(display):
    # extract \(...\) equations
    eqs=re.findall(r'\\((.*?)\\)', display)
    return eqs

# manual fresh-solve using sympy
import sympy as sp
x,y=sp.symbols('x y')
def solve_from_eqstrings(eqstrs):
    eqs=[]
    for s in eqstrs:
        s=s.replace('−','-')
        if '=' not in s: continue
        L,R=s.split('=')
        # insert * between number and variable
        L=re.sub(r'(\d)([xy])', r'\1*\2', L)
        R=re.sub(r'(\d)([xy])', r'\1*\2', R)
        eqs.append(sp.Eq(sp.sympify(L), sp.sympify(R)))
    return sp.solve(eqs,[x,y])

problems_report=[]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        disp=p["display"]
        sols=p["solutions"]
        eqstrs=parse_eqs(disp)
        # Some problems are word problems: skip auto-solve, handle manually
        note=""
        if len(eqstrs)>=2 and all('=' in e for e in eqstrs):
            try:
                res=solve_from_eqstrings(eqstrs)
                sx=float(res[x]); sy=float(res[y])
                ok = abs(sx-sols[0])<1e-9 and abs(sy-sols[1])<1e-9
                note=f"solved x={sx} y={sy} stored={sols} {'OK' if ok else '*** MISMATCH ***'}"
            except Exception as e:
                note=f"autoSolveFail: {e}"
        else:
            note=f"WORD PROBLEM (manual) stored={sols}"
        print(f"{tier}[{i}]: {note}")
