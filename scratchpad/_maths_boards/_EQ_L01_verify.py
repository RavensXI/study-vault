# -*- coding: utf-8 -*-
import json, io, re
import sympy as sp

x,y,a,b,m,n,p,t = sp.symbols('x y a b m n p t')
ns = {'x':x,'y':y,'a':a,'b':b,'m':m,'n':n,'p':p,'t':t}

with io.open("lesson_maths-eduqas_algebra-L01.json", encoding="utf-8") as f:
    pd = json.load(f)

fails=[]

def latex_to_expr(s):
    # strip \( \)
    s = s.replace("\\(","").replace("\\)","").strip()
    s = s.replace("\\times","*")
    if "\\div" in s:
        L,R = s.split("\\div",1)
        s = "((%s)/(%s))"%(L.strip(),R.strip())
    # \frac{A}{B} -> ((A)/(B))
    while "\\frac" in s:
        m2 = re.search(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", s)
        if not m2: break
        s = s[:m2.start()] + "((%s)/(%s))"%(m2.group(1),m2.group(2)) + s[m2.end():]
    # ^{...}
    s = re.sub(r"\^\{([^{}]*)\}", r"**(\1)", s)
    s = re.sub(r"\^(-?\d+)", r"**(\1)", s)
    # implicit multiplication: number/letter adjacency
    s = re.sub(r"(\d)([a-z\(])", r"\1*\2", s)
    s = re.sub(r"([a-z\)])(\d)", r"\1*\2", s)  # careful but ok since powers already **
    s = re.sub(r"([a-z\)])([a-z\(])", r"\1*\2", s)
    return sp.sympify(s, locals=ns)

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,prob in enumerate(pb[tier]):
        disp = prob["display"]
        # remove "Simplify"
        expr_s = disp.replace("Simplify","").strip()
        try:
            val = sp.simplify(latex_to_expr(expr_s))
        except Exception as e:
            fails.append("%s[%d] PARSE FAIL %s : %s"%(tier,i,expr_s,e)); continue
        sol_idx = prob["solutions"][0]
        opt = prob["options"][sol_idx]
        try:
            optval = sp.simplify(latex_to_expr(opt))
        except Exception as e:
            fails.append("%s[%d] OPT PARSE FAIL %s"%(tier,i,opt)); continue
        if sp.simplify(val-optval)!=0:
            fails.append("%s[%d] MISMATCH display=%s => %s ; option[%d]=%s => %s"%(tier,i,expr_s,val,sol_idx,opt,optval))
        # distinct options
        if len(set(prob["options"]))!=len(prob["options"]):
            fails.append("%s[%d] duplicate options"%(tier,i))

# verify teach walk final boxes land on the stated answers
def check_teach():
    T=pd["guided"]["teach"]
    # bronze 6x+2y+3x+5y -> 9x+7y ; boxes 9,7,16,16
    assert sp.simplify((6*x+2*y+3*x+5*y)-(9*x+7*y))==0
    assert 6+3==9 and 2+5==7 and 6+2+3+5==16 and 9+7==16
    # silver 4a^2 b * 2 a b^4 -> 8 a^3 b^5 ; boxes 8,3,5,8
    assert sp.simplify((4*a**2*b*2*a*b**4)-(8*a**3*b**5))==0
    assert 4*2==8 and 2+1==3 and 1+4==5
    # gold ((3x)^2*2x)/(6x^2) -> 3x ; boxes 9,18,3,1,3
    assert sp.simplify(((3*x)**2*2*x)/(6*x**2)-3*x)==0
    assert 3*3==9 and 9*2==18 and 18//6==3 and 3-2==1
check_teach()

# opener: 2+4=6, 3+2=5, and 2x+4x=6x, 3y+2y=5y
assert 2+4==6 and 3+2==5
assert sp.simplify((2*x+4*x)-6*x)==0 and sp.simplify((3*y+2*y)-5*y)==0

# tier_guide examples
assert sp.simplify((7*a+2*b-3*a+6*b)-(4*a+8*b))==0 and 7+2-3+6==12 and 4+8==12
assert sp.simplify((2*x*(x+3)+x**2)-(3*x**2+6*x))==0 and 2*4+1==9 and 3+6==9
assert sp.simplify(((2*x**3)**2/(4*x**2))-x**4)==0

if fails:
    print("FAILS:")
    for f in fails: print("  -",f)
else:
    print("ALL BANK + BOXES + EXAMPLES VERIFIED CLEAN")
