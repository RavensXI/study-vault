# -*- coding: utf-8 -*-
import json, re

pd = json.load(open("_QA_canonical.json", encoding="utf-8"))

# Normalise unicode math operators to python
def normops(s):
    return (s.replace("×", "*").replace("÷", "/").replace("−", "-")
             .replace("₀","0").replace("₁","1").replace("₂","2").replace("₃","3")
             .replace("₄","4").replace("₅","5").replace("₆","6").replace("₇","7")
             .replace("₈","8").replace("₉","9"))

# Extract the LAST "expr =" arithmetic from a pre string and evaluate it.
# We look for a trailing arithmetic expression ending in '='.
ARITH = re.compile(r'([0-9()\.\s\*/\+\-]+)=\s*$')

issues = []

def check_steps(steps, path):
    for i, st in enumerate(steps):
        ans = st.get("answer")
        if ans is None:
            continue
        pre = normops(st.get("pre",""))
        m = ARITH.search(pre.strip())
        if not m:
            # no explicit arithmetic to check; skip (value asserted, not computed)
            continue
        expr = m.group(1).strip()
        # must contain an operator to be a real computation
        if not re.search(r'[\*/\+\-]', expr):
            continue
        try:
            val = eval(expr)
        except Exception as e:
            issues.append("%s[%d] cannot eval '%s': %s" % (path,i,expr,e))
            continue
        if abs(val - ans) > 0.005:
            issues.append("%s[%d] pre '%s' = %s but answer=%s" % (path,i,expr,val,ans))

# teach walks
for tier in ("bronze","silver","gold"):
    t = pd["guided"]["teach"][tier]
    check_steps(t["steps"], "teach."+tier)
# opener
check_steps(pd["guided"]["opener"]["steps"], "opener")
# problem bank guided steps + misconceptions
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for idx, p in enumerate(pb[tier]):
        gp = "%s[%d]" % (tier, idx)
        if p.get("guided_steps"):
            check_steps(p["guided_steps"], gp+".gs")
        sols = p.get("solutions")
        acc = p.get("accept")
        for j,m in enumerate(p.get("misconceptions") or []):
            e = m.get("expect")
            if e is None: continue
            ev = e if isinstance(e,list) else [e]
            # dead-expect: does expect fall inside accept window of solution?
            if sols and len(ev)==len(sols):
                for a,b in zip(ev,sols):
                    tol = acc if acc is not None else 0.005
                    if abs(float(a)-float(b)) <= tol:
                        issues.append("%s.misc[%d] DEAD expect %s inside accept(%s) of sol %s"%(gp,j,a,tol,b))

# Final box in each guided walk must equal a stored solution (landing check)
for tier in ("bronze","silver","gold"):
    for idx,p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        if not gs: continue
        boxes = [s["answer"] for s in gs if s.get("answer") is not None]
        sol = p["solutions"][0]
        if sol not in [round(b,6) for b in boxes]:
            issues.append("%s[%d] solution %s not hit by any box %s"%(tier,idx,sol,boxes))

print("ARITHMETIC/EXPECT ISSUES:", len(issues))
for x in issues:
    print("  -", x)

# Board-neutrality scan
import io
raw = json.dumps(pd, ensure_ascii=False).lower()
for bad in ["aqa","edexcel","ocr","eduqas","wjec","equation sheet","memorise","memorize","on your data sheet","given to you in the exam"]:
    if bad in raw:
        # find context
        i = raw.find(bad)
        print("BOARD-FLAG:", bad, "...", raw[max(0,i-40):i+40])
print("board scan done")
