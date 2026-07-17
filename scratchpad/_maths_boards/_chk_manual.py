from fractions import Fraction as F
import sympy as sp
x,y=sp.symbols('x y')
def solve(a,b,c, d,e,f):  # a x + b y = c ; d x + e y = f
    r=sp.solve([sp.Eq(a*x+b*y,c), sp.Eq(d*x+e*y,f)],[x,y])
    return float(r[x]), float(r[y])

# (tier,index, eqs, stored)
cases=[
 ("bronze",0, (1,1,10, 1,-1,4), [7,3]),
 ("bronze",1, (2,1,9, 1,1,5), [4,1]),
 ("bronze",2, (1,3,13, 1,1,7), [4,3]),
 ("bronze",3, (3,1,14, 1,1,6), [4,2]),
 ("bronze",4, (2,1,11, 1,-1,4), [5,1]),
 ("bronze",5, (3,1,17, 1,1,7), [5,2]),
 ("bronze",6, (5,1,19, 2,1,10), [3,4]),
 ("bronze",7, (1,1,9, 2,-1,0), [3,6]),
 ("silver",0, (3,2,19, 2,-1,1), [3,5]),
 ("silver",1, (4,3,23, 2,1,9), [2,5]),
 ("silver",2, (2,3,13, 1,4,14), [2,3]),
 ("silver",3, (-3,1,-1, 2,1,14), [3,8]),   # y=3x-1 -> -3x+y=-1
 ("silver",4, (4,-1,17, 2,3,19), [5,3]),
 ("gold",0, (3,2,F(23,2), 2,3,11), [2.5,2]),  # 3x+2y=11.5 ; 2x+3y=11
 ("gold",1, (3,5,26, 7,2,22), [2,4]),
 ("gold",2, (1,1,15, 2,-1,6), [7,8]),
 ("gold",3, (4,-3,11, 3,2,4), [2,-1]),
]
bad=0
for tier,i,eq,stored in cases:
    sx,sy=solve(*eq)
    ok=abs(sx-stored[0])<1e-9 and abs(sy-stored[1])<1e-9
    if not ok: bad+=1
    print(f"{tier}[{i}]: solved=({sx},{sy}) stored={stored} {'OK' if ok else '*** MISMATCH ***'}")
print("BAD PROBLEMS:",bad)
