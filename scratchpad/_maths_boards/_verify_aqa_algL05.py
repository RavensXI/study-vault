# -*- coding: utf-8 -*-
import json, io
from sympy import symbols, Eq, solve, Rational, sympify
x = symbols('x')

# (display-equation as sympy string lhs, rhs, expected solution)
BANK = {
 "bronze": [
   ("3*x", "18", 6),
   ("x + 7", "15", 8),
   ("2*x - 5", "13", 9),
   ("4*x + 3", "19", 4),
   ("x/3", "7", 21),
   ("20 - 3*x", "5", 5),
   ("5*x + 2", "3*x + 16", 7),
   ("7*x - 1", "4*x + 8", 3),
 ],
 "silver": [
   ("3*(x + 4)", "27", 5),
   ("2*(3*x - 1)", "5*x + 7", 9),
   ("4*(x + 2)", "3*(x + 5)", 7),
   ("(x + 5)/2", "8", 11),
   ("(2*x - 3)/5", "5", 14),
   ("5*(2*x + 1) - 3*(x - 2)", "25", 2),
   ("3*x/4", "9", 12),
 ],
 "gold": [
   ("(x+1)/3 + (x-1)/4", "3", 5),
   ("(5*x + 2)/3", "(3*x + 8)/2", 20),
   ("2*(x-1)/5", "(x+3)/2", -19),
   ("3*(2*x + 1)", "2*(4*x - 3) + 3", 3),
   ("(7-x)/3", "(x+1)/5", 4),
 ],
}

pd = json.load(io.open("lesson_maths-aqa_algebra-L05.json", encoding="utf-8"))
ok = True
for tier, items in BANK.items():
    stored = pd["problem_bank"][tier]
    seen = set()
    for i, (lhs, rhs, exp) in enumerate(items):
        sol = solve(Eq(sympify(lhs), sympify(rhs)), x)
        s = sol[0]
        storedsol = stored[i]["solutions"][0]
        status = "OK" if (s == exp and exp == storedsol) else "*** MISMATCH ***"
        if status != "OK": ok = False
        if storedsol in seen:
            status += " DUP!"; ok = False
        seen.add(storedsol)
        print(f"{tier}[{i}] solve={s} exp={exp} stored={storedsol} {status}")

# misconception expects: verify each expect != correct
print("\n--- misconception expects vs correct ---")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            correct=p["solutions"][0]
            flag = "  <-- EQUALS CORRECT!" if (e is not None and abs(e-correct)<1e-9) else ""
            if flag: ok=False
            print(f"{tier}[{i}].misc[{j}] pattern={m['pattern']} expect={e} correct={correct}{flag}")

# verify final answer box of each guided_steps lands on solution
print("\n--- final 'So x =' box lands on solution ---")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        gs=p["guided_steps"]
        # find the box whose pre starts with 'So x ='
        finals=[st for st in gs if st.get("answer") is not None and st.get("pre","").strip().startswith("So x")]
        if finals:
            v=finals[-1]["answer"]; correct=p["solutions"][0]
            st="OK" if v==correct else "*** MISMATCH ***"
            if st!="OK": ok=False
            print(f"{tier}[{i}] final box answer={v} solution={correct} {st}")
        else:
            print(f"{tier}[{i}] NO 'So x =' box")

print("\nALL OK" if ok else "\nPROBLEMS FOUND")
