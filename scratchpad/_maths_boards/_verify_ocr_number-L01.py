# -*- coding: utf-8 -*-
# Independent re-solve: parse each display's arithmetic and check stored solution,
# then walk guided_steps chain, then reproduce every misconception expect.
import json, io, re

pd = json.load(io.open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_number-L01.json", encoding="utf-8"))
fails = []

def latex_to_expr(s):
    # strip \( \)
    s = s.replace("\\(", "").replace("\\)", "")
    # \frac{a}{b} and \dfrac
    for tag in ("\\dfrac", "\\frac"):
        while tag in s:
            i = s.index(tag)
            j = i + len(tag)
            # parse {..}
            assert s[j] == "{"
            depth = 0; k = j
            for k in range(j, len(s)):
                if s[k] == "{": depth += 1
                elif s[k] == "}":
                    depth -= 1
                    if depth == 0: break
            num = s[j+1:k]
            m = k+1
            assert s[m] == "{"
            depth = 0
            for n in range(m, len(s)):
                if s[n] == "{": depth += 1
                elif s[n] == "}":
                    depth -= 1
                    if depth == 0: break
            den = s[m+1:n]
            s = s[:i] + "((" + num + ")/(" + den + "))" + s[n+1:]
    # sqrt{..}
    while "\\sqrt{" in s:
        i = s.index("\\sqrt{")
        j = i + 5
        depth = 0
        for k in range(j, len(s)):
            if s[k] == "{": depth += 1
            elif s[k] == "}":
                depth -= 1
                if depth == 0: break
        inner = s[j+1:k]
        s = s[:i] + "((" + inner + ")**0.5)" + s[k+1:]
    s = s.replace("\\times", "*").replace("\\div", "/")
    s = s.replace("\\left", "").replace("\\right", "")
    # powers a^b or a^{b}
    s = re.sub(r"\^\{(\d+)\}", r"**\1", s)
    s = re.sub(r"\^(\d+)", r"**\1", s)
    s = s.replace("−", "-")
    return s

def ev(s):
    return eval(latex_to_expr(s), {"__builtins__": {}}, {})

pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    seen = {}
    for i, p in enumerate(pb[tier]):
        disp = p["display"]
        try:
            got = ev(disp)
        except Exception as e:
            fails.append("%s[%d] cannot eval %r: %s" % (tier, i, disp, e)); continue
        sol = p["solutions"][0]
        if abs(got - sol) > 1e-9:
            fails.append("%s[%d] display evaluates to %s but solution says %s (%s)" % (tier, i, got, sol, disp))
        if sol in seen:
            fails.append("%s[%d] DUP solution %s (also %s[%d])" % (tier, i, sol, tier, seen[sol]))
        seen[sol] = i
        # walk guided_steps final box lands on solution
        boxes = [st for st in p["guided_steps"] if st.get("answer") is not None]
        if boxes and abs(boxes[-1]["answer"] - sol) > 1e-9:
            fails.append("%s[%d] last guided box %s != solution %s" % (tier, i, boxes[-1]["answer"], sol))
        # misconception expects must not equal solution
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            if e is not None and abs(float(e) - sol) < 1e-9:
                fails.append("%s[%d] expect equals solution" % (tier, i))

# verify explicit expect derivations
checks = {
 ("bronze",0): (3+5)*2, ("bronze",1): (20-4)*3, ("bronze",2): (6+12)/4,
 ("bronze",3): 10-24, ("bronze",4): ((15/3)+4)*3, ("bronze",5): ((2*7)+3)*4,
 ("bronze",6): ((30-5)*4)+1, ("bronze",7): 48/(6/2),
 ("silver",0): 3+5*4, ("silver",1): 5*12-4+6, ("silver",2): (2*3)+5*3,
 ("silver",3): 100/4+6*3, ("silver",4): (3*4)**2-20, ("silver",5): 7**2-3**2+8,
 ("silver",6): 60-2*((3*2)+1),
 ("gold",0): 36-12/2*3, ("gold",1): ((8-2)**2)/9,
 ("gold",2): 9+4*((2*3)-3), ("gold",3): (8**2)/4-(2*3),
 ("gold",4): (2*3)**2+40/2**3,
}
for (tier,i),val in checks.items():
    exp = pb[tier][i]["misconceptions"][0]["expect"]
    if abs(exp - val) > 1e-9:
        fails.append("EXPECT mismatch %s[%d]: derived %s but stored %s" % (tier,i,val,exp))

# teach + opener boxes: just recompute chain locally by trusting pre text arithmetic where simple; check opener
op = pd["guided"]["opener"]["steps"]
if not (op[0]["answer"]==8 and op[1]["answer"]==11): fails.append("opener boxes wrong")
# opener: 3 + 2*4 = 11 ; blind = (3+2)*4=20
assert 3+2*4==11 and (3+2)*4==20

if fails:
    print("VERIFY FAIL:")
    for f in fails: print("  -", f)
else:
    print("VERIFY PASS: all displays eval to solutions, no dup within tier, all expects reproduce, opener sound")
