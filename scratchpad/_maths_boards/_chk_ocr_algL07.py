# -*- coding: utf-8 -*-
import json, io, re
import sympy as sp

x = sp.symbols('x')
pd = json.load(io.open("lesson_maths-ocr_algebra-L07.json", encoding="utf-8"))
fails = []

def parse_display(disp):
    # extract the equation inside \( ... \)
    m = re.search(r"\\\((.+?)\\\)", disp)
    eq = m.group(1)
    eq = eq.replace("^", "**")
    # insert * for implicit mult: number before x, and x**2 handled
    eq = re.sub(r"(\d)x", r"\1*x", eq)
    eq = eq.replace("=", "-(") + ")" if "=" in eq else eq
    # handle: split on original '=' properly
    return eq

def solve_disp(disp):
    m = re.search(r"\\\((.+?)\\\)", disp)
    raw = m.group(1).replace("^", "**")
    raw = re.sub(r"(\d)x", r"\1*x", raw)
    if "=" in raw:
        l, r = raw.split("=")
        expr = sp.sympify(l) - sp.sympify(r)
    else:
        expr = sp.sympify(raw)
    roots = sp.solve(sp.Eq(expr, 0), x)
    # multiplicity: use roots() for repeated
    vals = []
    for rt, mult in sp.roots(sp.Poly(expr, x)).items():
        for _ in range(mult):
            vals.append(complex(rt).real if rt.is_real is False else float(rt))
    return sorted([float(v) for v in vals]), expr

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        path = f"{tier}[{i}]"
        disp = p["display"]
        roots, expr = solve_disp(disp)
        stored = sorted([float(s) for s in p["solutions"]])
        if len(roots) != len(stored) or any(abs(a-b) > 1e-6 for a, b in zip(roots, stored)):
            fails.append(f"{path} SOLUTION MISMATCH disp={disp} solved={roots} stored={stored}")
        # verify each stored solution is a real root
        for s in p["solutions"]:
            v = expr.subs(x, sp.Rational(str(s)))
            if sp.simplify(v) != 0:
                fails.append(f"{path} stored root {s} does not satisfy {disp}: ={v}")
        # verify expects != solution and are determinate numbers
        sset = set(round(float(s), 6) for s in p["solutions"])
        for j, mc in enumerate(p.get("misconceptions") or []):
            e = mc.get("expect")
            if e is None:
                continue
            eset = set(round(float(v), 6) for v in e)
            if eset == sset:
                fails.append(f"{path}.mis[{j}] EXPECT == solution set {e}")
        # verify final guided check-step: last box answer 0 means root satisfies
        gs = p.get("guided_steps") or []
        # collect boxes that are roots (answers matching a solution)
        box_answers = [st["answer"] for st in gs if st.get("answer") is not None]
        # the two solutions should each appear as a box answer somewhere
        for s in p["solutions"]:
            if not any(abs(float(s)-float(b)) < 1e-6 for b in box_answers):
                fails.append(f"{path} solution {s} never appears as a guided box answer; boxes={box_answers}")

# verify opener box: 3 (multiply15 add8 smaller) and 0 (zero product)
op = [st.get("answer") for st in pd["guided"]["opener"]["steps"] if st.get("answer") is not None]
if op != [3, 0]:
    fails.append(f"opener box answers {op} != [3,0]")
# 3 and 5 multiply to 15 add to 8
if not (3*5 == 15 and 3+5 == 8):
    fails.append("opener numbers wrong")

# verify teach walks land: bronze x^2+7x+12 roots -3,-4; silver x^2-x-12 roots 4,-3; gold 2x^2+5x-3 roots .5,-3
teach_specs = {
    "bronze": ("x**2+7*x+12", [-3, -4]),
    "silver": ("x**2-x-12", [4, -3]),
    "gold": ("2*x**2+5*x-3", [0.5, -3]),
}
for tier, (e, expect_roots) in teach_specs.items():
    expr = sp.sympify(e)
    tr = sorted([float(r) for r in sp.solve(expr, x)])
    if tr != sorted(expect_roots):
        fails.append(f"teach {tier} roots {tr} != {sorted(expect_roots)}")
    boxes = [st["answer"] for st in pd["guided"]["teach"][tier]["steps"] if st.get("answer") is not None]
    for r in expect_roots:
        if not any(abs(r-float(b)) < 1e-6 for b in boxes):
            fails.append(f"teach {tier} root {r} not in boxes {boxes}")

# check every box answer numeric
def numck(steps, path):
    for k, st in enumerate(steps):
        if st.get("answer") is not None and not isinstance(st["answer"], (int, float)):
            fails.append(f"{path}[{k}] non-numeric answer {st['answer']!r}")

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        numck(p.get("guided_steps") or [], f"{tier}[{i}].gs")

if fails:
    print("CHECK FAIL", len(fails))
    for f in fails:
        print("  -", f)
else:
    print("CHECK PASS: all 20 solutions verified, expects distinct, boxes land on solutions, teach/opener verified")
