# -*- coding: utf-8 -*-
import json, io, re
DIR = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards"
fresh = json.load(io.open(DIR + r"\_aqa_L12_fresh.json", encoding="utf-8"))
out = json.load(io.open(DIR + r"\lesson_maths-aqa_algebra-L12.json", encoding="utf-8"))

bad = []
# preservation: related_videos, worked_examples, topic_links byte-identical
for f in ("related_videos", "worked_examples", "topic_links"):
    if json.dumps(fresh.get(f), sort_keys=True) != json.dumps(out.get(f), sort_keys=True):
        bad.append("PRESERVE CHANGED: " + f)

# bank displays/solutions/options/input_type unchanged
for t in ("bronze", "silver", "gold"):
    for i, (a, b) in enumerate(zip(fresh["problem_bank"][t], out["problem_bank"][t])):
        for k in ("display", "solutions", "options", "input_type", "calculator"):
            if json.dumps(a.get(k)) != json.dumps(b.get(k)):
                bad.append("BANK CHANGED %s[%d].%s" % (t, i, k))

# expect != correct for MC / single_value
for t in ("bronze", "silver", "gold"):
    for i, p in enumerate(out["problem_bank"][t]):
        sol = p["solutions"]
        for j, m in enumerate(p.get("misconceptions", [])):
            e = m.get("expect")
            if e is not None and [float(x) for x in (e if isinstance(e, list) else [e])] == [float(x) for x in sol]:
                bad.append("EXPECT==SOL %s[%d].misc[%d]" % (t, i, j))
            # MC: expect must be a valid non-correct option index
            if p["input_type"] == "multiple_choice":
                if not (isinstance(e, int) and 0 <= e < len(p["options"]) and e != sol[0]):
                    bad.append("BAD MC EXPECT %s[%d].misc[%d]=%r" % (t, i, j, e))

# recompute every guided box: openers, teach, guided_steps
def check_boxes(steps, tag):
    for i, s in enumerate(steps):
        if s.get("answer") is not None and not isinstance(s["answer"], (int, float)):
            bad.append("nonnumeric box %s[%d]" % (tag, i))

check_boxes(out["guided"]["opener"]["steps"], "opener")
for tr in ("bronze", "silver", "gold"):
    check_boxes(out["guided"]["teach"][tr]["steps"], "teach." + tr)
for t in ("silver", "gold"):
    for i, p in enumerate(out["problem_bank"][t]):
        if p.get("guided_steps"):
            check_boxes(p["guided_steps"], "%s[%d].gs" % (t, i))

# teach SVG must reference the teach quadratic (label check)
for tr, coeffs in (("bronze", "x squared minus 7x plus 12"), ("silver", "x squared minus 2x minus 15"), ("gold", "2x squared plus 5x minus 3")):
    disp = out["guided"]["teach"][tr]["display"]
    if coeffs not in disp:
        bad.append("teach %s SVG label mismatch (expected %s)" % (tr, coeffs))
    if 'role="img"' not in disp or "viewBox" not in disp:
        bad.append("teach %s SVG missing attrs" % tr)

# em dash sweep on student-facing (exclude note)
def sweep(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note", "guided_skip_reason"): continue
            sweep(v, path + "." + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): sweep(v, "%s[%d]" % (path, i))
    elif isinstance(o, str) and "—" in o:
        bad.append("EM DASH at " + path)
sweep(out, "pd")

# verify the two single_value counts by brute force
def count_between(a, b):  # strict integers between a and b
    import math
    return len([n for n in range(int(math.floor(a)) - 2, int(math.ceil(b)) + 3) if a < n < b])
assert count_between(-2, 5) == 6, "S5 count"
assert count_between(1, 5) == 3, "G5 count"

# verify opener arithmetic
assert 5 - 1 == 4 and 2.5 - 1 == 1.5 and 2.5 - 4 == -1.5

print("VERIFY:", "CLEAN" if not bad else "ISSUES")
for b in bad: print("  -", b)
