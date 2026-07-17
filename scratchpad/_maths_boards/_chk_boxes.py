import json, io, re
pd=json.load(io.open("_CHK_L09_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
guided=pd["guided"]

def norm(s):
    return s.replace('−','-').replace('×','*').replace('(-','( -')

def check_arith(expr, ans, where):
    # take substring after last '=' if present else whole
    e=norm(expr)
    # extract arithmetic: find pattern like "NUM op NUM" possibly with = at end
    # strip trailing '=' and spaces
    core=e
    if '=' in core:
        # could be like "3 + y = 5  ->  y ="  ; take the leftmost pure-arith before first '='
        parts=[p for p in core.split('=')]
        # try each part for pure arithmetic
        for part in parts:
            part=part.strip().rstrip('->').strip()
            # remove variable-containing
            if re.search(r'[a-zA-Z]', part): 
                continue
            part=part.replace('->','').strip()
            if part and re.fullmatch(r'[-+*/(). 0-9]+', part):
                try:
                    val=eval(part)
                    if abs(val-ans)<1e-9:
                        return None
                    else:
                        return f"{where}: '{part}' = {val} but answer={ans}"
                except: pass
        return None  # no pure arithmetic to check
    return None

issues=[]
# bank guided_steps
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        for j,st in enumerate(p.get("guided_steps",[])):
            if "answer" in st:
                pre=st.get("pre","")
                r=check_arith(pre, st["answer"], f"{tier}[{i}].guided_steps[{j}]")
                if r: issues.append(r)
# teach walks
for tier in ("bronze","silver","gold"):
    for j,st in enumerate(guided["teach"][tier]["steps"]):
        if "answer" in st:
            r=check_arith(st.get("pre",""), st["answer"], f"teach.{tier}[{j}]")
            if r: issues.append(r)
# opener
for j,st in enumerate(guided["opener"]["steps"]):
    if "answer" in st:
        r=check_arith(st.get("pre",""), st["answer"], f"opener[{j}]")
        if r: issues.append(r)

print("ARITH ISSUES:", len(issues))
for x in issues: print("  ", x)
