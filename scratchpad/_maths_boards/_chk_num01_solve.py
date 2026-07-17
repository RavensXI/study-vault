import json
live = json.load(open("_CHK_num01_live.json", encoding="utf-8"))
pb = live["problem_bank"]

# Fresh-solve each display via a safe eval after translating LaTeX to python
import re
def to_expr(disp):
    s=disp
    s=s.replace("\\dfrac","\\frac")
    # fractions \frac{A}{B}
    def frac(m):
        return f"(({m.group(1)})/({m.group(2)}))"
    while "\\frac" in s:
        s=re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", frac, s, count=1)
    s=s.replace("\\times","*").replace("\\div","/")
    s=s.replace("\\(","").replace("\\)","")
    s=s.replace("×","*").replace("÷","/")
    # powers a^b or a^{b}
    s=re.sub(r"\^\{([^{}]*)\}", r"**(\1)", s)
    s=re.sub(r"\^(\w)", r"**\1", s)
    return s

# integer floor division? No: use true division then compare. BIDMAS: python respects * / + - and ** precedence.
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        expr=to_expr(p["display"])
        try:
            val=eval(expr)
        except Exception as e:
            print(f"{t}[{i}] EVAL ERROR expr={expr!r}: {e}"); continue
        sol=p["solutions"][0]
        ok = abs(val-sol)<1e-9
        print(f"{t}[{i}] {p['display']!r} -> eval {val} stored {sol} {'OK' if ok else 'MISMATCH ***'}")
