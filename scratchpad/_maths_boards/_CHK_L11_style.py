# -*- coding: utf-8 -*-
import json
live = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_L11_live.json", encoding="utf-8"))

def has_latex(s):
    return isinstance(s, str) and ("\\(" in s or "$$" in s or "\\[" in s)

# hints in bank must be plain text
print("== LaTeX in bank hints ==")
for t, probs in live["problem_bank"].items():
    if not isinstance(probs, list): continue
    for i, p in enumerate(probs):
        if has_latex(p.get("hint","")):
            print(f"  {t}[{i}].hint: {p['hint']}")

# pre/post in guided_steps (bank) must be plain text
print("== LaTeX in bank guided_steps pre/post ==")
for t, probs in live["problem_bank"].items():
    if not isinstance(probs, list): continue
    for i, p in enumerate(probs):
        for j, st in enumerate(p.get("guided_steps",[])):
            for f in ("pre","post"):
                if has_latex(st.get(f,"")):
                    print(f"  {t}[{i}].guided_steps[{j}].{f}: {st[f]}")

# teach pre/post
print("== LaTeX in teach pre/post (allowed in say) ==")
for tier, w in live["guided"]["teach"].items():
    for j, st in enumerate(w["steps"]):
        for f in ("pre","post"):
            if has_latex(st.get(f,"")):
                print(f"  teach.{tier}.steps[{j}].{f}: {st[f]}")

# opener pre/post
print("== LaTeX in opener pre/post ==")
for j, st in enumerate(live["guided"]["opener"]["steps"]):
    for f in ("pre","post"):
        if has_latex(st.get(f,"")):
            print(f"  opener.steps[{j}].{f}: {st[f]}")

# hint plain in guided_steps / teach
print("== LaTeX in any step hint ==")
def scan_hint(steps, base):
    for j, st in enumerate(steps):
        if has_latex(st.get("hint","")):
            print(f"  {base}[{j}].hint: {st['hint']}")
for t, probs in live["problem_bank"].items():
    if isinstance(probs,list):
        for i,p in enumerate(probs):
            scan_hint(p.get("guided_steps",[]), f"{t}[{i}].gs")
for tier,w in live["guided"]["teach"].items():
    scan_hint(w["steps"], f"teach.{tier}")
scan_hint(live["guided"]["opener"]["steps"], "opener")

# which tier first-bank problems have guided_steps (completion problem targets)
print("== first-bank-problem input types ==")
for t in ("bronze","silver","gold"):
    p0 = live["problem_bank"][t][0]
    print(f"  {t}[0]: input_type={p0['input_type']} has_guided_steps={'guided_steps' in p0}")
print("== single_value problems w/ guided_steps ==")
for t in ("bronze","silver","gold"):
    for i,p in enumerate(live["problem_bank"][t]):
        if p["input_type"]=="single_value":
            print(f"  {t}[{i}] guided_steps={len(p.get('guided_steps',[]))} phase_tags={[j for j,s in enumerate(p.get('guided_steps',[])) if s.get('phase')=='substitute']}")
