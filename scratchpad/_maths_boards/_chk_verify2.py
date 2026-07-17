import json, io, re
import sympy as sp
pd=json.load(io.open("_CHK_L09_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
x,y=sp.symbols('x y')

def parse_eqs(display):
    return re.findall(r'\\((.*?)\\)', display)

def solve_from_eqstrings(eqstrs):
    eqs=[]
    for s in eqstrs:
        s=s.replace('−','-').replace('×','*')
        if '=' not in s: continue
        L,R=s.split('=')
        L=re.sub(r'(\d)\s*([xy])', r'\1*\2', L)
        R=re.sub(r'(\d)\s*([xy])', r'\1*\2', R)
        eqs.append(sp.Eq(sp.sympify(L), sp.sympify(R)))
    return sp.solve(eqs,[x,y])

# test regex
print("sample eqs bronze0:", parse_eqs(pb["bronze"][0]["display"]))
bad=0
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        eqstrs=[e for e in parse_eqs(p["display"]) if '=' in e]
        sols=p["solutions"]
        if len(eqstrs)>=2:
            try:
                res=solve_from_eqstrings(eqstrs)
                sx=float(res[x]); sy=float(res[y])
                ok = abs(sx-sols[0])<1e-9 and abs(sy-sols[1])<1e-9
                if not ok: bad+=1
                print(f"{tier}[{i}]: x={sx} y={sy} stored={sols} {'OK' if ok else '*** MISMATCH ***'}")
            except Exception as e:
                print(f"{tier}[{i}]: FAIL {e} | eqs={eqstrs}")
        else:
            print(f"{tier}[{i}]: WORD, eqs found={eqstrs}, stored={sols}")
print("BAD:",bad)
