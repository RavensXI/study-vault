# -*- coding: utf-8 -*-
"""Independent verification: fresh-solve every problem, re-eval every guided box."""
import json, io, re

pd = json.load(io.open("lesson_higher-calculations-L01@b5d94e42c2.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# ---- 1. Fresh-solve each problem independently from first principles ----
expected = {
    # tier, idx : (answer, unit)
    ("bronze", 0): 0.1 * (25.0 / 1000),                 # n=cV
    ("bronze", 1): 0.5 / 0.25,                          # c=n/V
    ("bronze", 2): 0.2 / 0.5,                           # V=n/c
    ("bronze", 3): 4.0 / (23 + 16 + 1),                 # n=mass/Mr
    ("bronze", 4): 0.15 / (500 / 1000),                 # c=n/V
    ("bronze", 5): 0.25 * (100 / 1000),                 # n=cV
    ("bronze", 6): 50 / 1000,                           # convert
    ("bronze", 7): 2.0 / (1 + 35.5),                    # n=mass/Mr
    ("silver", 0): (0.125 * 0.02) / 0.025,              # 1:1
    ("silver", 1): (0.2 * 0.025 / 2) / 0.02,            # 1:2
    ("silver", 2): (0.15 * 0.025) / 0.01875,            # 1:1
    ("silver", 3): (0.1 * 0.025 * 2) / 0.02,            # 1:2
    ("silver", 4): (0.2 * 0.025) / 0.0125,              # 1:1 (edited)
    ("silver", 5): (0.5 * 0.025 / 2) / 0.0125,          # 1:2 (edited)
    ("gold", 0): ((2.0 / 40 / 0.2) * 0.025) / (31.25 / 1000),          # NaOH flask->sample->HCl
    ("gold", 1): (((5.3 / 106) / 0.25) * 0.025 * 2) / 0.025,           # Na2CO3 1:2
    ("gold", 2): (0.5 * 0.25) * 36.5,                                  # mass HCl
    ("gold", 3): ((0.1 * 0.02) / 0.025 * 0.5) * 56,                    # mass KOH
    ("gold", 4): ((0.2 * 0.02) / 0.025 * 0.25) * 40,                   # mass NaOH
    ("gold", 5): ((0.1 * 0.0125) / 0.025 * 0.5) * 106,                # mass Na2CO3
}
for (tier, idx), val in expected.items():
    p = pb[tier][idx]
    sol = p["solutions"][0]
    acc = p.get("accept", 0.005)
    if abs(val - sol) > max(acc, 1e-9) + 1e-9:
        errs.append(f"{tier}[{idx}] stored {sol} but fresh-solve {val:.6g} (accept {acc})")

# ---- 2. Duplicate solutions per tier ----
for tier in ("bronze", "silver", "gold"):
    seen = {}
    for i, p in enumerate(pb[tier]):
        k = tuple(p["solutions"])
        if k in seen:
            errs.append(f"{tier}[{i}] duplicate solution {k} (also {tier}[{seen[k]}])")
        seen[k] = i

# ---- 3. Expects: numeric, outside accept window, != solution ----
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        sol = p["solutions"][0]
        acc = p.get("accept", 0.0)
        for j, m in enumerate(p.get("misconceptions", [])):
            if "expect" not in m:
                errs.append(f"{tier}[{i}].mis[{j}] missing expect key")
                continue
            e = m["expect"]
            if e is None:
                continue
            ev = e[0] if isinstance(e, list) else e
            if abs(ev - sol) <= acc + 1e-9:
                errs.append(f"{tier}[{i}].mis[{j}] expect {ev} inside accept window of {sol}")
            if abs(ev - sol) < 0.011:
                errs.append(f"{tier}[{i}].mis[{j}] expect {ev} == solution {sol}")

# ---- 4. Re-evaluate every guided box arithmetic 'A op B [op C] = ' in pre ----
OPS = {"×": lambda a, b: a * b, "÷": lambda a, b: a / b, "+": lambda a, b: a + b, "−": lambda a, b: a - b}
num_re = re.compile(r"-?\d+\.?\d*")

def eval_pre(pre):
    """Find the last 'expr = ' in pre and evaluate expr if it is a simple chain."""
    if "=" not in pre:
        return None
    left = pre.rsplit("=", 1)[0]
    # take the trailing arithmetic chain: tokens of number/op
    # normalise: keep only the final chain after last ':' or 'so' etc
    # grab a window: last chain of  num op num (op num)*
    m = re.search(r"(-?\d+\.?\d*)\s*([×÷+−])\s*(-?\d+\.?\d*)(?:\s*([×÷+−])\s*(-?\d+\.?\d*))?\s*$", left.strip())
    if not m:
        return None
    a = float(m.group(1)); op1 = m.group(2); b = float(m.group(3))
    v = OPS[op1](a, b)
    if m.group(4):
        v = OPS[m.group(4)](v, float(m.group(5)))
    return v

def check_walk(steps, label):
    boxc = 0
    for k, st in enumerate(steps):
        if st.get("answer") is None:
            continue
        boxc += 1
        pre = st.get("pre", "")
        v = eval_pre(pre)
        if v is not None:
            if abs(v - st["answer"]) > 0.005:
                errs.append(f"{label} box[{k}] pre '{pre.strip()}' evaluates {v:.6g} != answer {st['answer']}")
    return boxc

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        if gs:
            nb = check_walk(gs, f"{tier}[{i}].guided_steps")
            # final live box (excluding the check) should land on solution somewhere
            live_answers = [st["answer"] for st in gs if st.get("answer") is not None]
            if p["solutions"][0] not in [round(a, 6) for a in live_answers] and \
               not any(abs(a - p["solutions"][0]) <= p.get("accept", 0.005) for a in live_answers):
                errs.append(f"{tier}[{i}] solution {p['solutions'][0]} not among walk boxes {live_answers}")

# opener + teach
check_walk(pd["guided"]["opener"]["steps"], "opener")
for tier in ("bronze", "silver", "gold"):
    check_walk(pd["guided"]["teach"][tier]["steps"], f"teach.{tier}")

# ---- 5. board-neutrality + em dash scan on student-facing strings ----
def scan(obj, path):
    if isinstance(obj, dict):
        for kk, vv in obj.items():
            if kk in ("note", "guided_skip_reason"):
                continue
            scan(vv, path + "." + str(kk))
    elif isinstance(obj, list):
        for ii, vv in enumerate(obj):
            scan(vv, f"{path}[{ii}]")
    elif isinstance(obj, str):
        if "—" in obj:
            errs.append(f"em dash at {path}")
        low = obj.lower()
        for bad in ("aqa", "edexcel", "ocr", "equation sheet", "on your sheet", "you must memorise"):
            if bad in low:
                errs.append(f"board-specific phrase '{bad}' at {path}: {obj[:60]}")
scan(pd, "pd")

print("PROBLEMS FRESH-SOLVED:", len(expected))
if errs:
    print("FAIL", len(errs))
    for e in errs:
        print("  -", e)
else:
    print("ALL INDEPENDENT CHECKS PASS")
