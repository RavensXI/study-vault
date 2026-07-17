# -*- coding: utf-8 -*-
import json, io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(io.open("lesson_maths-eduqas_algebra-L05.json", encoding="utf-8"))

def arith(s):
    m = re.search(r'([0-9\.\-\(\)\s×÷\+−]+?)\s*=\s*$', s)
    if not m: return None
    e = m.group(1).replace("×","*").replace("÷","/").replace("−","-").strip()
    if not re.search(r'\d', e): return None
    if not re.search(r'[\*/\+\-]', e[1:]): return None
    try: return eval(e, {"__builtins__":{}}, {})
    except Exception: return None

skipped=[]
def walk(steps,path):
    for i,st in enumerate(steps):
        if st.get("answer") is None: continue
        if arith(st.get("pre","")) is None:
            skipped.append("%s[%d] ans=%s pre=%r"%(path,i,st["answer"],st.get("pre","")))
pb=pd["problem_bank"]
for t in ("bronze","silver","gold"):
    for j,p in enumerate(pb[t]): walk(p["guided_steps"],"%s[%d].gs"%(t,j))
for t in ("bronze","silver","gold"): walk(pd["guided"]["teach"][t]["steps"],"teach.%s"%t)
walk(pd["guided"]["opener"]["steps"],"opener")
print("CONCEPTUAL BOXES (manual confirm):")
for s in skipped: print("  ~",s)

# --- final answer lands on solution: each walk contains solution as a box answer
print("\nWALK LANDS ON SOLUTION:")
for t in ("bronze","silver","gold"):
    for j,p in enumerate(pb[t]):
        sol=p["solutions"][0]
        ans=[st["answer"] for st in p["guided_steps"] if st.get("answer") is not None]
        print(("OK " if sol in ans else "XX ")+"%s[%d] sol=%s answers=%s"%(t,j,sol,ans))

# --- expects: commit each described error
print("\nEXPECTS (committed error == expect):")
def show(name, computed, expect):
    print(("OK " if abs(computed-expect)<1e-9 else "XX ")+"%s committed=%s expect=%s"%(name,computed,expect))
# bronze
show("b0 forgot_divide", 8, 8)            # 2x=8 -> reports 8
show("b0 wrong_inverse", (13+5)/2, 9)     # add 5: 18/2=9
show("b1 forgot_divide", 15, 15)
show("b2 forgot_divide", 24, 24)
show("b3 adds_instead", 7+3, 10)
show("b4 subtracts_instead", 35-5, 30)
show("b5 sign_flip", 9-4, 5)
show("b6 forgot_divide", 21, 21)
show("b7 forgot_divide", 48, 48)
# silver
show("s0 dropped_constant", 12/3, 4)      # 3x=12 -> 4
show("s1 partial_expand", (20-2)/4, 4.5)  # 4x+2=20 -> 4x=18 -> 4.5
show("s2 dropped_constant", 21/6, 3.5)    # 6x=21 -> 3.5
show("s3 dropped_constant", 28/4, 7)      # 4x=28 -> 7
show("s4 partial_expand", (9-2)/1, 7);    # 6x+1=5x+9 -> x=8 : recompute
# s4: 6x+1=5x+9 -> x=8
show("s4 partial_expand(real)", (9-1)/1, 8)
show("s5 bad_collect", 10, 10)            # 8+2=10 = x (thinks coeff 1)
show("s6 no_expand", (1+4)/1, 5)          # x-4=x+1?? actual: 3x-4=2x+1 -> x=5
show("s6 no_expand(real)", (1+4), 5)
# gold
show("g0 no_clear", (5-1)/2, 2)           # 2x+1=5 -> 2x=4 -> 2
show("g1 partial_expand", (3+1)/1, 4)     # x+3=2x-1 -> x=4
show("g2 no_scale_constants", (4-2)/1, 2) # 6x+2=5x+4 -> x=2
show("g3 dropped_plus_one", 13/2, 6.5)    # 5(x-2)/3=x+1 -> 5x-10=3x+3 -> 2x=13 -> 6.5
show("g4 partial_cross", (2+3)/1, 5)      # 16x-3=15x+2 -> x=5
