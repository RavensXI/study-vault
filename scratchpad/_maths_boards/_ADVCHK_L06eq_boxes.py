# -*- coding: utf-8 -*-
import json, math
pd = json.load(open("_ADVCHK_L06eq_live.json", encoding="utf-8"))

# Dump every box (pre/post/answer) so I can eyeball each computation, plus flag
# any box whose 'answer' isn't a plain number, and count live boxes after phase.
def dump_walk(name, steps):
    print(f"\n### {name}")
    phase_idx = None
    box_indices = []
    for i,s in enumerate(steps):
        if "say" in s and "answer" not in s:
            print(f"  [{i}] SAY: {s['say'][:90]}")
        else:
            ans = s.get("answer")
            tag = " PHASE" if s.get("phase")=="substitute" else ""
            if s.get("phase")=="substitute": phase_idx=i
            box_indices.append(i)
            print(f"  [{i}] BOX{tag}: pre={s.get('pre','')[:70]!r} post={s.get('post','')!r} ans={ans}")
            if not isinstance(ans,(int,float)):
                print(f"      *** answer not numeric: {ans!r}")
    if phase_idx is not None:
        after = [i for i in box_indices if i>=phase_idx]
        before = [i for i in box_indices if i<phase_idx]
        print(f"  phase at {phase_idx}: boxes_before={len(before)} boxes_at/after={len(after)}")
        if len(after)<2: print("      *** fewer than 2 live boxes at/after phase")
        if len(before)<1: print("      *** no box before phase")

g = pd["guided"]
dump_walk("opener", g["opener"]["steps"])
for t in ["bronze","silver","gold"]:
    dump_walk(f"teach.{t}", g["teach"][t]["steps"])

pb = pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        gs = p.get("guided_steps")
        if gs: dump_walk(f"{t}[{i}] gs (sol={p['solutions']})", gs)
        else: print(f"\n### {t}[{i}] NO guided_steps input_type={p.get('input_type')}")
