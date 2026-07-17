# -*- coding: utf-8 -*-
import json, math
pd = json.load(open('_geoL08_live.json', encoding='utf-8'))
pb = pd['problem_bank']

def comp(v): return v

# independent re-solve of each stored problem -> expected solution
checks = {
 'bronze': [
   ('(2,5)+(3,-1) x', 2+3),
   ('(2,5)+(3,-1) y', 5+(-1)),
   ('3*(2,-1) x', 3*2),
   ('(4,3)-(1,5) y', 3-5),
   ('|(3,4)|', math.hypot(3,4)),
   ('-2*(3,-4) y', -2*(-4)),
   ('(1,2)+(-1,-2) x', 1+(-1)),
   ('|(5,12)|', math.hypot(5,12)),
 ],
 'silver': [
   ('AB=(5,7)-(1,3) x', 5-1),
   ('2a-3b x, a(4,1)b(2,-1)', 2*4-3*2),
   ('2a-3b y', 2*1-3*(-1)),
   ('parallel (2,6)&(3,9)', 1),
   ('midpoint A(2,4)B(8,10) x', (2+8)/2),
   ('|(-3,4)|', math.hypot(-3,4)),
   ('(6,-8)=k(3,k) k', -8/(6/3)),
 ],
 'gold': [
   ('OM=.5(a+b) x, a(2,6)b(10,2)', 0.5*(2+10)),
   ('P=A+1/3(B-A) y, A(1,3)B(7,9)', 3+(1/3)*(9-3)),
   ('AB=(4,6)-(1,2) x', 4-1),
   ('|(a,a)|=10 a', round(10/math.sqrt(2),1)),
   ('P=A+2/3(B-A) x, A(3,1)B(9,5)', 3+(2/3)*(9-3)),
 ],
}
for tier in ('bronze','silver','gold'):
    print('==',tier)
    sols=[p['solutions'] for p in pb[tier]]
    for i,(desc,val) in enumerate(checks[tier]):
        stored=sols[i][0]
        ok=abs(val-stored)<1e-9 or abs(round(val,1)-stored)<1e-9
        print(f'  [{i}] stored={stored} recomputed={val} {desc} {"OK" if ok else "**MISMATCH**"}')
    # duplicate check
    from collections import Counter
    c=Counter(tuple(s) for s in sols)
    dups={k:v for k,v in c.items() if v>1}
    print('  DUPES:', dups)
