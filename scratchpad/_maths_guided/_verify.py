import json,re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TR=standard_transformations+(implicit_multiplication_application,)
x,y=sp.symbols('x y')
def SY(s): return parse_expr(s, transformations=TR, local_dict={'x':x,'y':y})
live=json.load(open('_live_L10.json',encoding='utf-8'))
out=[]
bank=live['problem_bank']
allok=True
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(bank[tier]):
        disp=p['display']
        chunks=re.findall(r'[\\][(](.*?)[\\][)]', disp)
        eqlist=[]
        for c in chunks:
            c2=c.replace('^','**').replace(u'−','-').replace(u'×','*')
            L,R=c2.split('=')
            eqlist.append(sp.Eq(SY(L),SY(R)))
        solset=sp.solve(eqlist,[x,y],dict=True)
        xs=sorted(set(sp.nsimplify(s[x]) for s in solset), key=lambda v:float(v))
        stored=sorted(p['solutions'], key=lambda v:float(v))
        match = [float(v) for v in xs]==[float(v) for v in stored]
        # also verify each pair satisfies both eqs
        pairok=all(all(abs(complex(eq.lhs.subs({x:s[x],y:s[y]})-eq.rhs.subs({x:s[x],y:s[y]})))<1e-9 for eq in eqlist) for s in solset)
        if not match or not pairok: allok=False
        out.append("%s[%d] solved_x=%s stored=%s pairs_ok=%s %s"%(tier,i,[str(v) for v in xs],stored,pairok,"OK" if match else "*** MISMATCH"))
out.append("ALL_BANK_OK=%s"%allok)
open('_v.txt','w',encoding='utf-8').write("\n".join(out))
print("done")
