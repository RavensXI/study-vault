# -*- coding: utf-8 -*-
import json, io, re
import sympy as sp

pd = json.load(io.open("lesson_maths-aqa_algebra-L02.json", encoding="utf-8"))
x, y = sp.symbols('x y')
s3 = sp.sqrt(3)
errs = []

def latex_to_expr(s):
    s = s.replace("\\(", "").replace("\\)", "").strip()
    s = s.replace("\\sqrt{3}", "sqrt3")
    s = re.sub(r'([0-9a-zA-Z\)])\^([0-9]+)', r'\1**\2', s)
    s = s.replace("^", "**")
    # insert * between number/paren and variable
    s = re.sub(r'(\d)([xy(])', r'\1*\2', s)
    s = re.sub(r'([xy0-9\)])\s*\(', r'\1*(', s)
    s = s.replace("sqrt3", "sqrt3")
    return sp.sympify(s, locals={"x": x, "y": y, "sqrt3": s3})

# True expansions keyed by display -> expected expanded expr
def expand_display(d):
    d = d.replace("Expand and simplify", "").replace("Expand", "").strip()
    # take the leading math expression up to first period
    m = re.search(r'\\\((.+?)\\\)(?!.*\\\()', d)  # last? just handle special-case below
    return None

pb = pd["problem_bank"]
# Verify MC correct option == true expansion, computed from display
def true_expansion(display):
    core = re.findall(r'\\\((.+?)\\\)', display)[0]
    core = core.replace("\\sqrt{3}", "sqrt3")
    core = re.sub(r'([0-9a-zA-Z\)])\^([0-9]+)', r'\1**\2', core)
    core = core.replace("^", "**")
    core = re.sub(r'(\d)([xy(])', r'\1*\2', core)
    core = re.sub(r'([xy0-9\)])\s*\(', r'\1*(', core)
    e = sp.sympify(core, locals={"x": x, "y": y, "sqrt3": s3})
    return sp.expand(e)

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        path = f"{tier}[{i}]"
        it = p.get("input_type")
        if it == "multiple_choice":
            opts = p["options"]
            sol = p["solutions"][0]
            # true expansion of the display expression
            disp = p["display"]
            # gold[2] triple / etc all fine
            try:
                te = true_expansion(disp)
                co = sp.expand(latex_to_expr(opts[sol]))
                if sp.simplify(te - co) != 0:
                    errs.append(f"{path}: correct option {sol} '{opts[sol]}' != true expansion {te}")
            except Exception as ex:
                errs.append(f"{path}: parse error {ex} on {disp}")
            # misconceptions: expect must be a valid distractor index != sol
            for m in p.get("misconceptions", []):
                e = m["expect"]
                if e == sol:
                    errs.append(f"{path}: expect {e} equals correct index")
                if not (0 <= e < len(opts)):
                    errs.append(f"{path}: expect {e} out of range")
        else:
            # single_value gold[3]
            pass

# gold[3] single_value: verify a=4
g3 = pb["gold"][3]
lhs = sp.expand((x+4)**2 - (x+2)**2)
a_coeff = lhs.coeff(x, 1); b_coeff = lhs.coeff(x, 0)
if a_coeff != 4 or g3["solutions"][0] != 4:
    errs.append(f"gold[3]: a should be 4, got {a_coeff}, stored {g3['solutions']}")
if b_coeff != 12:
    errs.append(f"gold[3]: b should be 12, got {b_coeff}")

# Verify guided_steps walks numerically where they involve pure arithmetic checks
def check_boxes(steps, path):
    for j, st in enumerate(steps):
        if st.get("answer") is None:
            continue
        pre = (st.get("pre") or "")
        # try to evaluate arithmetic in pre like "3 × 10 = " or "15 + (−4) = "
        expr = pre
        expr = expr.split("=")[0] if "=" in expr else expr
        # normalise
        e = expr.replace("×", "*").replace("−", "-").replace("(", "(").replace(")", ")")
        e = e.replace("²", "**2")
        # keep only trailing arithmetic after last ':'
        if ":" in e:
            e = e.split(":")[-1]
        e = e.strip()
        # remove leading labels words
        m = re.search(r'[-+(]?\s*[\d().+\-*/ ]+$', e)
        if m:
            frag = m.group(0).strip()
            try:
                val = eval(frag)
                if abs(val - st["answer"]) > 1e-9:
                    # not all pre are pure arithmetic; only flag clear numeric ones
                    if re.fullmatch(r'[-+(). \d*/]+', frag):
                        errs.append(f"{path}[{j}]: '{frag}' = {val} but answer {st['answer']}")
            except Exception:
                pass

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("guided_steps"):
            check_boxes(p["guided_steps"], f"{tier}[{i}].guided_steps")
check_boxes(pd["guided"]["opener"]["steps"], "opener")
for t in ("bronze","silver","gold"):
    check_boxes(pd["guided"]["teach"][t]["steps"], f"teach.{t}")

# tier guide word budgets
def words(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
for t in ("bronze","silver","gold"):
    tot = sum(words(s) for s in pd["tier_guides"][t]["steps"])
    print(f"tier_guide {t} steps words = {tot} (budget 115)")

print("method_card content words =", words(re.sub('<[^>]+>',' ', pd['method_card']['content'])))

if errs:
    print("ERRORS:")
    for e in errs: print("  -", e)
else:
    print("ALL MATHS CHECKS PASS")
