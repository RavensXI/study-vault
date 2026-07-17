# -*- coding: utf-8 -*-
import json, io, re
from fractions import Fraction as F
pd = json.load(io.open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\lesson_maths-eduqas_probability-statistics-L02.json", encoding="utf-8"))
prob=[]
def note(m): prob.append(m)

# ---- 1. Fresh-solve each bank problem from its display, compare to solutions ----
# Extract region numbers from svg to cross-check consistency.
def svg_nums(disp):
    # returns dict of the four region texts and total, in order aOnly,both,bOnly,neither
    m = re.findall(r'x="76" y="96"[^>]*>([^<]*)<', disp)
    a = re.findall(r'x="130" y="96"[^>]*>([^<]*)<', disp)
    b = re.findall(r'x="184" y="96"[^>]*>([^<]*)<', disp)
    n = re.findall(r'x="236" y="150"[^>]*>([^<]*)<', disp)
    t = re.findall(r'Total: ([^<]*)<', disp)
    return (m[0] if m else None, a[0] if a else None, b[0] if b else None,
            n[0] if n else None, t[0] if t else None)

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        disp = p["display"]
        sols = p["solutions"]
        tag = "%s[%d]" % (tier,i)
        # SVG region consistency for count problems
        if "<svg" in disp and "Total: 1<" not in disp:
            aO,both,bO,nei,tot = svg_nums(disp)
            def num(x):
                if x in (None,"","?"): return None
                try: return float(x)
                except: return None
            vals = [num(aO),num(both),num(bO),num(nei),num(tot)]
            known = [v for v in vals[:4] if v is not None]
            if vals[4] is not None:
                s = sum(v for v in vals[:4] if v is not None)
                # if all four known, must equal total
                if all(v is not None for v in vals[:4]):
                    if abs(s - vals[4]) > 1e-6:
                        note("%s SVG regions %s sum %.2f != total %s" % (tag, vals[:4], s, vals[4]))
        # final guided box lands on solution
        gs = p.get("guided_steps")
        if gs:
            finals = [st for st in gs if st.get("answer") is not None]
            last = finals[-1]["answer"]
            # for fraction, last box is denominator; second last numerator
            if p["input_type"]=="fraction" and len(sols)==2:
                num_box = finals[-2]["answer"]; den_box=finals[-1]["answer"]
                if [num_box,den_box]!=sols:
                    note("%s fraction final boxes [%s,%s] != sols %s" % (tag,num_box,den_box,sols))
            elif p["input_type"]=="single_value":
                if abs(last - sols[0])>1e-9:
                    note("%s single final box %s != sol %s" % (tag,last,sols[0]))

# ---- 2. Verify walk arithmetic: eval each 'pre' that ends with '= ' expression ----
def evalpre(pre):
    # find rightmost 'EXPR = ' pattern
    txt = pre.replace("−","-").replace("×","*").replace("÷","/").replace(chr(8722),"-")
    m = re.search(r'([0-9().+\-*/ ]+?)\s*=\s*$', txt)
    if not m: return None
    expr = m.group(1).strip()
    if not re.match(r'^[0-9(). +\-*/]+$', expr): return None
    try: return eval(expr)
    except: return None

def check_walk(steps, tag):
    for j,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre = st.get("pre","")
        v = evalpre(pre)
        if v is not None:
            if abs(v - st["answer"])>1e-9:
                note("%s[%d] pre '%s' computes %s but answer=%s" % (tag,j,pre.strip(),v,st["answer"]))

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("guided_steps"):
            check_walk(p["guided_steps"], "%s[%d].gs"%(tier,i))
for t in ("bronze","silver","gold"):
    check_walk(pd["guided"]["teach"][t]["steps"], "teach.%s"%t)
check_walk(pd["guided"]["opener"]["steps"], "opener")

# ---- 3. Expect must not equal solution ----
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if isinstance(e,list) and len(e)==len(p["solutions"]):
                if all(abs(float(a)-float(b))<1e-9 for a,b in zip(e,p["solutions"])):
                    note("%s[%d] expect==sol %s"%(tier,i,e))

print("problems found:" if prob else "ALL CHECKS PASS")
for m in prob: print("  -",m)
