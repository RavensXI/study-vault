import json, re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TR=standard_transformations+(implicit_multiplication_application,)
x,y=sp.symbols('x y')
def SY(s): return parse_expr(s, transformations=TR, local_dict={'x':x,'y':y})
live=json.load(open('_live_L10.json',encoding='utf-8'))
out=[]
bad=0
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(live['problem_bank'][tier]):
        chunks=re.findall(r'[\\][(](.*?)[\\][)]', p['display'])
        line=None
        for c in chunks:
            c2=c.replace('^','**').replace('−','-').replace('×','*')
            L,R=c2.split('=')
            for e in sp.solve(sp.Eq(SY(L),SY(R)),y):
                if e.is_polynomial(x) and sp.Poly(e,x).degree()<=1:
                    line=e
        for j,st in enumerate(p['guided_steps']):
            if not isinstance(st,dict) or 'answer' not in st: continue
            pre=st.get('pre','')
            m=re.search(r'At x = (−?-?\d+\.?\d*): y', pre)
            if m and line is not None:
                xv=float(m.group(1).replace('−','-'))
                yv=float(line.subs(x,xv))
                if abs(yv-float(st['answer']))>1e-9:
                    out.append("BAD y-box %s[%d].guided_steps[%d] x=%s expected y=%s stored=%s"%(tier,i,j,xv,yv,st['answer'])); bad+=1
out.append("y-box mismatches: %d"%bad)
open('_b.txt','w',encoding='utf-8').write("\n".join(out))
print("\n".join(out))
