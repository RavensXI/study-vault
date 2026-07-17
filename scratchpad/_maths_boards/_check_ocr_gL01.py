# -*- coding: utf-8 -*-
"""Adversarial box-arithmetic check: parse the trailing 'expr =' in every pre and
confirm it evaluates to the stated answer. Also confirm expects != solution."""
import json, re, io

MINUS = "−"; DIV = "÷"; TIMES = "×"
pd = json.load(io.open("lesson_maths-ocr_graphs-L01.json", encoding="utf-8"))

def normalize(s):
    s = s.replace(MINUS, "-").replace(DIV, "/").replace(TIMES, "*")
    return s

def trailing_expr(pre):
    """Return the arithmetic expression just before the final '='."""
    t = normalize(pre).strip()
    if not t.endswith("="):
        return None
    t = t[:-1].strip()
    # take the part after the last ':' or the last '=' inside (chained)
    # split on '=' -> take last non-empty chunk
    chunks = [c.strip() for c in t.split("=") if c.strip()]
    if not chunks:
        return None
    expr = chunks[-1]
    # strip a leading label: keep only from the first numeric token, including a
    # leading '(' or '(-' bracket wrapper on a negative literal.
    m = re.search(r"\(?-?\d", expr)
    if not m:
        return None
    start = m.start()
    # if the matched digit sits inside a bracket like '(-2', back up to the '('
    if start > 0 and expr[start-1] == "(" and expr[m.start()] == "-":
        start -= 1
    elif expr[start] == "(":
        pass
    expr = expr[start:]
    # only allow arithmetic chars
    if re.fullmatch(r"[-0-9()+*/. ]+", expr):
        return expr
    return None

problems = 0; boxes = 0; mismatches = []
def check_steps(steps, path):
    global boxes
    for i, st in enumerate(steps):
        if st.get("answer") is None:
            continue
        boxes += 1
        expr = trailing_expr(st.get("pre", ""))
        if expr is None:
            continue
        try:
            val = eval(expr)
        except Exception as e:
            mismatches.append((path + "[%d]" % i, "EVAL_ERR", expr, str(e)))
            continue
        if abs(val - st["answer"]) > 1e-9:
            mismatches.append((path + "[%d]" % i, expr, "=%s" % val, "answer=%s" % st["answer"]))

pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        problems += 1
        if p.get("guided_steps"):
            check_steps(p["guided_steps"], "%s[%d].guided_steps" % (tier, i))
        # misconception expect != solution
        for j, m in enumerate(p.get("misconceptions", [])):
            e = m.get("expect")
            if e is not None and e == p["solutions"][0]:
                mismatches.append(("%s[%d].misc[%d]" % (tier, i, j), "EXPECT==SOL", e, ""))

check_steps(pd["guided"]["opener"]["steps"], "opener")
for t in ("bronze","silver","gold"):
    check_steps(pd["guided"]["teach"][t]["steps"], "teach."+t)

print("problems", problems, "boxes", boxes, "arith-mismatches", len(mismatches))
for mm in mismatches:
    print("  ", mm)
