# -*- coding: utf-8 -*-
# Fresh-solve every stored problem from its display; report duplicates.
from fractions import Fraction as F
checks = []
def rec(tier,i,desc,mine,stored):
    ok = (mine==stored)
    checks.append((tier,i,desc,mine,stored,ok))

# BRONZE (live)
rec("b",0,"grad (0,2)(3,8)",F(8-2,3-0),F(2))
rec("b",1,"grad (1,4)(5,12)",F(12-4,5-1),F(2))
rec("b",2,"yint y=3x+2",F(2),F(2))
rec("b",3,"grad y=4x-3",F(4),F(4))
rec("b",4,"grad (2,1)(6,9)",F(9-1,6-2),F(2))
rec("b",5,"y=5x+1 x=3",F(5*3+1),F(16))
rec("b",6,"chart y at x=3 [1,3,5,7,9,11]",F(7),F(7))
rec("b",7,"chart grad [10,8,6,4,2,0]",F(8-10,1-0),F(-2))
# SILVER
rec("s",0,"grad (-1,4)(3,-8)",F(-8-4,3-(-1)),F(-3))
rec("s",1,"y=mx+3 thru (2,11) m",F((11-3),2),F(4))
rec("s",2,"2y=6x+10 grad",F(6,2),F(3))
rec("s",3,"grad (-2,-3)(4,9)",F(9-(-3),4-(-2)),F(2))
rec("s",4,"(0,-2)(5,13) m",F(13-(-2),5-0),F(3))
rec("s",5,"3y-9x=12 yint",F(12,3),F(4))
rec("s",6,"(1,7)(3,3) yint: m then c",F(7)-F(3-7,3-1)*1,F(9))
# GOLD
rec("g",0,"grad (-3,11)(5,-5)",F(-5-11,5-(-3)),F(-2))
rec("g",1,"(2,5)(6,17) c",F(5)-F(17-5,6-2)*2,F(-1))
rec("g",2,"parallel A m2 B(0,7)(2,3)",0 if F(3-7,2-0)!=2 else 1,0)
rec("g",3,"5x+2y=20 grad",F(-5,2),F(-5,2))
rec("g",4,"midpoint (a,3)(7,11)=(5,7) a",2*5-7,3)

bad=[c for c in checks if not c[5]]
print("MISMATCHES:", len(bad))
for c in bad: print("  ",c)

# duplicate scan per tier
from collections import Counter
for t in ("b","s","g"):
    sols=[str(c[4]) for c in checks if c[0]==t]
    cnt=Counter(sols)
    dups={k:v for k,v in cnt.items() if v>1}
    print(t,"solutions:",sols,"DUPS:",dups)
