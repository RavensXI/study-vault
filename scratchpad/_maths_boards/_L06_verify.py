# -*- coding: utf-8 -*-
import re, json, sympy as sp
x=sp.symbols('x')
def P(s):
    t=s.replace('\\(','').replace('\\)','').strip().replace('^2','**2')
    t=re.sub(r'(\d)(x)',r'\1*\2',t); t=re.sub(r'(\d)\(',r'\1*(',t)
    t=re.sub(r'\)\(',r')*(',t); t=re.sub(r'x\(',r'x*(',t)
    return sp.expand(sp.sympify(t))
d=json.load(open("lesson_maths-eduqas_algebra-L06.json",encoding="utf-8"))
fails=[]
EM='—'
def chk_em(s,path):
    if EM in s: fails.append(f"EM DASH {path}: {s}")

pb=d["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        disp=p["display"].replace("Factorise","").strip()
        tgt=P(disp)
        exps=[P(o) for o in p["options"]]
        sol=p["solutions"][0]
        if sp.simplify(exps[sol]-tgt)!=0: fails.append(f"{tier}[{i}] solutions idx {sol} not correct")
        # exactly one correct
        ncorr=sum(1 for e in exps if sp.simplify(e-tgt)==0)
        if ncorr!=1: fails.append(f"{tier}[{i}] {ncorr} correct options")
        # duplicates
        for a in range(4):
            for b in range(a+1,4):
                if sp.simplify(exps[a]-exps[b])==0: fails.append(f"{tier}[{i}] dup opts {a},{b}")
        chk_em(p["hint"],f"{tier}[{i}].hint")
        if '\\(' in p["hint"] or '<' in p["hint"]: fails.append(f"{tier}[{i}] hint has latex/html")
        for mi,m in enumerate(p["misconceptions"]):
            e=m["expect"]
            if e==sol: fails.append(f"{tier}[{i}].misc[{mi}] expect==sol")
            chk_em(m["message"],f"{tier}[{i}].misc[{mi}].msg")
            pat=m["pattern"]; ev=exps[e]
            # classify
            coeffs=lambda poly: (sp.Poly(poly,x).coeff_monomial(x**2),sp.Poly(poly,x).coeff_monomial(x),sp.Poly(poly,x).coeff_monomial(1))
            a2,a1,a0=coeffs(ev); t2,t1,t0=coeffs(tgt)
            if pat=='sign_error':
                # middle sign flipped, same a2 and a0
                if not(a2==t2 and a0==t0 and a1==-t1): fails.append(f"{tier}[{i}].misc[{mi}] sign_error mismatch: {ev}")
            elif pat=='forgot_a':
                # leading coeff differs from target OR it's k(...) ; just ensure not equal target
                if sp.simplify(ev-tgt)==0: fails.append(f"{tier}[{i}].misc[{mi}] forgot_a equals tgt")
            elif pat=='wrong_pair':
                if sp.simplify(ev-tgt)==0: fails.append(f"{tier}[{i}].misc[{mi}] wrong_pair equals tgt")
            elif pat=='dots':
                if sp.simplify(ev-tgt)==0: fails.append(f"{tier}[{i}].misc[{mi}] dots equals tgt")

# opener boxes
op=d["guided"]["opener"]
for s in op["steps"]:
    if 'say' in s: chk_em(s['say'],'opener.say')
    if 'hint' in s: chk_em(s['hint'],'opener.hint')
# opener product/sum
assert op["steps"][1]["answer"]*op["steps"][2]["answer"]==12
assert op["steps"][1]["answer"]+op["steps"][2]["answer"]==7
# svg self-contained
svg=op["display"]
if 'http' in svg or '<script' in svg: fails.append("opener svg external/script")
if 'role="img"' not in svg or 'aria-label' not in svg: fails.append("opener svg missing a11y")
if 'currentColor' not in svg: fails.append("opener svg no currentColor")

# teach boxes recompute
def evalbox(pre):
    m=re.search(r'=\s*$',pre)
    return None
for name,t in d["guided"]["teach"].items():
    for si,s in enumerate(t["steps"]):
        if 'say' in s: chk_em(s['say'],f"teach.{name}[{si}].say")
        if 'pre' in s:
            chk_em(s['pre'],f"teach.{name}[{si}].pre")
            if 'hint' in s: chk_em(s['hint'],f"teach.{name}[{si}].hint")
        if 'done' in s: chk_em(s['done'],f"teach.{name}[{si}].done")

# tier guide em-dash + budget
for tg in d["tier_guides"].values():
    chk_em(tg["title"],"tg.title")
    for st in tg["steps"]: chk_em(st,"tg.step")

# check specific recomputes of teach arithmetic
def num(a): return a
assert d["guided"]["teach"]["bronze"]["steps"][1]["answer"]==2*6
assert d["guided"]["teach"]["silver"]["steps"][1]["answer"]==2*-12
assert d["guided"]["teach"]["gold"]["steps"][1]["answer"]==6*4

print("FAILS:",len(fails))
for f in fails: print(" ",f)
print("solutions:",{t:[p['solutions'][0] for p in pb[t]] for t in ('bronze','silver','gold')})
