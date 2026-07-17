import json
pd=json.load(open("_CHKR_live.json",encoding="utf-8"))["practice_data"]
teach=pd["guided"]["teach"]
for tier in ["bronze","silver","gold"]:
    w=teach.get(tier)
    print(f"\n########## TEACH {tier} ##########")
    print("keys:",list(w.keys()) if isinstance(w,dict) else type(w))
    if isinstance(w,dict):
        if "display" in w: print("display:",w["display"][:300])
        steps=w.get("steps",[])
        for j,s in enumerate(steps):
            if "say" in s and "answer" not in s:
                print(f" [{j}] SAY: {s['say'][:180]}")
            else:
                print(f" [{j}] pre={s.get('pre','')!r} post={s.get('post','')!r} answer={s.get('answer')} phase={s.get('phase','')} done={s.get('done','')[:60]!r}")
