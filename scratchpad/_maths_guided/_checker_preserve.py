# -*- coding: utf-8 -*-
import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="1c2aa03c-fff3-4f9a-83f6-438c587b8948"
live=json.load(open("_live_L02.json",encoding="utf-8"))
pre=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_pre_fanout_dump.json",encoding="utf-8"))
# find pre entry
def find(o):
    if isinstance(o,dict):
        if o.get("id")==ID: return o
        for v in o.values():
            r=find(v)
            if r: return r
    elif isinstance(o,list):
        for v in o:
            r=find(v)
            if r: return r
    return None
pe=find(pre)
print("pre entry found:", pe is not None)
ppd = pe.get("practice_data") if pe else None
if ppd:
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE:",json.dumps(ppd.get(f),ensure_ascii=False)[:400])
            print("  LIVE:",json.dumps(live.get(f),ensure_ascii=False)[:400])
    # input types preserved?
    for tier in ["bronze","silver","gold"]:
        pit=[p.get("input_type") for p in ppd.get("problem_bank",{}).get(tier,[])]
        lit=[p.get("input_type") for p in live.get("problem_bank",{}).get(tier,[])]
        pn=len(ppd.get("problem_bank",{}).get(tier,[])); ln=len(live.get("problem_bank",{}).get(tier,[]))
        print(f"{tier}: pre_n={pn} live_n={ln} pre_types={set(pit)} live_types={set(lit)}")
    # pre gold[0] display
    print("PRE gold[0] display:", ppd.get("problem_bank",{}).get("gold",[{}])[0].get("display"))
    print("PRE bronze[5] display:", ppd.get("problem_bank",{}).get("bronze",[{}]*6)[5].get("display") if len(ppd.get("problem_bank",{}).get("bronze",[]))>5 else "n/a")
