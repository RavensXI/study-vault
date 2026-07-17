import json
pd=json.load(open('_live_algebra-L08.json',encoding='utf-8'))
for tier in ('bronze','silver','gold'):
    seen={}
    for i,p in enumerate(pd['problem_bank'][tier]):
        k=tuple(p['solutions'])
        seen.setdefault(k,[]).append(i)
    dups={k:v for k,v in seen.items() if len(v)>1}
    print(tier,'DUPS:',dups)
# proposed fixes verify
import math
def disc(a,b,c): return b*b-4*a*c
print('fix b0 x2+7x-5 b=',7)
print('fix b7 roots x2+5x+2 disc=',disc(1,5,2),'-> roots=',2 if disc(1,5,2)>0 else 0)
# recheck bronze answers after fix distinct
after=[7,12,0,-16,3,9,17,2]
print('bronze after fix distinct?',len(after)==len(set(after)), after)
