# -*- coding: utf-8 -*-
import json
pd = json.load(open("lesson_maths-aqa_probability-statistics-L03.json", encoding="utf-8"))
pb = pd["problem_bank"]

# 1. duplicate solutions within tier (non-MC)
for tier in ("bronze", "silver", "gold"):
    seen = {}
    for i, p in enumerate(pb[tier]):
        if p.get("input_type") == "multiple_choice": continue
        k = tuple(p["solutions"])
        if k in seen: print("DUP", tier, i, k, "vs", seen[k])
        seen[k] = i

# 2. last live box of each guided walk should relate to solution; print final answers + expects
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        sol = p["solutions"]
        boxes = [s["answer"] for s in gs if "answer" in s] if gs else []
        # expects sanity: none equal solution
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            if e is not None:
                ev = e if isinstance(e, list) else [e]
                if len(ev) == len(sol) and all(abs(float(a)-float(b))<0.01 for a,b in zip(ev,sol)):
                    print("EXPECT==SOL", tier, i, e)
        print(tier, i, "sol", sol, "boxes", boxes, "it", p.get("input_type"))

# 3. teach walks final boxes
for t in ("bronze","silver","gold"):
    tb = pd["guided"]["teach"][t]
    boxes=[s["answer"] for s in tb["steps"] if "answer" in s]
    print("teach", t, boxes)
op=[s.get("answer") for s in pd["guided"]["opener"]["steps"] if "answer" in s]
print("opener", op)

# 4. tier guide step word counts
def words(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
for t in ("bronze","silver","gold"):
    print("tg", t, "words", sum(words(s) for s in pd["tier_guides"][t]["steps"]))
print("mc content words", words(pd["method_card"]["content"]))

# 5. SVG char sizes
import re
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if "<svg" in (p.get("display") or ""):
            print("svg", tier, i, "len", len(p["display"]))
