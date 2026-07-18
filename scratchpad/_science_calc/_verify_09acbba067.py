# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_higher-calculations-L05@09acbba067.json", encoding="utf-8"))
errs = []
MINUS = chr(0x2212); DIV = chr(0xF7); MUL = chr(0xD7)

def compute_pre(pre):
    # try to eval trailing "A op B op C ... = " arithmetic
    m = re.search(r"([-\d][\d\s%s%s%s+.()]*?)\s*=\s*$" % (re.escape(MINUS), re.escape(DIV), re.escape(MUL)), pre)
    if not m: return None
    expr = m.group(1)
    expr = expr.replace(MINUS, "-").replace(DIV, "/").replace(MUL, "*")
    expr = re.sub(r"[A-Za-z]", "", expr)  # strip stray letters
    if not re.fullmatch(r"[-\d\s/*+.()]+", expr): return None
    try:
        return eval(expr, {"__builtins__": {}})
    except Exception:
        return None

pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        tag = "%s[%d]" % (tier, i)
        sols = p["solutions"]
        gs = p.get("guided_steps") or []
        boxans = [st["answer"] for st in gs if st.get("answer") is not None]
        # arithmetic continuity on parseable pres
        for j, st in enumerate(gs):
            if st.get("answer") is None: continue
            r = compute_pre(st.get("pre", ""))
            if r is not None and abs(r - st["answer"]) > 0.005:
                errs.append("%s.gs[%d] pre '%s' computes %s not %s" % (tag, j, st["pre"].strip(), r, st["answer"]))
        # final numeric box should equal the solution (last non-check answer path);
        # check that the solution value appears among box answers
        if sols and not any(abs(a - sols[0]) < 0.005 for a in boxans):
            errs.append("%s solution %s not reached by any box %s" % (tag, sols, boxans))
        # expects differ from solution
        for m in p.get("misconceptions") or []:
            e = m.get("expect")
            if e is not None and abs(float(e) - float(sols[0])) < 0.011:
                errs.append("%s expect %s equals solution %s" % (tag, e, sols))
        # boundary
        sub = [k for k, st in enumerate(gs) if st.get("phase") == "substitute"]
        if gs:
            if not sub:
                errs.append("%s no substitute boundary" % tag)
            else:
                s0 = sub[0]
                live = sum(1 for st in gs[s0:] if st.get("answer") is not None)
                before = sum(1 for st in gs[:s0] if st.get("answer") is not None)
                if before < 1: errs.append("%s no pre-worked box before boundary" % tag)
                if live < 2: errs.append("%s only %d live boxes after boundary" % (tag, live))

# em dash sweep
def sweep(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note",): continue
            sweep(v, path + "." + k)
    elif isinstance(o, list):
        for k, v in enumerate(o): sweep(v, "%s[%d]" % (path, k))
    elif isinstance(o, str) and "—" in o:
        errs.append("EM DASH at " + path)
sweep(pd, "pd")

# print full solutions recap
print("SOLUTIONS:")
for tier in ("bronze","silver","gold"):
    print(" ", tier, [p["solutions"][0] for p in pb[tier]])
print("EXPECTS:")
for tier in ("bronze","silver","gold"):
    print(" ", tier, [ (p["misconceptions"][0]["expect"] if p.get("misconceptions") else None) for p in pb[tier]])
print()
print("ERRORS:" if errs else "ALL CHECKS PASS")
for e in errs: print("  -", e)
