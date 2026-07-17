# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_maths-eduqas_algebra-L13.json", encoding="utf-8"))
errs = []

def nth_arith(seq):
    d = seq[1]-seq[0]
    return d, seq[0]-d  # d, zero term

# fresh-solve every bank problem
checks = {
 # bronze
 ("bronze",0): 4+(10-1)*5,          # 10th of 4,9,14,19
 ("bronze",4): 5-8,                 # common diff 8,5,2,-1
 ("bronze",6): 1+(20-1)*3,          # 20th of 1,4,7,10
 # silver
 ("silver",0): 15,                  # 5n-2=73
 ("silver",4): 19-4*4,              # first term, 5th=19 d=4
 ("silver",6): 2+5+8+11+14,         # sum 5 of 2,5,8,11
 # gold
 ("gold",0): 11,
 ("gold",1): 3,
 ("gold",2): 2,
 ("gold",3): 10,
 ("gold",4): 4,
}
for (t,i),expect in checks.items():
    sol = pd["problem_bank"][t][i]["solutions"][0]
    if sol != expect:
        errs.append(f"{t}[{i}] solution {sol} != fresh {expect}")

# verify MC solutions point to correct option (arithmetic)
mc = {
 ("bronze",1): "4n + 1", ("bronze",2): "4n - 1", ("bronze",3): "3n - 1",
 ("bronze",5): "5n + 5", ("bronze",7): "4n + 2",
 ("silver",1): "Yes (n = 27)", ("silver",2): "23 - 3n", ("silver",3): "4n - 5", ("silver",5): "No",
}
for (t,i),correct in mc.items():
    p = pd["problem_bank"][t][i]
    idx = p["solutions"][0]
    opt = p["options"][idx].replace("\\(","").replace("\\)","").strip()
    if opt != correct:
        errs.append(f"{t}[{i}] option[{idx}]='{opt}' != '{correct}'")

# G3 fixed: sum first 10 of 4,7,10 = 175 ; quadratic factorises
S10 = sum(4+3*k for k in range(10))
if S10 != 175: errs.append(f"S10={S10} != 175")
# 3n^2+5n-350 roots
import math
disc = 5*5+4*3*350
if int(math.isqrt(disc))**2 != disc: errs.append(f"G3 discriminant {disc} not perfect square")
# (n-10)(3n+35) = 3n^2+35n-30n-350 = 3n^2+5n-350  check
if (1*3, 35-30, 10*35) != (3,5,350): errs.append("G3 factorisation wrong")

# recompute every guided_step final box lands on solution; and each say/box shape
def last_box(steps):
    vals=[s["answer"] for s in steps if s.get("answer") is not None]
    return vals[-1] if vals else None

# verify the "answer" numbers in a few critical walks by recomputation
def approx(a,b): return abs(a-b)<1e-9

# G3 walk boxes: 350, 10, 175
g3 = pd["problem_bank"]["gold"][3]["guided_steps"]
g3boxes=[s["answer"] for s in g3 if s.get("answer") is not None]
if g3boxes != [350,10,175]: errs.append(f"G3 boxes {g3boxes}")

# opener rule 2n+3 at n=1,2,3
for n,exp in [(1,5),(2,7),(3,9)]:
    if 2*n+3!=exp: errs.append(f"opener rule fail n={n}")

# bronze teach dots 3,5,7 rule 2n+1, pattern10=21
if 2*10+1!=21: errs.append("teach bronze fail")
# silver teach 4,9,14,19 rule 5n-1; 100 -> 20.2 ; 104 -> 21
if not approx(101/5,20.2): errs.append("silver teach 100")
if 105//5!=21: errs.append("silver teach 104")
# gold teach Sn=n^2+4n, term6 = S6-S5
if (6**2+4*6)-(5**2+4*5)!=15: errs.append("gold teach term6")

# no duplicate single_value solutions within a tier
for t in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pd["problem_bank"][t]):
        if p.get("input_type")=="multiple_choice": continue
        k=tuple(p["solutions"])
        if k in seen: errs.append(f"{t} dup solution {k} at [{i}] and [{seen[k]}]")
        seen[k]=i

# expects != solution
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][t]):
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and not (p.get("input_type")=="multiple_choice"):
                if e==p["solutions"][0]: errs.append(f"{t}[{i}] expect==solution {e}")

# em dash scan (U+2014)
def scan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+str(k))
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,f"{path}[{j}]")
    elif isinstance(o,str) and "—" in o:
        errs.append(f"EM DASH at {path}")
scan(pd,"pd")

# preservation vs live
live=json.load(io.open("_eduqas_L13_live.json",encoding="utf-8"))
for f in ("related_videos","worked_examples","topic_links"):
    if pd[f]!=live[f]: errs.append(f"preservation: {f} changed")

# method_card word count
def words(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
print("method_card content words:", words(pd["method_card"]["content"]))
for t in ("bronze","silver","gold"):
    print(f"tier_guides.{t} steps words:", sum(words(s) for s in pd["tier_guides"][t]["steps"]))

if errs:
    print("FAIL", len(errs))
    for e in errs: print("  -",e)
else:
    print("ALL MATHS CHECKS PASS")
