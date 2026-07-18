# -*- coding: utf-8 -*-
import json, re

with open("_CK03_canonical.json", encoding="utf-8") as f:
    pd = json.load(f)

problems = []

def expr_eval(s):
    # extract the arithmetic portion before '=' , normalise symbols
    # take substring: last '=' means result; we want left of the trailing '='
    if "=" not in s:
        return None
    left = s.rsplit("=", 1)[0]
    # If there are multiple '=', e.g. "Mean = 40 ÷ 5 =" -> take part after first '='? messy.
    # Grab the rightmost arithmetic chunk: find last '=' segment before final '='
    parts = [p for p in s.split("=")]
    # candidate expression = the segment just before the final empty/whitespace
    cand = None
    for seg in parts:
        seg2 = seg.strip()
        if re.search(r"[0-9].*[×÷+\-−].*[0-9]", seg2):
            cand = seg2
    if cand is None:
        return None
    e = cand
    e = e.replace("×", "*").replace("÷", "/").replace("−", "-").replace(",", "")
    # strip any leading label words (keep only from first digit or '(' )
    m = re.search(r"[\(\-]?\s*\d.*$", e)
    if not m:
        return None
    e = e[m.start():]
    # remove trailing non-expression tokens like '(to 3 d.p.)'
    e = re.sub(r"\(to.*?\)", "", e)
    e = e.strip()
    # keep only allowed chars
    if not re.fullmatch(r"[0-9\.\+\-\*/() ]+", e):
        return None
    try:
        return eval(e, {"__builtins__": {}})
    except Exception:
        return None

def check_steps(steps, label):
    for i, st in enumerate(steps):
        if st.get("answer") is None:
            continue
        pre = st.get("pre", "")
        val = expr_eval(pre)
        ans = st["answer"]
        if val is not None:
            if abs(val - ans) > 0.005:
                print(f"BOX MISMATCH {label}[{i}] pre={pre!r} eval={val} stored={ans}")

# teach walks
for tier, t in pd["guided"]["teach"].items():
    check_steps(t["steps"], f"teach.{tier}")
# opener
check_steps(pd["guided"]["opener"]["steps"], "opener")

# bank
for tier, probs in pd["problem_bank"].items():
    if tier.endswith("_description"):
        continue
    for pi, p in enumerate(probs):
        gs = p.get("guided_steps")
        if gs:
            check_steps(gs, f"{tier}[{pi}].gs")

print("--- expects vs accept windows ---")
for tier, probs in pd["problem_bank"].items():
    if tier.endswith("_description"):
        continue
    for pi, p in enumerate(probs):
        sols = p.get("solutions")
        accept = p.get("accept", 0)
        for mi, m in enumerate(p.get("misconceptions", [])):
            e = m.get("expect")
            if e is None:
                continue
            if isinstance(sols, list) and len(sols) == 1 and isinstance(e, (int, float)):
                if abs(e - sols[0]) <= accept + 1e-9:
                    print(f"DEAD EXPECT {tier}[{pi}].misc[{mi}] expect={e} sol={sols[0]} accept={accept}")
print("recompute done")
