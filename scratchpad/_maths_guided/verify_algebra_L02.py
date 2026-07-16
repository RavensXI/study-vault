# -*- coding: utf-8 -*-
"""Independent checker for algebra-L02: fresh-solve options, verify correct
index, and confirm every misconception expect points to a real distractor."""
import json, io, re
from sympy import symbols, sympify, expand, Eq
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

x = symbols('x')
T = standard_transformations + (implicit_multiplication_application,)

def latex_to_expr(s):
    s = s.replace("\\(", "").replace("\\)", "").strip()
    s = s.replace("^", "**").replace("−", "-").replace("\\times", "*").replace("\\cdot", "*")
    return parse_expr(s, transformations=T, evaluate=True)

def display_to_expr(disp):
    # extract the LaTeX inside \(...\) of the display and expand it
    m = re.search(r"\\\((.*)\\\)", disp)
    inner = m.group(1)
    inner = inner.replace("^", "**").replace("−", "-")
    return expand(parse_expr(inner, transformations=T))

pd = json.load(io.open("lesson_algebra-L02.json", encoding="utf-8"))
pb = pd["problem_bank"]
errors = []

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        tag = f"{tier}[{i}]"
        true = display_to_expr(p["display"])
        opts = [expand(latex_to_expr(o)) for o in p["options"]]
        sol = p["solutions"][0]
        # correct option must equal true expansion
        if opts[sol] != true:
            errors.append(f"{tag} WRONG correct option: opt{sol}={opts[sol]} but true={true}")
        # each other option must NOT equal true (so it is a genuine distractor)
        for j, o in enumerate(opts):
            if j != sol and o == true:
                errors.append(f"{tag} distractor opt{j} equals correct answer {true}")
        # misconception expects
        for m in p.get("misconceptions", []):
            e = m["expect"]
            if e is None:
                continue
            if e == sol:
                errors.append(f"{tag} misconception '{m['pattern']}' expect==correct index {e}")
            if not (0 <= e < len(opts)):
                errors.append(f"{tag} misconception '{m['pattern']}' expect {e} out of range")

# report the true expansions + correct option for eyeballing
print("=== fresh-solve table ===")
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        true = display_to_expr(p["display"])
        sol = p["solutions"][0]
        print(f"{tier}[{i}] {p['display'][:45]:45} -> {true}   [opt{sol}]")

print()
if errors:
    print("ERRORS:")
    for e in errors:
        print("  -", e)
else:
    print("ALL BANK OPTIONS + EXPECTS VERIFIED CLEAN")
