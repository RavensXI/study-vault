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
p=pb["gold"][0]
disp=strip_svg(p["display"])
print("DISP:",disp)
eqs=re.findall(r'\\((.*?)\\)',disp)
print("EQS:",eqs)
parsed=[]
for e in eqs:
    if '=' not in e: continue
    l,r=e.split('=')
    parsed.append(Eq(sympify(to_expr(l)),sympify(to_expr(r))))
print("PARSED:",parsed)
print("SOLVE:",solve(parsed,[x,y],dict=True))
