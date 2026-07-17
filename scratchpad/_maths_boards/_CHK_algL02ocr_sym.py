import json, re, io
from sympy import symbols, expand, sympify, Eq
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

x, y, a, b = symbols('x y a b')
T = standard_transformations + (implicit_multiplication_application, convert_xor)
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
live = json.load(open(base+"_CHK_algL02ocr_live.json", encoding="utf-8"))
out = io.open(base+"_CHK_sym_out.txt","w",encoding="utf-8")

def clean(s):
    s = s.replace("\\(","").replace("\\)","")
    s = s.replace("−","-").replace("×","*").replace("·","*")
    s = s.replace("^","**")
    return s.strip()

def P(s):
    return parse_expr(clean(s), transformations=T)

def latex_to_expr(disp):
    # extract the \(...\) math after 'Expand' / 'Expand and simplify'
    m = re.findall(r"\\\((.*?)\\\)", disp)
    return m

fails = []
pb = live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i, prob in enumerate(pb[tier]):
        disp = prob["display"]
        opts = prob.get("options")
        sols = prob.get("solutions")
        maths = latex_to_expr(disp)
        if not maths:
            out.write(f"{tier}[{i}] NO MATH in display: {disp}\n"); continue
        expr_str = maths[0]  # the expression to expand
        try:
            correct = expand(P(expr_str))
        except Exception as e:
            out.write(f"{tier}[{i}] PARSE-FAIL '{expr_str}': {e}\n"); continue
        if opts and sols is not None:
            idx = sols[0]
            opt_expr = expand(P(latex_to_expr(opts[idx])[0]))
            match = (opt_expr - correct == 0)
            out.write(f"{tier}[{i}] {expr_str} -> {correct} | sol_opt[{idx}]={opt_expr} {'OK' if match else 'MISMATCH'}\n")
            if not match: fails.append(f"{tier}[{i}] solution mismatch")
            # check other options are genuinely different from correct
            for j,o in enumerate(opts):
                oe = expand(P(latex_to_expr(o)[0]))
                if j!=idx and oe-correct==0:
                    out.write(f"   !! distractor[{j}] equals correct answer\n")
                    fails.append(f"{tier}[{i}] distractor {j} == correct")

# Teach walk expansions
teach = live["guided"]["teach"]
teach_expected = {"bronze":"5*(x+4)","silver":"(x+2)*(x+6)","gold":"(x+5)**2"}
for tier,exprs in teach_expected.items():
    out.write(f"TEACH {tier} display: {teach[tier]['display']} -> expand={expand(P(exprs))}\n")

out.write("\nFAILS: "+("NONE" if not fails else "; ".join(fails))+"\n")
out.close()
print("done; fails:", fails)
