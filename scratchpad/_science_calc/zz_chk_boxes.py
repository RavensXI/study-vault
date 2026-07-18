import json, re

pd = json.load(open("zz_chk_canonical.json", encoding="utf-8"))

# Extract the final "a op b op c ... = " arithmetic before the box, evaluate, compare to answer
op = {"×": "*", "÷": "/", "−": "-", "+": "+", "*": "*"}
num = r"[-+]?\d+(?:\.\d+)?"
# match a chain like  A op B op C =   at end of pre string
chain_re = re.compile(rf"({num}(?:\s*[×÷−+]\s*{num})+)\s*=\s*$")

def evalchain(expr):
    # left to right with correct precedence: convert to python; here we respect *,/ before +,- via python eval
    e = expr
    for k, v in op.items():
        e = e.replace(k, v)
    return eval(e)

checked = 0
mismatch = 0

def check_steps(steps, label):
    global checked, mismatch
    for i, st in enumerate(steps):
        if "answer" not in st:
            continue
        pre = st.get("pre", "")
        m = chain_re.search(pre)
        if not m:
            continue
        expr = m.group(1)
        try:
            val = evalchain(expr)
        except Exception as ex:
            print(f"  PARSEFAIL {label}[{i}]: {expr!r} ({ex})")
            continue
        ans = st["answer"]
        checked += 1
        if abs(val - ans) > 1e-6:
            mismatch += 1
            print(f"  MISMATCH {label}[{i}]: '{expr}' = {val} but answer={ans}")

# opener
check_steps(pd["guided"]["opener"]["steps"], "opener")
# teach
for t in ["bronze", "silver", "gold"]:
    check_steps(pd["guided"]["teach"][t]["steps"], f"teach.{t}")
# bank
for tier in ["bronze", "silver", "gold"]:
    for pi, prob in enumerate(pd["problem_bank"][tier]):
        check_steps(prob.get("guided_steps", []), f"{tier}[{pi}]")

print(f"\nChecked {checked} arithmetic boxes, {mismatch} mismatches")
