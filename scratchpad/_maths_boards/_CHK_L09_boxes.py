import json, re
live = json.load(open("_CHK_L09eduqas_live.json", encoding="utf-8"))
issues=[]

def eval_arith(expr):
    # expr like "72 − 44", "2 × 3 + 3 × 2", "6y × 2"(skip), "5x × 3"(skip letters)
    e=expr.replace("−","-").replace("×","*").replace("÷","/")
    e=e.strip()
    # strip trailing artefacts
    if not e: return None
    # if it contains letters (x,y) it's a coefficient box; handle "Nx * M" -> coeff N*M
    if re.search(r'[a-wz]', e):  # words
        return None
    if re.fullmatch(r'[-+*/(). 0-9]+', e):
        try: return eval(e)
        except: return None
    return None

def check_box(path, b):
    if "answer" not in b: return
    pre=b.get("pre","") or ""
    post=b.get("post","") or ""
    ans=b["answer"]
    # pull the arithmetic just before the '=' at end, or full pre if it has '='
    # Cases: "72 − 44 = " ; "2x × 3 = " (coeff -> letter) ; "3 + y = 5  →  y = " ; "-2y = 11 − 15 = "
    p=pre
    # coefficient boxes: "<coeff><letter> × <n> =" with post letter -> N*n
    m=re.match(r'^\s*(-?\d*)\s*([xy])\s*×\s*(\d+)\s*=\s*$', pre.replace("−","-"))
    if m and post in("x","y"):
        c=m.group(1); c=1 if c in("","+") else(-1 if c=="-" else int(c))
        exp=c*int(m.group(3))
        if exp!=ans: issues.append((path,"coeffbox",pre,exp,ans))
        return
    # "<letter> × <n> =" e.g. "y × 2 ="
    m=re.match(r'^\s*([xy])\s*×\s*(\d+)\s*=\s*$', pre)
    if m and post in("x","y"):
        exp=int(m.group(2))
        if exp!=ans: issues.append((path,"coeffbox2",pre,exp,ans))
        return
    # general: take substring after last relevant '=' sign chain; use the arithmetic segment
    # find all "= <arith> =" or trailing "... = "
    # Simplest: split on '=' and '→', take the segment immediately preceding final '='
    seg=pre
    # remove arrow parts, keep last arithmetic expr before final '='
    # e.g "3 + y = 5  →  y ="  -> not pure arithmetic (has y). skip
    # e.g "-2y = 11 − 15 ="  -> segment "11 - 15" = -4
    parts=re.split(r'[=→]', pre)
    parts=[pp.strip() for pp in parts if pp.strip()]
    got=None
    for seg in reversed(parts):
        v=eval_arith(seg)
        if v is not None:
            got=v; break
    if got is None: return  # non-arithmetic box (e.g. plain "x =", "y =")
    if abs(got-ans)>1e-9:
        issues.append((path,"arith",pre,got,ans))

# opener
for i,b in enumerate(live["guided"]["opener"]["steps"]):
    check_box(f"opener.steps[{i}]", b)
# teach
for tier,walk in live["guided"]["teach"].items():
    for i,b in enumerate(walk["steps"]):
        check_box(f"teach.{tier}.steps[{i}]", b)
# bank
pb=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for pi,p in enumerate(pb[tier]):
        for i,b in enumerate(p.get("guided_steps",[])):
            check_box(f"{tier}[{pi}].guided_steps[{i}]", b)

print("=== BOX ARITHMETIC ISSUES ===")
for x in issues: print(x)
print("total:",len(issues))
