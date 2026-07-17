import json, io, re
import sympy as sp
from sympy import Rational, symbols, solveset, S, sympify, Interval, oo

x, k = sp.symbols('x k')
live=json.load(io.open("_CHK_algL12ocr_live.json","r",encoding="utf-8"))
errs=[]

def texnum(s):
    return s

# --- MULTIPLE CHOICE quadratic-inequality solver ---
# We independently solve each MC problem's inequality and compare the option text
# to the interval we compute.
def solve_ineq(expr_str, rel, rhs_str="0"):
    lhs=sympify(expr_str)
    rhs=sympify(rhs_str)
    if rel=="<": r=lhs<rhs
    elif rel=="<=": r=lhs<=rhs
    elif rel==">": r=lhs>rhs
    elif rel==">=": r=lhs>=rhs
    return sp.solve_univariate_inequality(r, x, relational=False)

# Manually encode each MC problem: (tier, idx, solveset, correct_option_text_desc)
# We'll parse option text into intervals to match.
def parse_option(opt):
    # returns a sympy set for common GCSE forms
    o=opt.replace("\\(","").replace("\\)","").replace("\\frac{1}{3}","1/3").replace("\\frac{1}{2}","1/2")
    o=o.replace("\\tfrac{1}{3}","1/3").replace("\\tfrac{1}{2}","1/2")
    o=o.replace("\\leq","<=").replace("\\geq",">=")
    o=o.replace("−","-").strip()
    o=o.replace(" ","")
    # forms: a<x<b ; x<a orx>b ; x<a  ; x>a
    def num(t):
        return Rational(sp.sympify(t))
    m=re.match(r"^(-?[\d/]+)<x<(-?[\d/]+)$", o)
    if m: return Interval.open(num(m.group(1)),num(m.group(2)))
    m=re.match(r"^(-?[\d/]+)<=x<=(-?[\d/]+)$", o)
    if m: return Interval(num(m.group(1)),num(m.group(2)))
    m=re.match(r"^x<(-?[\d/]+)orx>(-?[\d/]+)$", o)
    if m: return Interval.open(-oo,num(m.group(1)))|Interval.open(num(m.group(2)),oo)
    m=re.match(r"^x<=(-?[\d/]+)orx>=(-?[\d/]+)$", o)
    if m: return Interval(-oo,num(m.group(1)))|Interval(num(m.group(2)),oo)
    m=re.match(r"^x>(-?[\d/]+)$", o)
    if m: return Interval.open(num(m.group(1)),oo)
    m=re.match(r"^x<(-?[\d/]+)$", o)
    if m: return Interval.open(-oo,num(m.group(1)))
    m=re.match(r"^x>=(-?[\d/]+)$", o)
    if m: return Interval(num(m.group(1)),oo)
    m=re.match(r"^x<=(-?[\d/]+)$", o)
    if m: return Interval(-oo,num(m.group(1)))
    return ("UNPARSED",opt)

MC=[
 ("gold",0,"3*x**2+2*x-1",">"),
 ("gold",2,"x**2-3*x-4",">"),   # rearranged from x^2-2x> x+4
 ("gold",4,"-x**2-x+6",">="),   # 6 - x - x^2 >= 0
 ("bronze",0,"x**2-4","<"),
 ("bronze",1,"x**2-9",">"),
 ("bronze",2,"(x-1)*(x-5)","<"),
 ("bronze",3,"x**2-6*x+8","<="),
 ("bronze",5,"(x+3)*(x-1)",">"),
 ("bronze",7,"x**2+x-6","<"),
 ("silver",0,"x**2-2*x-8",">="),
 ("silver",1,"2*x**2-5*x-3","<"),
 ("silver",3,"-x**2+4*x-3",">"),
 ("silver",4,"x**2+6*x+5",">"),
]
for tier,idx,expr,rel in MC:
    prob=live["problem_bank"][tier][idx]
    truth=solve_ineq(expr,rel)
    sol_idx=prob["solutions"][0]
    chosen=prob["options"][sol_idx]
    parsed=parse_option(chosen)
    ok = (parsed==truth)
    print(f"{tier}[{idx}] {expr} {rel} 0 -> truth {truth} | stored opt#{sol_idx} '{chosen}' parsed {parsed} -> {'OK' if ok else 'MISMATCH'}")
    if not ok:
        errs.append(f"{tier}[{idx}] MC mismatch: truth {truth} vs stored {parsed}")

# --- gold[1] discriminant no-real-roots ---
# x^2+kx+4=0 no real roots: k^2-16<0 -> -4<k<4
truth=sp.solve_univariate_inequality(k**2-16<0,k,relational=False)
prob=live["problem_bank"]["gold"][1]
print("gold[1] k range truth", truth, "stored opt", prob["options"][prob["solutions"][0]])

print("\n--- single_value integer counts ---")
def count_int(setexpr, lo, hi):
    return sum(1 for i in range(lo,hi+1) if setexpr.contains(i))

# gold[3]: x^2-9<=0 AND x+1>0
s=Interval(-3,3)
c=[i for i in range(-3,4) if i>-1]
print("gold[3] count", len(c), "stored", live["problem_bank"]["gold"][3]["solutions"])
# bronze[4]: x^2>25, integers -10..10
c=[i for i in range(-10,11) if i*i>25]
print("bronze[4] count", len(c), "stored", live["problem_bank"]["bronze"][4]["solutions"])
# bronze[6]: x^2-3x-4<=0 integers
c=[i for i in range(-50,51) if i*i-3*i-4<=0]
print("bronze[6] count", len(c), c, "stored", live["problem_bank"]["bronze"][6]["solutions"])
# silver[2]: x^2<=3x+10
c=[i for i in range(-50,51) if i*i<=3*i+10]
print("silver[2] count", len(c), c, "stored", live["problem_bank"]["silver"][2]["solutions"])
# silver[5]: positive integers x^2<50
c=[i for i in range(1,100) if i*i<50]
print("silver[5] count", len(c), c, "stored", live["problem_bank"]["silver"][5]["solutions"])
# silver[6]: positive root of x^2+4x-5>=0
print("silver[6] positive root", [r for r in sp.solve(x**2+4*x-5) if r>0], "stored", live["problem_bank"]["silver"][6]["solutions"])

print("\nERRORS:", errs if errs else "NONE")
