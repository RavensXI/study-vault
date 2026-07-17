import json
ID="93469b0d-2704-499c-a20b-587a84c2e214"
live = json.load(open("_ADVCHK_L05rp_live.json", encoding="utf-8"))["practice_data"]
pre = next(r for r in json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8")) if r.get("id")==ID)["practice_data"]
lb=live["problem_bank"]; pbk=pre["problem_bank"]
for t in ["bronze","silver","gold"]:
    lp,pp=lb[t],pbk[t]
    print(f"\n=== {t}: pre {len(pp)} / live {len(lp)}")
    for i in range(max(len(lp),len(pp))):
        a=pp[i] if i<len(pp) else None
        b=lp[i] if i<len(lp) else None
        da=a.get("display") if a else None
        db=b.get("display") if b else None
        sa=a.get("solutions") if a else None
        sb=b.get("solutions") if b else None
        if da!=db:
            print(f"  [{i}] DISPLAY changed:\n     PRE : {da}\n     LIVE: {db}")
        if sa!=sb:
            print(f"  [{i}] SOLUTIONS changed: {sa} -> {sb}")
