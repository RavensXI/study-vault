# -*- coding: utf-8 -*-
import json, re
live = json.load(open("_chk_L04_live.json", encoding="utf-8"))
pb = live["problem_bank"]
errors=[]; notes=[]

# Evaluate any "a op b op c = " arithmetic in pre/say and compare to answer
def eval_expr(e):
    e=e.replace("×","*").replace("÷","/").replace("−","-")
    e=e.replace("Σfx","").replace("Σf","")
    # keep only trailing arithmetic before '='
    m=re.findall(r'([0-9][0-9\.\s\+\-\*/\(\)]*[0-90-9\)])\s*=\s*$', e)
    if not m: return None
    expr=m[-1]
    if not re.fullmatch(r'[0-9\.\s\+\-\*/\(\)]+',expr): return None
    try: return eval(expr)
    except: return None

def check_walk(steps,path):
    for j,st in enumerate(steps):
        if "answer" not in st: continue
        for fld in ("pre","say"):
            v=st.get(fld,"")
            r=eval_expr(v)
            if r is not None:
                if abs(r-st["answer"])>1e-6:
                    errors.append(f"{path}[{j}] {fld} expr={r} but answer={st['answer']}: {v.strip()[-40:]!r}")

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if not gs: continue
        check_walk(gs,f"{tier}[{i}].guided_steps")
        # final box lands on solution
        finals=[s for s in gs if "answer" in s]
        # find the box that states the answer (done note or last non-check)
        sol=p["solutions"][0]
        vals=[s["answer"] for s in finals]
        if sol not in vals:
            errors.append(f"{tier}[{i}] solution {sol} not among guided box answers {vals}")
        # completion boundary
        phase_idx=[k for k,s in enumerate(gs) if s.get("phase")=="substitute"]
        if phase_idx:
            first=phase_idx[0]
            before=first
            after=len(gs)-first
            if before<1: errors.append(f"{tier}[{i}] <1 box before boundary")
            if after<2: errors.append(f"{tier}[{i}] <2 boxes at/after boundary")
        else:
            notes.append(f"{tier}[{i}] no phase:substitute boundary")

for tier in ("bronze","silver","gold"):
    check_walk(live["guided"]["teach"][tier]["steps"],f"teach.{tier}")
check_walk(live["guided"]["opener"]["steps"],"opener")

print("=== ARITH ERRORS ===")
for e in errors: print(" ",e)
print("=== NOTES ===")
for n in notes: print(" ",n)
print("TOTAL",len(errors))
