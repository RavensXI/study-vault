import json, re
import sympy as sp

x, y = sp.symbols('x y')
live = json.load(open("_CHK_algL03_live.json", encoding="utf-8"))
pb = live["problem_bank"]

def latex_to_expr(s):
    # strip \( \)
    s = s.replace("\\(","").replace("\\)","")
    # ^ powers
    s = s.replace("^{2}","**2").replace("^2","**2").replace("^{3}","**3").replace("^3","**3")
    s = s.replace("−","-").replace("×","*")
    # insert * for implicit multiplication: )( , digit-letter, letter-(
    s = re.sub(r"\)\(", ")*(", s)
    s = re.sub(r"(\d)([a-zA-Z(])", r"\1*\2", s)
    s = re.sub(r"([a-zA-Z)])\(", r"\1*(", s)
    return sp.sympify(s)

for tier in ["bronze","silver","gold"]:
    for idx,p in enumerate(pb[tier]):
        disp = p["display"]
        m = re.search(r"\\\((.*)\\\)", disp)
        expr = latex_to_expr("\\("+m.group(1)+"\\)")
        opts = p["options"]
        exps = []
        for o in opts:
            try:
                exps.append(sp.expand(latex_to_expr(o)))
            except Exception as e:
                exps.append(("ERR",str(e),o))
        # correct = option index in solutions
        sol = p["solutions"][0]
        # verify correct option expands to the target expression
        tgt = sp.expand(expr)
        okcorrect = (exps[sol]==tgt)
        # detect equivalent option pairs
        dups=[]
        for i in range(len(exps)):
            for j in range(i+1,len(exps)):
                if isinstance(exps[i],sp.Expr) and isinstance(exps[j],sp.Expr) and sp.simplify(exps[i]-exps[j])==0:
                    dups.append((i,j))
        flag = "" if okcorrect else "  <<< CORRECT OPTION MISMATCH"
        print(f"{tier}[{idx}] {disp[:40]:42} correct=opt{sol} match={okcorrect}{flag}")
        if dups:
            print("      EQUIV OPTION PAIRS:", dups, "->", [opts[i] for i,j in dups]+[opts[j] for i,j in dups])
