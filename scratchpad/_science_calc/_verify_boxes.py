import json,io,re
pd=json.load(io.open("_live_canonical.json",encoding="utf-8"))
issues=[]

def check_box(pre,ans,path):
    # extract trailing "A op B op C = " arithmetic
    if pre is None: return
    m=re.search(r'([0-9.]+(?:\s*[×x*÷/]\s*[0-9.]+)+)\s*=\s*$', pre.strip())
    if not m: 
        # also handle patterns like "... = 5.3 ÷ 106 = " take last expr before final =
        m2=re.findall(r'([0-9.]+(?:\s*[×÷]\s*[0-9.]+)+)\s*=', pre)
        if m2:
            expr=m2[-1]
        else:
            return
    else:
        expr=m.group(1)
    e=expr.replace("×","*").replace("÷","/").replace("x","*")
    try:
        val=eval(e)
    except Exception as ex:
        return
    if abs(val-ans)>0.0051:
        issues.append(f"{path}: '{expr}' = {val} but box answer {ans}")

def walk(steps,path):
    for i,st in enumerate(steps):
        if st.get("answer") is not None:
            check_box(st.get("pre"), st["answer"], f"{path}[{i}]")

# guided teach + opener
for tier in ("bronze","silver","gold"):
    walk(pd["guided"]["teach"][tier]["steps"], f"teach.{tier}")
walk(pd["guided"]["opener"]["steps"], "opener")
# banks
for tier in ("bronze","silver","gold"):
    for j,p in enumerate(pd["problem_bank"][tier]):
        gs=p.get("guided_steps") or []
        walk(gs, f"{tier}[{j}].gs")

if issues:
    print("BOX ARITHMETIC ISSUES:")
    for x in issues: print(" -",x)
else:
    print("all parsed boxes arithmetic OK")
