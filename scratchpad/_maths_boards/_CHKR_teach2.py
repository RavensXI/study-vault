import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHKR_live.json",encoding="utf-8"))["practice_data"]
teach=pd["guided"]["teach"]
for tier in ["bronze","silver","gold"]:
    w=teach.get(tier)
    print(f"\n########## TEACH {tier} ##########")
    if isinstance(w,dict):
        if "display" in w: print("display:",w["display"][:400])
        for j,s in enumerate(w.get("steps",[])):
            if "say" in s and "answer" not in s:
                print(f" [{j}] SAY: {s['say']}")
            else:
                print(f" [{j}] pre={s.get('pre','')!r} post={s.get('post','')!r} ans={s.get('answer')} phase={s.get('phase','')} hint={s.get('hint','')!r} done={s.get('done','')!r}")
