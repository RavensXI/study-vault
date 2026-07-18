# -*- coding: utf-8 -*-
import json,io,re
pd=json.load(io.open('_live_fresh.json',encoding='utf-8'))
out=[]
# normalise unicode math to python
def norm(s):
    s=s.replace('×','*').replace('÷','/').replace('−','-')
    # subscripts irrelevant to arithmetic; strip
    return s
# find an arithmetic expression ending in '=' inside pre
exprpat=re.compile(r'([0-9\.\(\)\s\*\/\+\-]+)=\s*$')
def eval_pre(pre):
    p=norm(pre).strip()
    m=exprpat.search(p)
    if not m: return None
    e=m.group(1).strip()
    if not re.search(r'[\*\/\+\-]',e): return None
    try:
        return eval(e,{"__builtins__":{}})
    except Exception:
        return None
def walk(name,steps):
    for i,st in enumerate(steps):
        if st.get('answer') is None: continue
        pre=st.get('pre','')
        v=eval_pre(pre)
        if v is None: continue
        a=float(st['answer'])
        if abs(v-a)>0.006:
            out.append(f"BOX MISMATCH {name}[{i}]: '{pre.strip()}' computes {v} but answer={a}")
walk("opener",pd['guided']['opener']['steps'])
for t in ('bronze','silver','gold'):
    walk("teach."+t,pd['guided']['teach'][t]['steps'])
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pd['problem_bank'][tier]):
        if p.get('guided_steps'): walk(f"{tier}[{i}]",p['guided_steps'])
out.append("recompute done; mismatches above (none = all boxes verified where parseable)")
io.open('_rc_out.txt','w',encoding='utf-8').write("\n".join(out))
print("\n".join(out) if out else "no output")
