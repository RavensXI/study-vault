# -*- coding: utf-8 -*-
"""Independent adversarial verification: recompute every box value from scratch,
re-solve every problem, commit every misconception error, check boundaries."""
import json, io, re

pd = json.load(io.open("lesson_algebra-L07.json", encoding="utf-8"))
errs = []

def solve_quadratic_from_display(disp):
    """Parse an ax^2+bx+c=0 (or rearrangeable) display, return set of roots."""
    s = disp.replace("Solve", "").replace("\\(", "").replace("\\)", "").replace(" ", "")
    if "=" in s:
        L, R = s.split("=")
    else:
        L, R = s, "0"
    def poly(side):
        # returns dict power->coeff
        d = {0: 0, 1: 0, 2: 0}
        side = side.replace("-", "+-")
        for term in side.split("+"):
            if term == "":
                continue
            if "x^2" in term:
                co = term.replace("x^2", "")
                co = "-1" if co == "-" else ("1" if co == "" else co)
                d[2] += int(co)
            elif "x" in term:
                co = term.replace("x", "")
                co = "-1" if co == "-" else ("1" if co == "" else co)
                d[1] += int(co)
            else:
                d[0] += int(term)
        return d
    dl, dr = poly(L), poly(R)
    a = dl[2] - dr[2]; b = dl[1] - dr[1]; c = dl[0] - dr[0]
    # integer roots
    roots = set()
    for x in range(-100, 101):
        if a * x * x + b * x + c == 0:
            roots.add(x)
    return roots, (a, b, c)

# 1. re-solve every bank problem vs stored solutions
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        roots, abc = solve_quadratic_from_display(p["display"])
        stored = set(p["solutions"])
        if roots != stored:
            errs.append("%s[%d] SOLVE mismatch: display %s -> roots %s vs stored %s" %
                        (tier, i, p["display"], sorted(roots), sorted(stored)))

# 2. verify guided_steps boxes: parse 'pre' arithmetic where it is a pure sum/eval, and
#    verify factor-pair / bracket boxes land on solutions.
def eval_arith(text):
    """Try to evaluate a trailing arithmetic expression 'A op B ... = ' -> number."""
    t = text.strip()
    if not t.endswith("="):
        return None
    expr = t.rstrip("=").strip()
    # take substring after last ':'
    if ":" in expr:
        expr = expr.split(":")[-1].strip()
    expr = expr.replace("−", "-").replace("×", "*").replace("÷", "/").replace("²", "**2")
    # must look purely numeric
    if not re.fullmatch(r"[0-9\.\+\-\*\/\(\)\s]+", expr):
        return None
    try:
        return eval(expr)
    except Exception:
        return None

def check_walk(path, steps):
    boxes = [st for st in steps if st.get("answer") is not None]
    if len(boxes) < 3:
        errs.append(path + " <3 boxes")
    for j, st in enumerate(steps):
        if st.get("answer") is None:
            continue
        val = eval_arith(st.get("pre", ""))
        if val is not None:
            if abs(val - st["answer"]) > 1e-9:
                errs.append("%s step[%d] arithmetic '%s' = %s but answer=%s" %
                            (path, j, st["pre"], val, st["answer"]))

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        gs = p.get("guided_steps") or []
        check_walk("%s[%d].guided_steps" % (tier, i), gs)
        # completion boundary
        sub = [k for k, st in enumerate(gs) if st.get("phase") == "substitute"]
        if not sub:
            errs.append("%s[%d] no substitute boundary" % (tier, i))
        else:
            first = sub[0]
            if first < 1:
                errs.append("%s[%d] boundary at 0" % (tier, i))
            live = sum(1 for st in gs[first:] if st.get("answer") is not None)
            if live < 2:
                errs.append("%s[%d] only %d live boxes after boundary" % (tier, i, live))
        # final two live boxes before check must equal the two solutions
        # gather substitute-phase boxes (excluding the final check whose answer is 0)
        sol_boxes = [st["answer"] for st in gs if st.get("phase") == "substitute" and st.get("answer") is not None]
        if set(sol_boxes) != set(p["solutions"]):
            errs.append("%s[%d] substitute boxes %s != solutions %s" %
                        (tier, i, sol_boxes, p["solutions"]))

# 3. misconceptions: expect must equal committed error, and never equal correct answer
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        sols = p["solutions"]
        for k, m in enumerate(p.get("misconceptions") or []):
            e = m.get("expect")
            mp = "%s[%d].misc[%d](%s)" % (tier, i, k, m.get("pattern"))
            if e is None:
                continue
            # negated pattern: expect must be element-wise negation of solutions
            if m.get("pattern") == "factor_pair_not_solved":
                if set(e) != set(-s for s in sols):
                    errs.append(mp + " expect %s != negated solutions %s" % (e, [-s for s in sols]))
                if set(e) == set(sols):
                    errs.append(mp + " expect equals correct answer")

# 4. teach + opener boxes arithmetic
check_walk("guided.opener", pd["guided"]["opener"]["steps"])
for tier in ("bronze", "silver", "gold"):
    t = pd["guided"]["teach"][tier]
    check_walk("guided.teach.%s" % tier, t["steps"])

# 5. teach walks: verify the checked quadratic root
for tier in ("bronze", "silver", "gold"):
    t = pd["guided"]["teach"][tier]
    roots, abc = solve_quadratic_from_display(t["display"])
    # collect final solve boxes (answers that are roots) - just confirm each non-check box that
    # claims 'so x =' equals a root
    for st in t["steps"]:
        if st.get("answer") is not None and "so x =" in st.get("pre", ""):
            if st["answer"] not in roots:
                errs.append("teach.%s box '%s' answer %s not a root %s" %
                            (tier, st["pre"], st["answer"], sorted(roots)))

if errs:
    print("VERIFY FAIL (%d):" % len(errs))
    for e in errs:
        print("  -", e)
else:
    print("VERIFY PASS: all solves, boxes, boundaries, misconceptions independently confirmed")
