# -*- coding: utf-8 -*-
"""Adversarial self-check of the built shard: fresh-solve bank, recompute every
guided-step box that states explicit arithmetic, check misconception expects."""
import io, json, re
from fractions import Fraction as Fr

pd = json.load(io.open("lesson_maths-ocr_probability-statistics-L01.json", encoding="utf-8"))
live = json.load(io.open("_ps01_live.json", encoding="utf-8"))
errs = []

# 1) solutions unchanged vs live
for tier in ("bronze", "silver", "gold"):
    for i, (p, lp) in enumerate(zip(pd["problem_bank"][tier], live["problem_bank"][tier])):
        if p["solutions"] != lp["solutions"]:
            errs.append("%s[%d] solutions changed %s -> %s" % (tier, i, lp["solutions"], p["solutions"]))

# 2) fresh-solve each problem from intent (hard-coded independent recompute)
def fr(n, d): return Fr(n, d)
expect_sol = {
 ("bronze",0): [1,5], ("bronze",1): [1,2], ("bronze",2): [1,4], ("bronze",3): [0.7],
 ("bronze",4): [3,8], ("bronze",5): [3,5], ("bronze",6): [4,5], ("bronze",7): [1,3],
 ("silver",0): [1,2], ("silver",1): [25,64], ("silver",2): [5,14], ("silver",3): [0.12],
 ("silver",4): [1,6], ("silver",5): [0.4], ("silver",6): [8,15],
 ("gold",0): [14,55], ("gold",1): [0.58], ("gold",2): [1,8], ("gold",3): [3,8], ("gold",4): [5,33],
}
# independent computations
comp = {
 ("bronze",0): fr(2,10), ("bronze",1): fr(3,6), ("bronze",2): fr(13,52), ("bronze",3): 1-0.3,
 ("bronze",4): fr(3,8), ("bronze",5): fr(3,5), ("bronze",6): fr(8,10), ("bronze",7): fr(2,6),
 ("silver",0): fr(2,4), ("silver",1): fr(5,8)*fr(5,8), ("silver",2): fr(5,8)*fr(4,7),
 ("silver",3): 0.4*0.3, ("silver",4): fr(6,36), ("silver",5): 1-0.6,
 ("silver",6): fr(6,10)*fr(4,9)+fr(4,10)*fr(6,9),
 ("gold",0): fr(8,12)*fr(7,11)*fr(6,10), ("gold",1): 1-(1-0.3)*(1-0.4),
 ("gold",2): fr(1,2)**3, ("gold",3): fr(3,8), ("gold",4): fr(5,12)*fr(4,11),
}
for key, sol in expect_sol.items():
    got = pd["problem_bank"][key[0]][key[1]]["solutions"]
    if got != sol:
        errs.append("%s stored %s != intended %s" % (key, got, sol))
    c = comp[key]
    if isinstance(c, Fr):
        if [c.numerator, c.denominator] != sol:
            errs.append("%s recompute %s != %s" % (key, c, sol))
    else:
        if abs(round(c, 6) - sol[0]) > 1e-9:
            errs.append("%s recompute %s != %s" % (key, c, sol))

# 3) recompute every guided-step box stating explicit "a op b [op c] = "
op = {'+': lambda a, b: a+b, '−': lambda a, b: a-b, '×': lambda a, b: a*b, '÷': lambda a, b: a/b}
pat2 = re.compile(r'(-?\d+\.?\d*)\s*([+−×÷])\s*(-?\d+\.?\d*)\s*(?:([+−×÷])\s*(-?\d+\.?\d*)\s*)?=\s*$')
def num(s):
    f = float(s); return int(f) if f == int(f) else f
def check_steps(steps, tag):
    for j, st in enumerate(steps):
        if st.get("answer") is None: continue
        pre = st.get("pre", "")
        m = pat2.search(pre)
        if not m: continue
        a = num(m.group(1)); o1 = m.group(2); b = num(m.group(3))
        val = op[o1](a, b)
        if m.group(4):
            val = op[m.group(4)](val, num(m.group(5)))
        val = round(val, 6)
        ans = st["answer"]
        if abs(val - ans) > 1e-9:
            errs.append("%s[%d] pre '%s' computes %s but answer=%s" % (tag, j, pre.strip(), val, ans))

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        check_steps(p.get("guided_steps", []), "%s[%d].gs" % (tier, i))
check_steps(pd["guided"]["opener"]["steps"], "opener")
for t in ("bronze", "silver", "gold"):
    check_steps(pd["guided"]["teach"][t]["steps"], "teach."+t)

# 4) misconception expects: present, != solution, list length matches
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        sol = p["solutions"]
        for k, m in enumerate(p.get("misconceptions", [])):
            if "expect" not in m:
                errs.append("%s[%d].mis[%d] missing expect" % (tier, i, k)); continue
            e = m["expect"]
            ev = e if isinstance(e, list) else [e]
            if len(ev) == len(sol) and all(abs(float(a)-float(b)) < 0.011 for a, b in zip(ev, sol)):
                errs.append("%s[%d].mis[%d] expect==solution %s" % (tier, i, k, e))

# 5) style: no em dash anywhere student-facing (validator does this too)
def scan(o, path):
    if isinstance(o, dict):
        for kk, vv in o.items():
            if kk in ("note",): continue
            scan(vv, path+"."+str(kk))
    elif isinstance(o, list):
        for ii, vv in enumerate(o): scan(vv, "%s[%d]" % (path, ii))
    elif isinstance(o, str) and "—" in o:
        errs.append("EM DASH at "+path)
scan(pd, "pd")

# 6) preservation of untouched fields vs live
for f in ("worked_examples", "related_videos"):
    if pd.get(f) != live.get(f):
        errs.append("field %s changed vs live" % f)

if errs:
    print("FAIL", len(errs))
    for e in errs: print("  -", e)
else:
    print("ALL CHECKS PASS: solutions match, every explicit box computes, expects clean, no em dash, preserved fields intact")
    # count figures
    figs = 0
    for tier in ("bronze","silver","gold"):
        for p in pd["problem_bank"][tier]:
            if "<svg" in p.get("display",""): figs += 1
    figs += 1  # opener bag
    for t in ("bronze","silver","gold"):
        if "<svg" in pd["guided"]["teach"][t]["display"]: figs += 1
    print("figures with svg:", figs)
