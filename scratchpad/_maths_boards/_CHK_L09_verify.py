import json, re

live = json.load(open("_CHK_L09eduqas_live.json", encoding="utf-8"))
pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))

# pre-dump may be a dict keyed by id or list; find L09 entry
def find_pre(pre):
    ID="038c2343-8acf-41e4-b02a-914268bc6572"
    if isinstance(pre, dict):
        if ID in pre: return pre[ID]
        for k,v in pre.items():
            if isinstance(v,dict) and (v.get("id")==ID or v.get("slug")=="simultaneous-equations-linear"):
                return v.get("practice_data", v)
    if isinstance(pre, list):
        for v in pre:
            if v.get("id")==ID or v.get("slug")=="simultaneous-equations-linear":
                return v.get("practice_data", v)
    return None
pre_pd = find_pre(pre)
print("pre type:", type(pre).__name__, "| pre_pd found:", pre_pd is not None)
if isinstance(pre,dict): print("pre keys sample:", list(pre.keys())[:3])

errors=[]

# ---- em dash scan on all student-facing strings ----
EMDASH="—"
def scan(obj, path, skip_note=True):
    if isinstance(obj, str):
        if EMDASH in obj:
            errors.append(("EMDASH", path, obj[:60]))
    elif isinstance(obj, dict):
        for k,v in obj.items():
            if skip_note and k=="note": continue
            scan(v, path+"."+k, skip_note)
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            scan(v, f"{path}[{i}]", skip_note)
scan(live, "root")

# ---- solve every problem fresh from display ----
def parse_eq(s):
    # s like "2x + 5y = 24" -> (a,b,c)
    s=s.replace("−","-").replace(" ","")
    lhs,rhs=s.split("=")
    rhs=int(rhs)
    # coefficients
    import re
    a=b=0
    for m in re.finditer(r'([+-]?\d*)x', lhs):
        t=m.group(1)
        a+= 1 if t in("","+") else (-1 if t=="-" else int(t))
    for m in re.finditer(r'([+-]?\d*)y', lhs):
        t=m.group(1)
        b+= 1 if t in("","+") else (-1 if t=="-" else int(t))
    return a,b,rhs

def solve(disp):
    # display "Solve \(2x + 5y = 24\) and \(3x + 4y = 22\)"
    eqs=re.findall(r'\\((.*?)\\)', disp)
    a1,b1,c1=parse_eq(eqs[0]); a2,b2,c2=parse_eq(eqs[1])
    det=a1*b2-a2*b1
    x=(c1*b2-c2*b1)/det; y=(a1*c2-a2*c1)/det
    return x,y

pb=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        disp=p["display"]
        try:
            x,y=solve(disp)
        except Exception as e:
            errors.append(("SOLVEFAIL",f"{tier}[{i}]",disp+" "+str(e))); continue
        sol=p["solutions"]
        if abs(x-sol[0])>1e-9 or abs(y-sol[1])>1e-9:
            errors.append(("SOLUTION",f"{tier}[{i}]",f"disp={disp} stored={sol} fresh=({x},{y})"))
        if p.get("calculator")==False:
            if abs(x-round(x))>1e-9 or abs(y-round(y))>1e-9:
                errors.append(("NONCALC_MESSY",f"{tier}[{i}]",f"{disp} -> ({x},{y})"))
        # final guided boxes land on solutions: last two numeric answers with post x / y? just check the check step exists
        # verify all guided_steps: box answers must be numbers
        # duplicate detection handled later

# ---- duplicate solutions within tier ----
for tier in ["bronze","silver","gold"]:
    seen={}
    for i,p in enumerate(pb[tier]):
        key=tuple(p["solutions"])
        disp=p["display"]
        seen.setdefault(disp,[]).append(i)
    dups={d:ix for d,ix in seen.items() if len(ix)>1}
    if dups: errors.append(("DUP_DISPLAY",tier,str(dups)))

print("\n=== ERRORS ===")
for e in errors:
    print(e)
print("total:",len(errors))
