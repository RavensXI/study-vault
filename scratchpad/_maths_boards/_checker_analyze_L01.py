# -*- coding: utf-8 -*-
import json, re

base = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards"
live = json.load(open(base + r"\_LIVE_number-L01.json", encoding="utf-8"))

# 1. em-dash sweep on student-facing strings (exclude internal 'note')
emdash = []
def walk(obj, path):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "note":
                continue
            walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if "—" in obj:
            emdash.append(path + " :: " + obj)
walk(live, "")
print("EM DASHES:", len(emdash))
for e in emdash: print("  ", e)

# 2. non-numeric answer boxes
badbox = []
def check_boxes(steps, path):
    for i, s in enumerate(steps):
        if isinstance(s, dict) and "answer" in s:
            if not isinstance(s["answer"], (int, float)):
                badbox.append(f"{path}[{i}] answer={s['answer']!r}")
for tier in ["bronze","silver","gold"]:
    for i, p in enumerate(live["problem_bank"][tier]):
        if "guided_steps" in p:
            check_boxes(p["guided_steps"], f"{tier}[{i}].guided_steps")
    check_boxes(live["guided"]["teach"][tier]["steps"], f"teach.{tier}")
check_boxes(live["guided"]["opener"]["steps"], "opener")
print("NON-NUMERIC BOXES:", badbox)

# 3. HTML entities in plain text pre/post/hint
ent = []
entpat = re.compile(r"&(?:[a-zA-Z]+|#\d+);")
def check_plain(steps, path):
    for i, s in enumerate(steps):
        if isinstance(s, dict):
            for f in ["pre","post","hint"]:
                if f in s and isinstance(s[f], str):
                    if entpat.search(s[f]): ent.append(f"{path}[{i}].{f}")
                    if "\\(" in s[f] or "\\dfrac" in s[f]: ent.append(f"{path}[{i}].{f} LATEX-in-plain")
for tier in ["bronze","silver","gold"]:
    for i, p in enumerate(live["problem_bank"][tier]):
        if "guided_steps" in p:
            check_plain(p["guided_steps"], f"{tier}[{i}].guided_steps")
print("ENTITY/LATEX-IN-PLAIN:", ent)

# 4. tier guide word budgets (<=115 words steps)
for tier in ["bronze","silver","gold"]:
    tg = live["tier_guides"][tier]
    wc = sum(len(re.sub(r"<[^>]+>","",s).split()) for s in tg["steps"])
    print(f"tier_guide {tier} steps words: {wc}  title: {tg['title']!r}")

# 5. dash in titles
for tier in ["bronze","silver","gold"]:
    t = live["tier_guides"][tier]["title"]
    if " - " in t or "–" in t: print("DASH IN TITLE", tier, t)

# 6. duplicate answers within a tier
for tier in ["bronze","silver","gold"]:
    sols = [tuple(p["solutions"]) for p in live["problem_bank"][tier]]
    dupes = [s for s in set(sols) if sols.count(s) > 1]
    print(f"{tier} solutions: {sols}  DUPES: {dupes}")
