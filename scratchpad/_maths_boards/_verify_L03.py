# -*- coding: utf-8 -*-
import json, re
import sympy as sp

x, a, m, p, y = sp.symbols('x a m p y')
SYMS = {'x': x, 'a': a, 'm': m, 'p': p, 'y': y}

def to_expr(latex):
    s = latex.replace("\\(", "").replace("\\)", "")
    s = s.replace("Factorise completely", "").replace("Factorise", "").strip()
    s = s.replace("−", "-")
    s = re.sub(r"\^2", "**2", s)
    s = re.sub(r"\^3", "**3", s)
    s = s.replace("^", "**")
    # insert * for implicit multiplication: number|letter followed by ( ; ) followed by ( ; letter/number adjacency
    s = re.sub(r"(\d)([a-zA-Z(])", r"\1*\2", s)      # 3x, 3(, 4a
    s = re.sub(r"([a-zA-Z])\(", r"\1*(", s)          # x(
    s = re.sub(r"\)\(", r")*(", s)                    # )(
    s = re.sub(r"\)([a-zA-Z0-9])", r")*\1", s)        # )x
    s = re.sub(r"([a-zA-Z])([a-zA-Z])", r"\1*\2", s)  # rare
    return sp.expand(sp.sympify(s, locals=SYMS))

pd = json.load(open("lesson_maths-eduqas_algebra-L03.json", encoding="utf-8"))
ok = True
for tier in ("bronze", "silver", "gold"):
    for i, prob in enumerate(pd["problem_bank"][tier]):
        target = to_expr(prob["display"])
        opts = [to_expr(o) for o in prob["options"]]
        sol = prob["solutions"][0]
        # correct option equals target
        if sp.simplify(opts[sol] - target) != 0:
            print("FAIL %s[%d] correct option %d != display: %s vs %s" % (tier, i, sol, opts[sol], target)); ok = False
        # each other option must NOT equal target (distractor genuinely wrong)
        for j, o in enumerate(opts):
            if j != sol and sp.simplify(o - target) == 0:
                # allowed only if it's a not-fully-factorised equal-value distractor; flag it
                print("NOTE %s[%d] option %d equals value of display (unfactorised distractor): %s" % (tier, i, j, prob["options"][j]))
        # misconception expects point to wrong options, never the correct one
        for mc in prob.get("misconceptions", []):
            e = mc["expect"]
            if e == sol:
                print("FAIL %s[%d] misconception expect == correct index" % (tier, i)); ok = False
            if not (0 <= e < len(opts)):
                print("FAIL %s[%d] expect out of range: %d" % (tier, i, e)); ok = False
print("ALL GOOD" if ok else "PROBLEMS FOUND")
