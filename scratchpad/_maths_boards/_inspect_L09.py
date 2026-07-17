import json
pd = json.load(open("_L09_live_fresh.json",encoding="utf-8"))["practice_data"]
# check mojibake in gold[0]
g0 = pd["problem_bank"]["gold"][0]["display"]
print("GOLD0 repr:", repr(g0))
print()
# guided block
gd = pd.get("guided",{})
print("guided keys:", list(gd.keys()))
op = gd.get("opener",{})
print("opener display:", repr(op.get("display")))
print("opener n steps:", len(op.get("steps",[])))
for s in op.get("steps",[]):
    print("   box ans:", s.get("answer"), "| pre:", repr(s.get("pre")))
teach = gd.get("teach",{})
for t in ("bronze","silver","gold"):
    tt = teach.get(t,{})
    print(t,"teach display:", repr(tt.get("display")), "nboxes:", sum(1 for st in tt.get("steps",[]) if st.get("answer") is not None))
# tier_guides
print()
tg = pd.get("tier_guides",{})
for t in ("bronze","silver","gold"):
    print("TG",t,"title:",repr(tg.get(t,{}).get("title")))
# check each problem has guided_steps, hint, tier descriptions
pb = pd["problem_bank"]
for t in ("bronze","silver","gold"):
    print("desc",t,repr(pb.get(t+"_description")))
    for i,p in enumerate(pb[t]):
        print("  ",t,i,"gs:",len(p.get("guided_steps",[])),"hint:",bool(p.get("hint")),"misc:",len(p.get("misconceptions",[])))
