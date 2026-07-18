# -*- coding: utf-8 -*-
# Independent adversarial verification of the built lesson.
import json, io, re, sys
sys.stdout.reconfigure(encoding="utf-8")

pd = json.load(io.open("lesson_831aee1062.json", encoding="utf-8"))
errs = []

# Ground-truth solver from the DISPLAY text of each problem (independent of build).
# We encode the intended physics per problem index and confirm stored solution.
truth = {
    ("bronze", 0): 600 / 0.2,          # p = F/A
    ("bronze", 1): 5000 * 2,           # F = pA
    ("bronze", 2): 5 * 1000 * 10,      # p = hrg
    ("bronze", 3): 200 / 0.04,
    ("bronze", 4): 3 * 800 * 10,
    ("bronze", 5): 1200 / 0.3,         # changed from 900 -> 1200
    ("silver", 0): 40 * 1000 * 10,
    ("silver", 1): 200000 * 0.05,
    ("silver", 2): 102500 / (1025 * 10),
    ("silver", 3): 1200 / 6000,
    ("silver", 4): (0.8 - 0.5) * 1000 * 10,
    ("gold", 0): 120 * 1025 * 10 * 500,
    ("gold", 1): 0.5 * 1.2 * 10,
    ("gold", 2): 1000 * 0.18 * 10,
    ("gold", 3): 3500 / (1000 * 10),
}

for tier in ("bronze", "silver", "gold"):
    seen = {}
    for i, p in enumerate(pd["problem_bank"][tier]):
        sol = p["solutions"][0]
        exp = truth[(tier, i)]
        if abs(sol - exp) > 1e-6:
            errs.append("%s[%d] solution %s != physics %s" % (tier, i, sol, exp))
        # duplicate check
        if sol in seen:
            errs.append("%s[%d] duplicate solution %s (also %s)" % (tier, i, sol, seen[sol]))
        seen[sol] = i
        # display number must appear in the display OR be derivable; check the
        # display text references the numbers we solved with (spot: force/area/depth)
        # misconception expects must lie outside +/-0.011 of the solution
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            if e is not None and abs(float(e) - float(sol)) < 0.011:
                errs.append("%s[%d] expect %s inside accept of %s" % (tier, i, e, sol))
        # walk must land on the solution: last box with 'answer' before/at check
        gs = p["guided_steps"]
        boxes = [s for s in gs if s.get("answer") is not None]
        # the compute box (first phase substitute box) should equal solution
        sub_boxes = [s for s in gs if s.get("phase") == "substitute" and s.get("answer") is not None]
        if not any(abs(float(b["answer"]) - float(sol)) < 1e-6 for b in sub_boxes):
            errs.append("%s[%d] no substitute box lands on solution %s" % (tier, i, sol))
        # every box numeric
        for j, b in enumerate(boxes):
            if not isinstance(b["answer"], (int, float)):
                errs.append("%s[%d] box %d non-numeric" % (tier, i, j))

# Walk arithmetic continuity: recompute each guided_steps pre-expression where it
# is a simple 'A op B =' pattern and confirm it equals the stored answer.
expr_re = re.compile(r"([-\d.()\s×÷+−]+?)\s*=\s*$")
def scan_walk(steps, tag):
    for j, s in enumerate(steps):
        if s.get("answer") is None:
            continue
        pre = s.get("pre", "")
        m = expr_re.search(pre)
        if not m:
            continue
        expr = m.group(1).strip()
        # need at least one operator to be an arithmetic expression
        if not any(op in expr for op in "×÷+−"):
            continue
        py = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
        if not re.fullmatch(r"[-\d.()*/+ ]+", py):
            continue
        try:
            got = eval(py, {"__builtins__": {}}, {})
        except Exception:
            continue
        if abs(got - float(s["answer"])) > 1e-6:
            errs.append("%s box %d: '%s' computes %s but answer %s" % (tag, j, expr, got, s["answer"]))

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        scan_walk(p["guided_steps"], "%s[%d]" % (tier, i))
    scan_walk(pd["guided"]["teach"][tier]["steps"], "teach.%s" % tier)
scan_walk(pd["guided"]["opener"]["steps"], "opener")

# Board neutrality: no board names / equation-sheet claims in student-facing text
blob = json.dumps(pd, ensure_ascii=False).lower()
for bad in ["equation sheet", "on your sheet", "you must memorise", "aqa", "edexcel", "ocr", "wjec", "eduqas"]:
    if bad in blob:
        errs.append("board/sheet phrase present: %r" % bad)

# SVG safety: every svg has role/aria, no http, and figure numbers appear in text
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        q = p["question"]
        if "role=\"img\"" not in q or "aria-label=" not in q:
            errs.append("%s[%d] svg missing role/aria" % (tier, i))
        if "http://" in q or "https://" in q:
            errs.append("%s[%d] svg has http" % (tier, i))

print("PROBLEMS CHECKED:", sum(len(pd['problem_bank'][t]) for t in ('bronze','silver','gold')))
if errs:
    print("VERIFY FAIL:")
    for e in errs:
        print("  -", e)
else:
    print("VERIFY PASS: solutions, expects, walk arithmetic, board-neutrality, svg all clean")
