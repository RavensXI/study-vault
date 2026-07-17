# -*- coding: utf-8 -*-
import json
base = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards"
live = json.load(open(base + r"\_chk_rp02_live.json", encoding="utf-8"))
d = json.load(open(base + r"\_pre_dump_maths-aqa.json", encoding="utf-8"))
SID="5b37c8ce-e970-4d38-9c96-c65baa661fa4"
entry=[r for r in d if r["id"]==SID][0]
pre=entry["practice_data"]
print("PRE keys :", sorted(pre.keys()))
print("LIVE keys:", sorted(live.keys()))
print("added keys:", sorted(set(live)-set(pre)))
print("removed keys:", sorted(set(pre)-set(live)))
for f in ["related_videos","topic_links","worked_examples","method_card"]:
    pv=pre.get(f,"<MISSING>"); lv=live.get(f,"<MISSING>")
    same=json.dumps(pv,sort_keys=True,ensure_ascii=False)==json.dumps(lv,sort_keys=True,ensure_ascii=False)
    print(f"\nPRESERVE {f}: {'OK' if same else 'CHANGED'}")
    if not same:
        print("  PRE :",json.dumps(pv,ensure_ascii=False)[:400])
        print("  LIVE:",json.dumps(lv,ensure_ascii=False)[:400])
# problem count + displays/solutions preserved?
print("\n--- problem_bank display/solution compare ---")
for tier in ["bronze","silver","gold"]:
    pl=pre.get("problem_bank",{}).get(tier,[])
    ll=live["problem_bank"][tier]
    print(f"{tier}: pre={len(pl)} live={len(ll)}")
    for i in range(min(len(pl),len(ll))):
        if pl[i].get("display")!=ll[i].get("display"):
            print(f"  {tier}[{i}] DISPLAY changed:\n    PRE :{pl[i].get('display')}\n    LIVE:{ll[i].get('display')}")
        if pl[i].get("solutions")!=ll[i].get("solutions"):
            print(f"  {tier}[{i}] SOLUTION changed: pre={pl[i].get('solutions')} live={ll[i].get('solutions')}")
