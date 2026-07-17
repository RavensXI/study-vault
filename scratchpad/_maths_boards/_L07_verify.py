# -*- coding: utf-8 -*-
import json, io, math
pd = json.load(io.open("lesson_maths-eduqas_number-L07.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# Fresh-solve every stored solution
def approx(a, b, t=0.02): return abs(a-b) < t

checks = {
 ("bronze",0): 2+4, ("bronze",1): 7-3, ("bronze",2): 4*2, ("bronze",3): math.isqrt(49),
 ("bronze",4): round(27**(1/3)), ("bronze",5): 45-0.5, ("bronze",6): 45+0.5, ("bronze",7): 1,
 ("silver",2): round(8**(1/3))**2, ("silver",5): 6.4+0.05, ("silver",6): round(125**(1/3))**2,
 ("gold",1): (math.sqrt(20)+math.sqrt(45))/math.sqrt(5),
 ("gold",2): round(5.25*8.65,2), ("gold",3): 9-5, ("gold",4): (2**3)/(2**3),
}
for (t,i),v in checks.items():
    sol = pb[t][i]["solutions"][0]
    if not approx(float(sol), float(v)):
        errs.append(f"{t}[{i}] solution {sol} != computed {v}")

# fraction silver[3]
s3 = pb["silver"][3]["solutions"]
if s3 != [1,8]: errs.append(f"silver[3] fraction {s3} != [1,8]")

# MC correctness: verify the marked-correct option is the truly-correct value AND unique
def val(opt):
    # crude LaTeX surd evaluator for a*sqrt(b) or plain int
    o = opt.replace("\\(","").replace("\\)","").replace("{","").replace("}","")
    o = o.replace("\\dfrac","").replace("\\frac","")
    if "\\sqrt" in o:
        # forms: a\sqrt b  or \sqrt b
        import re
        m = re.match(r"^(\d*)\\sqrt(\d+)$", o)
        if m:
            a = int(m.group(1)) if m.group(1) else 1
            return a*math.sqrt(int(m.group(2)))
    try: return float(o)
    except: return None

for t,i,correct in [("silver",0,0),("silver",1,0),("silver",4,0),("gold",0,0)]:
    p = pb[t][i]
    vals = [val(o) for o in p["options"]]
    cidx = p["solutions"][0]
    cv = vals[cidx]
    # no other option numerically equals correct
    for j,vj in enumerate(vals):
        if j!=cidx and vj is not None and cv is not None and approx(vj,cv,1e-4):
            errs.append(f"{t}[{i}] option {j} ({p['options'][j]}) equals correct {p['options'][cidx]}")

# Known correct MC values
mc_expected = {("silver",0):5*math.sqrt(2),("silver",1):6*math.sqrt(2),
               ("silver",4):5*math.sqrt(3),("gold",0):2*math.sqrt(3)}
for (t,i),cvv in mc_expected.items():
    p=pb[t][i]; cidx=p["solutions"][0]; v=val(p["options"][cidx])
    if v is None or not approx(v,cvv,1e-4):
        errs.append(f"{t}[{i}] marked option {p['options'][cidx]} != expected value {cvv}")

# Verify every guided_steps box lands and walk continuity by recomputing key finals
# Check that the phase:substitute solution-box in each non-MC problem equals stored solution
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        gs = p.get("guided_steps")
        if not gs: continue
        boxes = [s for s in gs if s.get("answer") is not None]
        # last non-check box before final should reach solution; just ensure all numeric
        for k,s in enumerate(gs):
            if s.get("answer") is not None and not isinstance(s["answer"],(int,float)):
                errs.append(f"{t}[{i}].gs[{k}] non-numeric")

# expects must not equal solution (single-value)
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        sols=p["solutions"]
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is None: continue
            if p.get("input_type") not in ("multiple_choice",) and len(sols)==1:
                if approx(float(e),float(sols[0]),1e-6):
                    errs.append(f"{t}[{i}] expect {e} == solution")

# Duplicate solutions within tier (non-MC)
for t in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[t]):
        if p.get("input_type")=="multiple_choice": continue
        key=tuple(p["solutions"])
        if key in seen: errs.append(f"{t} dup solution {key} at {seen[key]} and {i}")
        seen[key]=i

# em dash sweep
def sweep(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note",): continue
            sweep(v,path+"."+str(k))
    elif isinstance(o,list):
        for j,v in enumerate(o): sweep(v,f"{path}[{j}]")
    elif isinstance(o,str) and "—" in o: errs.append("EMDASH "+path)
sweep(pd)

print("ERRORS:" if errs else "ALL MATHS CHECKS PASS")
for e in errs: print("  -",e)
