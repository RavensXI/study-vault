# -*- coding: utf-8 -*-
"""Independent fresh-solve check of every bank answer, every guided box, every
opener/teach box, and every misconception expect for algebra-L04."""
import json, io, math

pd = json.load(io.open("lesson_algebra-L04.json", encoding="utf-8"))
errs = []

# --- Fresh-solve the bank answers from an independent evaluator ---
def bidmas_ok(desc, computed, stored):
    if abs(computed - stored[0]) > 1e-9:
        errs.append(f"ANSWER MISMATCH {desc}: computed {computed} vs stored {stored}")

B = pd["problem_bank"]["bronze"]; S = pd["problem_bank"]["silver"]; G = pd["problem_bank"]["gold"]

# Bronze fresh
bidmas_ok("B0 2x+5,x=3", 2*3+5, B[0]["solutions"])
bidmas_ok("B1 4x-1,x=6", 4*6-1, B[1]["solutions"])
bidmas_ok("B2 3a+2b,a4b5", 3*4+2*5, B[2]["solutions"])
bidmas_ok("B3 5x-3,x=-2", 5*(-2)-3, B[3]["solutions"])
bidmas_ok("B4 4a-b,a5b3", 4*5-3, B[4]["solutions"])
bidmas_ok("B5 x/2+3,x=10", 10/2+3, B[5]["solutions"])
bidmas_ok("B6 6x+y,x3y-4", 6*3+(-4), B[6]["solutions"])
bidmas_ok("B7 10-3x,x=5", 10-3*5, B[7]["solutions"])
# Silver fresh
bidmas_ok("S0 x^2+5,x=4", 4**2+5, S[0]["solutions"])
bidmas_ok("S1 x^2-5x,x=6", 6**2-5*6, S[1]["solutions"])
bidmas_ok("S2 2x^2+1,x=-3", 2*(-3)**2+1, S[2]["solutions"])
bidmas_ok("S3 v=u+at,u5a4t3", 5+4*3, S[3]["solutions"])
bidmas_ok("S4 3x^2-2x+4,x=2", 3*2**2-2*2+4, S[4]["solutions"])
bidmas_ok("S5 (x^2+1)/5,x=3", (3**2+1)/5, S[5]["solutions"])
bidmas_ok("S6 x^2+2x-8,x=-4", (-4)**2+2*(-4)-8, S[6]["solutions"])

# Gold: verify correct option algebraically by checking the option string index
# Correct rearrangements confirmed manually:
gold_correct = {0:0, 1:0, 2:0, 3:1, 4:0}
for i,g in enumerate(G):
    if g["solutions"][0] != gold_correct[i]:
        errs.append(f"GOLD G{i} correct option {g['solutions']} != expected {gold_correct[i]}")

# --- Duplicate solution check within non-MC tiers ---
for name, tier in (("bronze",B),("silver",S)):
    seen={}
    for i,p in enumerate(tier):
        k=tuple(p["solutions"])
        if k in seen:
            errs.append(f"DUP solution in {name}: idx {seen[k]} and {i} both {k}")
        seen[k]=i

# --- Verify guided_steps boxes: final live boxes land on solution; check continuity of stated arithmetic ---
def check_walk(prob, label):
    gs = prob.get("guided_steps")
    if not gs: return
    # collect box answers
    boxes=[st for st in gs if st.get("answer") is not None]
    # final box answer should equal the solution for these single_value substitution walks
    sol = prob["solutions"][0]
    if abs(boxes[-1]["answer"]-sol) > 1e-9:
        errs.append(f"{label}: final box {boxes[-1]['answer']} != solution {sol}")
    # boundary: >=1 box before phase substitute, >=2 live at/after
    sub_at=None
    for i,st in enumerate(gs):
        if st.get("phase")=="substitute" and sub_at is None: sub_at=i
    if sub_at is None:
        errs.append(f"{label}: no substitute boundary")
    else:
        before=sum(1 for st in gs[:sub_at] if st.get("answer") is not None)
        after=sum(1 for st in gs[sub_at:] if st.get("answer") is not None)
        if before<1: errs.append(f"{label}: {before} boxes before boundary")
        if after<2: errs.append(f"{label}: {after} live boxes after boundary")

for i,p in enumerate(B): check_walk(p, f"bronze[{i}]")
for i,p in enumerate(S): check_walk(p, f"silver[{i}]")

# --- Verify specific box arithmetic by re-deriving from the pre text semantics (manual mirror) ---
# Bronze boxes expected sequences
expected_boxes = {
 "bronze[0]":[6,11,11], "bronze[1]":[24,23,23], "bronze[2]":[12,10,22],
 "bronze[3]":[-10,-13,-13], "bronze[4]":[20,17,17], "bronze[5]":[5,8,8],
 "bronze[6]":[18,14,14], "bronze[7]":[15,-5,-5],
 "silver[0]":[16,21,21], "silver[1]":[36,30,6], "silver[2]":[9,18,19],
 "silver[3]":[12,17,17], "silver[4]":[4,12,4,12], "silver[5]":[9,10,2],
 "silver[6]":[16,-8,0],
}
for name,tier in (("bronze",B),("silver",S)):
    for i,p in enumerate(tier):
        key=f"{name}[{i}]"
        got=[st["answer"] for st in p["guided_steps"] if st.get("answer") is not None]
        if got != expected_boxes[key]:
            errs.append(f"{key} box sequence {got} != expected {expected_boxes[key]}")

# --- Misconception expects: recompute the committed error ---
def me(prob, idx, val, label):
    m=prob["misconceptions"][idx]
    if m["expect"]!=val:
        errs.append(f"{label} expect {m['expect']} != recomputed {val}")
    if val is not None and val==prob["solutions"][0] and prob.get("input_type")!="multiple_choice":
        errs.append(f"{label} expect equals correct answer")

me(B[0],0,2*(3+5),"B0.mis0")            # 16
me(B[1],0,4*(6-1),"B1.mis0")            # 20
me(B[2],0,(3+4)+(2+5),"B2.mis0")        # 14
me(B[3],0,5*(-2-3),"B3.mis0")           # -25
me(B[3],1,10-3,"B3.mis1")               # 7
me(B[4],0,4*(5-3),"B4.mis0")            # 8
me(B[5],0,(10+3)/2,"B5.mis0")           # 6.5
me(B[6],0,6*(3+(-4)),"B6.mis0")         # -6
me(B[6],1,18+4,"B6.mis1")               # 22
me(B[7],0,(10-3)*5,"B7.mis0")           # 35
me(S[0],0,(4+5)**2,"S0.mis0")           # 81
me(S[1],0,(36-5)*6,"S1.mis0")           # 186
me(S[2],0,2*(-9)+1,"S2.mis0")           # -17 (neg squared as -9)
me(S[2],1,(2*-3)**2+1,"S2.mis1")        # 37
me(S[3],0,(5+4)*3,"S3.mis0")            # 27
me(S[4],0,(3*2)**2-2*2+4,"S4.mis0")     # 36
me(S[5],0,9+1/5,"S5.mis0")              # 9.2
me(S[6],0,-16-8-8,"S6.mis0")            # -32 (neg squared as -16)

# Gold misconception expects are option indices; just ensure != correct
for i,g in enumerate(G):
    for j,m in enumerate(g["misconceptions"]):
        if m["expect"]==g["solutions"][0]:
            errs.append(f"gold[{i}].mis{j} expect equals correct option")

# --- Opener + teach boxes ---
op=[st["answer"] for st in pd["guided"]["opener"]["steps"] if st.get("answer") is not None]
if op!=[11,15]: errs.append(f"opener boxes {op} != [11,15]")
if 3+2*4!=11 or 3+2*6!=15: errs.append("opener maths wrong")
tb=[st["answer"] for st in pd["guided"]["teach"]["bronze"]["steps"] if st.get("answer") is not None]
if tb!=[15,8,23,23]: errs.append(f"teach bronze {tb}")
if 5*3!=15 or 2*4!=8 or 15+8!=23: errs.append("teach bronze maths")
ts=[st["answer"] for st in pd["guided"]["teach"]["silver"]["steps"] if st.get("answer") is not None]
if ts!=[25,50,47,47]: errs.append(f"teach silver {ts}")
if (-5)**2!=25 or 2*25!=50 or 50-3!=47: errs.append("teach silver maths")
tg=[st["answer"] for st in pd["guided"]["teach"]["gold"]["steps"] if st.get("answer") is not None]
if tg!=[12,4,2,20]: errs.append(f"teach gold {tg}")
if (20-12)//4!=2 or 4*2+12!=20: errs.append("teach gold maths")

# --- tier_guide examples land right ---
if 4*2+3!=11: errs.append("bronze tier example")
if (-3)**2-4!=5: errs.append("silver tier example")
if (4+6)//2!=5 or 2*5-6!=4: errs.append("gold tier example")

# --- method_card example ---
if 5+3*4!=17: errs.append("method_card example")

if errs:
    print("FAIL", len(errs))
    for e in errs: print("  -", e)
else:
    print("ALL MATHS VERIFIED CLEAN")
