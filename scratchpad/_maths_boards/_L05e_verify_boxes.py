# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_maths-eduqas_algebra-L05.json", encoding="utf-8"))

def arith(s):
    # evaluate trailing "<expr> = " arithmetic using unicode ops
    m = re.search(r'([0-9\.\-\(\)\s×÷\+−]+?)\s*=\s*$', s)
    if not m: return None
    e = m.group(1).replace("×","*").replace("÷","/").replace("−","-")
    e = e.strip()
    if not re.search(r'\d', e): return None
    # must contain an operator to be an arithmetic check
    if not re.search(r'[\*/\+\-]', e[1:]): return None
    try:
        v = eval(e, {"__builtins__":{}}, {})
        return v
    except Exception:
        return None

bad = []
checked = 0
skipped = []

def check_walk(steps, path):
    global checked
    for i, st in enumerate(steps):
        if st.get("answer") is None: continue
        pre = st.get("pre","")
        v = arith(pre)
        if v is None:
            skipped.append(path+"[%d] pre=%r ans=%s"%(i,pre,st["answer"]))
            continue
        checked += 1
        if abs(v - st["answer"]) > 1e-9:
            bad.append("%s[%d]: pre computes %s but answer=%s | %r"%(path,i,v,st["answer"],pre))

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for j,p in enumerate(pb[tier]):
        check_walk(p["guided_steps"], "%s[%d].gs"%(tier,j))
for tier in ("bronze","silver","gold"):
    check_walk(pd["guided"]["teach"][tier]["steps"], "teach.%s"%tier)
check_walk(pd["guided"]["opener"]["steps"], "opener")

print("=== ARITHMETIC BOXES ===")
print("checked:", checked, "bad:", len(bad))
for b in bad: print("  XX", b)
print("--- skipped (non-arith, manual):", len(skipped))
for s in skipped: print("   ~", s)
