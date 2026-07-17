# -*- coding: utf-8 -*-
import sympy as sp
x = sp.symbols('x')

# (display_expr_lhs, rhs, expected) after repair
def solve_eq(lhs, rhs):
    sols = sp.solve(sp.Eq(lhs, rhs), x)
    return sols

bronze = [
    ("2x+5=13", 2*x+5, 13, 4),
    ("3x-4=11", 3*x-4, 11, 5),
    ("4x+1=25", 4*x+1, 25, 6),
    ("x/3=7", x/3, 7, 21),
    ("5x=35", 5*x, 35, 7),
    ("x+9=4", x+9, 4, -5),
    ("7x+2=23 (was 30)", 7*x+2, 23, 3),
    ("6x-10=38 (was 20)", 6*x-10, 38, 8),
]
silver = [
    ("5x-3=2x+12", 5*x-3, 2*x+12, 5),
    ("4(x+2)=20", 4*(x+2), 20, 3),
    ("3(2x-1)=21", 3*(2*x-1), 21, 4),
    ("7x+4=3x+28 (was 24)", 7*x+4, 3*x+28, 6),
    ("2(3x+1)=5x+9 (was 7)", 2*(3*x+1), 5*x+9, 7),
    ("8-2x=3x-2 (was 3x-7)", 8-2*x, 3*x-2, 2),
    ("3(x-4)=2(x+1)", 3*(x-4), 2*(x+1), 14),
]
gold = [
    ("(2x+1)/3=5", (2*x+1)/3, 5, 7),
    ("(x+3)/4=(x-1)/2", (x+3)/4, (x-1)/2, 5),
    ("3x/5+2=x/2+4", 3*x/5+2, x/2+4, 20),
    ("5(x-2)/3=2(x+1)/2+1", 5*(x-2)/3, 2*(x+1)/2+1, 8),
    ("(4x-3)/5=(3x+2)/4", (4*x-3)/5, (3*x+2)/4, 22),
]
ok = True
for name, tier in [("BRONZE",bronze),("SILVER",silver),("GOLD",gold)]:
    print("==",name)
    sols = []
    for label,l,r,exp in tier:
        got = solve_eq(l,r)
        good = (len(got)==1 and got[0]==exp)
        sols.append(exp)
        print(("OK " if good else "XX ")+label+" -> "+str(got)+" expect "+str(exp))
        if not good: ok=False
    dups = [s for s in set(sols) if sols.count(s)>1]
    print("  distinct:", len(sols)==len(set(sols)), "dups:", dups)
    if dups: ok=False
print("ALL OK" if ok else "PROBLEMS")
