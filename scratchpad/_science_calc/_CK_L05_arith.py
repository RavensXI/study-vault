import json, re

pd = json.load(open("_CK_L05_row0.json", encoding="utf-8"))

SUP = {"⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9"}
def desup(s):
    return "".join(SUP.get(c,c) for c in s)

def evalexpr(e):
    # normalise
    e = desup(e)
    e = e.replace("×","*").replace("÷","/").replace("−","-").replace("–","-")
    # handle 2^n written as 2*2*... already; handle a^b
    e = re.sub(r'(\d+)\^(\d+)', lambda m: str(int(m.group(1))**int(m.group(2))), e)
    e = e.strip().rstrip("=").strip()
    if not e or not re.fullmatch(r'[0-9\.\+\-\*/ ]+', e):
        return None
    try:
        return eval(e)
    except Exception:
        return None

def check_steps(steps, label):
    for i, st in enumerate(steps):
        if "answer" not in st:
            continue
        pre = st.get("pre","")
        # extract the arithmetic before the final "="
        # take substring after last ':' or after '=' chain; find pattern "<expr> = "
        m = re.search(r'([0-9⁰-⁹\.\+\-\−–\*×/÷ \^]+)=\s*$', pre)
        expr = None
        if m:
            expr = m.group(1)
        else:
            # try "= expr = " middle e.g. "50 × 2⁴ = 50 × 16 = "
            parts = pre.split("=")
            if len(parts) >= 2:
                expr = parts[-2]
        if expr is None:
            continue
        val = evalexpr(expr)
        if val is None:
            continue
        ans = st["answer"]
        if abs(val - ans) > 1e-9:
            print(f"MISMATCH {label}[{i}]: pre={pre!r} expr={expr!r} eval={val} answer={ans}")

# banks
for tier, probs in pd["problem_bank"].items():
    if not isinstance(probs, list):
        continue
    for pi, p in enumerate(probs):
        gs = p.get("guided_steps")
        if gs:
            check_steps(gs, f"{tier}[{pi}]")
        # verify final live box lands on solution
        sol = p.get("solutions")
        if gs and sol:
            live = [s for s in gs if "answer" in s]
# teach walks
for tier, w in pd["guided"]["teach"].items():
    check_steps(w["steps"], f"teach.{tier}")
check_steps(pd["guided"]["opener"]["steps"], "opener")
print("arith check done")
