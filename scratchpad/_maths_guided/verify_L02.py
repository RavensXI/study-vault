# -*- coding: utf-8 -*-
import json, io, re

pd = json.load(io.open("lesson_probability-statistics-L02.json", encoding="utf-8"))

def norm(s):
    return (s.replace("−", "-").replace("×", "*").replace("÷", "/")
             .replace("−", "-"))

# Extract the LAST "expr = " arithmetic from a pre string and eval it.
expr_re = re.compile(r"([0-9().+\-*/ ]+?)\s*=\s*$")

def check_box(pre, ans, path, problems):
    p = norm(pre).strip()
    m = expr_re.search(p)
    if not m:
        return  # no evaluable trailing arithmetic (verbal box)
    expr = m.group(1).strip()
    # must contain an operator to be an arithmetic check
    if not re.search(r"[+\-*/]", expr):
        return
    try:
        val = eval(expr, {"__builtins__": {}})
    except Exception as e:
        problems.append(f"{path}: could not eval '{expr}': {e}")
        return
    if abs(float(val) - float(ans)) > 1e-9:
        problems.append(f"{path}: '{expr}' = {val} but answer stored {ans}")

problems = []

def walk(steps, path):
    for i, st in enumerate(steps):
        if st.get("answer") is not None and st.get("pre"):
            check_box(st["pre"], st["answer"], f"{path}[{i}]", problems)

for tier in ("gold", "bronze", "silver"):
    for j, prob in enumerate(pd["problem_bank"][tier]):
        gs = prob.get("guided_steps")
        if gs: walk(gs, f"{tier}[{j}].guided_steps")

walk(pd["guided"]["opener"]["steps"], "opener")
for t in ("bronze", "silver", "gold"):
    walk(pd["guided"]["teach"][t]["steps"], f"teach.{t}")

# Final-answer landing: last answer box(es) must match solutions for single/fraction
def last_boxes(gs, n):
    vals = [s["answer"] for s in gs if s.get("answer") is not None]
    return vals

for tier in ("gold", "bronze", "silver"):
    for j, prob in enumerate(pd["problem_bank"][tier]):
        gs = prob.get("guided_steps")
        if not gs: continue
        sols = prob["solutions"]
        it = prob.get("input_type", "single_value")
        vals = last_boxes(gs, len(sols))
        # the solution value(s) must appear among the boxes (answer is produced, check follows)
        for s in sols:
            if not any(abs(float(v) - float(s)) < 1e-9 for v in vals):
                problems.append(f"{tier}[{j}]: solution {s} not produced by any box")

# Misconception expects must NOT equal solution (validator already checks), and be present
for tier in ("gold", "bronze", "silver"):
    for j, prob in enumerate(pd["problem_bank"][tier]):
        for k, m in enumerate(prob.get("misconceptions", [])):
            if "expect" not in m:
                problems.append(f"{tier}[{j}].misc[{k}] missing expect")

if problems:
    print("ISSUES:")
    for p in problems: print("  -", p)
else:
    print("ALL ARITHMETIC BOXES VERIFIED, all solutions produced, all expects present")
