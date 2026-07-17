import json
pd=json.load(open("_CHKR_L06_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
for t in ["gold","silver","bronze"]:
    sols=[tuple(p["solutions"]) for p in pb[t]]
    dups=[s for s in sols if sols.count(s)>1]
    print(t, "solutions", sols, "DUPS" if dups else "distinct")
