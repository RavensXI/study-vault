# -*- coding: utf-8 -*-
import json, io, re
import sympy as sp

x = sp.symbols('x')
pd = json.load(io.open("lesson_maths-aqa_algebra-L06.json", encoding="utf-8"))
fails = []

def latex_to_expr(s):
    # strip \( \), replace unicode minus, ^ handled by sympy via ** ; convert x^2 -> x**2
    s = s.replace("\\(", "").replace("\\)", "").replace("−", "-")
    s = s.replace("^2", "**2").replace("^", "**")
    # insert * between number and x, and between ) (
    s = re.sub(r'(\d)\s*x', r'\1*x', s)
    s = s.replace(")(", ")*(")
    s = re.sub(r'(\d)\s*\(', r'\1*(', s)   # 2(x**2...) and 5*(...)
    return sp.expand(sp.sympify(s))

def disp_quadratic(display):
    m = re.search(r'\\\((.*?)\\\)', display)
    return latex_to_expr("\\(" + m.group(1) + "\\)")

pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        path = f"{tier}[{i}]"
        target = disp_quadratic(p["display"])
        exps = []
        for k,o in enumerate(p["options"]):
            e = latex_to_expr(o)
            exps.append(e)
        # duplicate expansion check
        for a in range(len(exps)):
            for b in range(a+1,len(exps)):
                if sp.simplify(exps[a]-exps[b])==0:
                    fails.append(f"{path} options {a} and {b} are identical expansions: {exps[a]}")
        ci = p["solutions"][0]
        if sp.simplify(exps[ci]-target)!=0:
            fails.append(f"{path} solution index {ci} expands to {exps[ci]} != {target}")
        # misconception expect points to a distractor (not correct), and equals a wrong option
        for m in p.get("misconceptions",[]):
            ex = m["expect"]
            if ex==ci:
                fails.append(f"{path} misconception '{m['pattern']}' expect==correct index")
            if not (0<=ex<len(p["options"])):
                fails.append(f"{path} misconception expect out of range: {ex}")
        # every option distinct visually
        if len(set(p["options"]))!=len(p["options"]):
            fails.append(f"{path} duplicate option strings")

# check teach + opener boxes numerically (arithmetic in pre text)
def check_box_pre(pre, ans, path):
    # extract the arithmetic expression before '='
    if "=" in pre:
        expr = pre.split("=")[-2] if pre.count("=")>=1 else ""
        # take substring after last ':' or start
    # simpler: find all 'A op B =' patterns; just trust manual, but attempt eval
    return

# Opener: verify sides multiply to 15 and add to 8
op = pd["guided"]["opener"]["steps"]
boxes=[s["answer"] for s in op if s.get("answer") is not None]
if boxes!=[3,5] or 3*5!=15 or 3+5!=8:
    fails.append(f"opener boxes wrong: {boxes}")

# Teach walks: recompute the arithmetic each box claims
def evalexpr(t):
    t=t.replace("×","*").replace("−","-").replace("(-","(-").replace(" ","")
    t=t.replace("+(","+(").replace("×","*")
    return eval(t)
for tier,tw in pd["guided"]["teach"].items():
    for j,st in enumerate(tw["steps"]):
        if st.get("answer") is None: continue
        pre=st["pre"]
        # 'a × c = 3 × 4 = ' -> take the arithmetic between the last two '=' signs
        parts=[s for s in pre.split("=")]
        seg=parts[-2] if len(parts)>=2 else parts[0]
        mm=re.search(r'([0-9()+\-*×−.\s]+)$', seg)
        got=None
        if mm:
            try: got=evalexpr(mm.group(1))
            except Exception as e: got=("ERR",str(e))
        if got!=st["answer"]:
            fails.append(f"teach.{tier}.steps[{j}] pre '{pre}' computes {got} != stored {st['answer']}")

# tier_guides examples: expand answer == question
for tier,g in pd["tier_guides"].items():
    ex=g["example"]
    q=disp_quadratic(ex["question"])
    ans=None
    for s in ex["steps"]:
        if s.get("isAnswer"):
            mm=re.search(r'\\\((.*?)\\\)', s["content"])
            ans=latex_to_expr("\\("+mm.group(1)+"\\)")
    if ans is None or sp.simplify(ans-q)!=0:
        fails.append(f"tier_guides.{tier} example answer {ans} != question {q}")

if fails:
    print("VERIFY FAIL:")
    for f in fails: print("  -",f)
else:
    print("VERIFY PASS: all option expansions, solutions, distinct distractors, opener/teach boxes, tier examples correct.")
