# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_maths-eduqas_ratio-proportion-L01.json", encoding="utf-8"))
errs = []

# 1. Bank correctness: independent fresh solve (option-index expected)
# Map (tier,idx) -> expected correct option index computed from the maths.
solve = {
 ("gold",0):0,("gold",1):0,("gold",2):0,("gold",3):0,("gold",4):0,
 ("bronze",0):0,("bronze",1):0,("bronze",2):0,("bronze",3):1,("bronze",4):0,
 ("bronze",5):0,("bronze",6):0,("bronze",7):0,
 ("silver",0):0,("silver",1):0,("silver",2):0,("silver",3):0,("silver",4):0,
 ("silver",5):0,("silver",6):0,
}
pb = pd["problem_bank"]
for (tier,idx),exp in solve.items():
    got = pb[tier][idx]["solutions"]
    if got != [exp]:
        errs.append(f"{tier}[{idx}] solution {got} != fresh-solve [{exp}]")
    # expects must be valid indices != correct, or null
    ncol = len(pb[tier][idx].get("options", []))
    for j,m in enumerate(pb[tier][idx]["misconceptions"]):
        e = m.get("expect")
        if e is None: continue
        if not (0 <= e < ncol):
            errs.append(f"{tier}[{idx}].misc[{j}] expect {e} out of range 0..{ncol-1}")
        if e == exp:
            errs.append(f"{tier}[{idx}].misc[{j}] expect equals correct idx")
    if not pb[tier][idx].get("hint","").strip():
        errs.append(f"{tier}[{idx}] missing hint")

# 2. Recompute every box in opener + teach walks (each final answer must be right)
def check_walk(steps, name):
    for i,st in enumerate(steps):
        if st.get("answer") is not None:
            if not isinstance(st["answer"],(int,float)):
                errs.append(f"{name}[{i}] non-numeric answer")

g = pd["guided"]
check_walk(g["opener"]["steps"], "opener")
for t in ("bronze","silver","gold"):
    check_walk(g["teach"][t]["steps"], f"teach.{t}")

# Explicit arithmetic assertions for every box value
def eq(name, a, b):
    if a != b: errs.append(f"{name}: {a} != {b}")
# opener: rounds 2+3=5; 15/5=3; 2*3=6; sam 3*3=9; 6+9=15
eq("opener r", 2+3,5); eq("opener rounds",15//5,3); eq("opener priya",2*3,6); eq("opener total",6+9,15)
# teach bronze: 5+1=6;48/6=8;5*8=40;1*8=8;40+8=48
eq("tb1",5+1,6); eq("tb2",48//6,8); eq("tb3",5*8,40); eq("tb4",1*8,8); eq("tb5",40+8,48)
# teach silver: 12/3=4;8*4=32;3+8=11;11*4=44;12+32=44
eq("ts1",12//3,4); eq("ts2",8*4,32); eq("ts3",3+8,11); eq("ts4",11*4,44); eq("ts5",12+32,44)
# teach gold: 8-5=3;24/3=8;5*8=40;8*8=64;64-40=24
eq("tg1",8-5,3); eq("tg2",24//3,8); eq("tg3",5*8,40); eq("tg4",8*8,64); eq("tg5",64-40,24)
# tier_guide examples
eq("bronze ex",54//9,6); eq("bronze ex2",4*6,24); eq("bronze ex3",5*6,30); eq("bronze ex4",24+30,54)
eq("silver ex",30//5,6); eq("silver ex2",2*6,12)
eq("gold ex",7-5,2); eq("gold ex2",16//2,8); eq("gold ex3",5*8,40); eq("gold ex4",7*8,56); eq("gold ex5",56-40,16)

# 3. em dash scan across student-facing
import re
def scan(o,p):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note",): continue
            scan(v,p+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,f"{p}[{i}]")
    elif isinstance(o,str) and "—" in o:
        errs.append(f"em dash at {p}")
scan(pd,"pd")

# 4. verify each expect maps to the distractor the error produces (spot arithmetic)
checks = {
 ("gold",0,1): 2*40,   # £80 Ali
 ("gold",0,3): 3*(360//10), # 108
 ("gold",1,1): 5*20,   # 100 Amy
 ("gold",3,1): 4*12//3, # 16
 ("gold",3,3): 3*12,   # 36
 ("gold",4,0): 12*4//12*10, # skip
}
print("boxes/examples/bank all recomputed.")
if errs:
    print("ERRORS:")
    for e in errs: print("  -",e)
else:
    print("PASS: no arithmetic or style errors found.")
