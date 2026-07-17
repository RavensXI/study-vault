# -*- coding: utf-8 -*-
import json
ID="ca643606-adf3-40c8-a4dd-8dfb8c25a21f"
live=json.load(open("_MYCHK_live.json",encoding="utf-8"))
dump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))

# find entry
entry=None
if isinstance(dump,list):
    for e in dump:
        if e.get("id")==ID or e.get("lesson_id")==ID:
            entry=e; break
elif isinstance(dump,dict):
    entry=dump.get(ID)
print("dump type:", type(dump).__name__, "keys sample:", (list(dump.keys())[:3] if isinstance(dump,dict) else "list"))
if entry is None and isinstance(dump,list):
    print("first elem keys:", list(dump[0].keys()))
print("entry found:", entry is not None)
if entry:
    pre=entry.get("practice_data") or entry.get("pd") or entry
    for fld in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(pre.get(fld),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(fld),sort_keys=True,ensure_ascii=False)
        print(f"{fld}: {'SAME' if a==b else 'DIFF'}")
        if a!=b:
            print("  PRE:",a[:300])
            print("  LIVE:",b[:300])

# completion boundary check
print("\n=== completion boundaries ===")
pb=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if not gs:
            print(f"{tier}[{i}]: no guided_steps (input={p.get('input_type')})")
            continue
        # find phase index among box steps
        box_idx=[j for j,s in enumerate(gs) if ("answer" in s)]
        phase_j=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not phase_j:
            print(f"{tier}[{i}]: NO phase tag")
            continue
        pj=phase_j[0]
        before=[j for j in box_idx if j<pj]
        atafter=[j for j in box_idx if j>=pj]
        flag="" if (len(before)>=1 and len(atafter)>=2) else "  <-- CHECK"
        print(f"{tier}[{i}]: boxes_before={len(before)} boxes_at/after={len(atafter)}{flag}")
