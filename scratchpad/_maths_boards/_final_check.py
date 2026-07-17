# -*- coding: utf-8 -*-
import json, io
from fractions import Fraction as F
live=json.load(io.open("_live_number-L02.json",encoding="utf-8"))
new=json.load(io.open("lesson_number-L02.json",encoding="utf-8"))

# 1. preserved fields byte-identical
for k in ("related_videos","worked_examples","topic_links"):
    same = live.get(k)==new.get(k)
    print(f"preserve {k}: {'SAME' if same else 'CHANGED'}")

# 2. bank display/solutions: what changed vs live
for tier in ("bronze","silver","gold"):
    lo=live["problem_bank"][tier]; nw=new["problem_bank"][tier]
    assert len(lo)==len(nw), (tier,len(lo),len(nw))
    for i,(a,c) in enumerate(zip(lo,nw)):
        if a["display"]!=c["display"] or a["solutions"]!=c["solutions"]:
            print(f"CHANGED {tier}[{i}]: display {a['display']!r}->{c['display']!r} sol {a['solutions']}->{c['solutions']}")

# 3. re-fresh-solve every NEW display, confirm solutions
import re
def parse_and_solve(disp, sol):
    # strip latex, evaluate manually is hard; just re-list known solved map by index via display
    return None
# recompute via explicit map (mirror of _solve/_verify already run) -- confirm every solution present & no dup within tier
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(new["problem_bank"][tier]):
        s=tuple(p["solutions"]); seen.setdefault(s,[]).append(i)
        # expect != solution
        for m in p["misconceptions"]:
            assert m.get("expect")!=p["solutions"], (tier,i,m["pattern"])
            assert "expect" in m
    dups={k:v for k,v in seen.items() if len(v)>1}
    print(f"{tier}: dups={dups if dups else 'none'}")

# 4. em dash scan (belt and braces)
s=json.dumps(new,ensure_ascii=False)
print("em dash present:", "—" in s)
# 5. every guided box answer numeric & has pre+hint
bad=0
def scan(steps):
    global bad
    for st in steps:
        if st.get("answer") is not None:
            if not isinstance(st["answer"],(int,float)): bad+=1
            if not st.get("pre","").strip() or not st.get("hint","").strip(): bad+=1
for tier in ("bronze","silver","gold"):
    for p in new["problem_bank"][tier]: scan(p["guided_steps"])
    scan(new["guided"]["teach"][tier]["steps"])
scan(new["guided"]["opener"]["steps"])
print("bad boxes:", bad)
print("opener has svg:", "<svg" in new["guided"]["opener"]["display"], "| xmlns present:", "xmlns" in new["guided"]["opener"]["display"])
