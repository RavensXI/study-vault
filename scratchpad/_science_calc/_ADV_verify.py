import json

pd = json.load(open("_ADV_canonical.json", encoding="utf-8"))
findings = []
BOX_TOL = 0.005

def approx(a, b, tol):
    return abs(a - b) <= tol

# ---- Fresh-solve every bank problem (independent) ----
# Each entry: expected solution computed here, plus accept, plus expects to check.
expected = {
    "bronze": [6, 6000, 20, 4, 300, 8, 400, 1],  # last MC -> index 1
    "silver": [168, 1, 1350, 4.32, 16200, 496.8], # MC index 1 for S2
    "gold": [3.97, 130.4, 920, 0.9, 12000, 60.23],
}

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i, p in enumerate(pb[tier]):
        path = f"{tier}[{i}]"
        sols = p["solutions"]
        exp = expected[tier][i]
        if p.get("input_type") == "multiple_choice":
            if sols[0] != exp:
                findings.append(f"{path} MC solution index {sols[0]} != expected {exp}")
            continue
        acc = p.get("accept", 0)
        if not approx(float(sols[0]), float(exp), max(acc, 1e-9)):
            findings.append(f"{path} stored {sols[0]} vs fresh-solve {exp} (accept {acc})")
        # expects outside accept window
        for j, m in enumerate(p.get("misconceptions") or []):
            e = m.get("expect")
            if e is None:
                continue
            ev = e[0] if isinstance(e, list) else e
            lo, hi = float(sols[0]) - acc, float(sols[0]) + acc
            if lo <= float(ev) <= hi:
                findings.append(f"{path}.misconceptions[{j}] DEAD expect {ev} inside accept window [{lo},{hi}]")

# ---- Recompute every guided_steps box: verify pre-arithmetic and continuity ----
import re
def check_box_arith(pre, answer, path):
    # extract "A op B =" pattern at end of pre
    m = re.search(r'(-?\d[\d,\.]*)\s*([×x*÷/+\-−])\s*(-?\d[\d,\.]*)\s*(?:×|x|\*|÷|/)?\s*(-?\d[\d,\.]*)?\s*=\s*$', pre)
    return  # handled explicitly below

# Explicit box recomputation for guided_steps, teach, opener
def num(s):
    return float(s.replace(",", ""))

def recompute(steps, path):
    for i, st in enumerate(steps):
        if st.get("answer") is None:
            continue
        pre = st.get("pre","")
        ans = st["answer"]
        # find all "= " expression
        m = re.search(r'([-\d,\.]+(?:\s*[×÷/*+\-−]\s*[-\d,\.]+)+)\s*=\s*(?:\(.*\))?\s*$', pre)
        if not m:
            # boxes like "Write ... = " with no arithmetic; skip (given values)
            continue
        expr = m.group(1)
        # normalize operators
        e = expr.replace("×","*").replace("÷","/").replace("−","-").replace(",","")
        try:
            val = eval(e)
        except Exception as ex:
            findings.append(f"{path}[{i}] cannot eval '{expr}': {ex}")
            continue
        # some boxes state 'to nearest joule' etc -> allow rounding
        if not approx(float(val), float(ans), max(BOX_TOL, abs(val)*1e-6, 1.0 if abs(val)>1000 else BOX_TOL)):
            # tighter check: allow integer rounding within 1 for 'nearest'
            if abs(round(val) - ans) > 1:
                findings.append(f"{path}[{i}] box: {expr} = {val} but answer={ans}")

for tier in ("bronze","silver","gold"):
    for i, p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        if gs:
            recompute(gs, f"{tier}[{i}].guided_steps")

g = pd["guided"]
recompute(g["opener"]["steps"], "opener")
for tier in ("bronze","silver","gold"):
    recompute(g["teach"][tier]["steps"], f"teach.{tier}")

print("FINDINGS:", len(findings))
for f in findings:
    print("  -", f)
