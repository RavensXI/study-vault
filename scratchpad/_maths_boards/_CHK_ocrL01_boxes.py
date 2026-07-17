import json, re
pd = json.load(open("_CHK_ocrL01_live.json", encoding="utf-8"))
issues = []

def normalize(expr):
    e = expr
    e = e.replace("×","*").replace("÷","/").replace("−","-").replace("£","").replace(",","")
    return e

# find arithmetic like "3 + 5 =" or "£40 ÷ 4 =" or "10 × £10 ="; capture RHS-before-'='
# We take the substring up to the LAST '=' and evaluate the trailing arithmetic expr.
arith_re = re.compile(r'([0-9.]+(?:\s*[+\-*/]\s*[0-9.]+)+)\s*=\s*$')

def check_box(path, pre, answer):
    if pre is None: return
    e = normalize(pre)
    e = e.strip()
    if not e.endswith("="):
        # maybe ends with "= " already stripped; try to find last '='
        pass
    # take part after last known operation phrase: use regex on the normalized string
    m = arith_re.search(e)
    if not m:
        # try: expression right before '='
        # split on '=' and take second-to-last chunk
        parts = e.split("=")
        cand = parts[-2] if len(parts)>=2 else None
        if cand:
            cand = cand.strip()
            mm = re.search(r'([0-9.]+(?:\s*[*/+\-]\s*[0-9.]+)+)$', cand)
            if mm:
                m = mm
    if not m:
        return  # no evaluable arithmetic (e.g. "the first number is")
    exprstr = m.group(1)
    try:
        val = eval(exprstr)
    except Exception as ex:
        issues.append(f"{path}: cannot eval '{exprstr}' ({ex})")
        return
    if abs(val - answer) > 1e-9:
        issues.append(f"{path}: '{exprstr}' = {val} but answer={answer}  (pre={pre!r})")

def walk_steps(steps, base):
    for i,s in enumerate(steps):
        if "answer" in s and "pre" in s:
            check_box(f"{base}[{i}]", s.get("pre",""), s["answer"])

g = pd["guided"]
walk_steps(g["opener"]["steps"], "opener")
for t in ["bronze","silver","gold"]:
    walk_steps(g["teach"][t]["steps"], f"teach.{t}")
pb = pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    for pi,prob in enumerate(pb[t]):
        walk_steps(prob.get("guided_steps",[]), f"{t}[{pi}].guided_steps")

print("=== BOX ISSUES ===")
for x in issues: print(x)
if not issues: print("none")
