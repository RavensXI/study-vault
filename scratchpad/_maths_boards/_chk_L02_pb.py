import json,io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ID="cbc91397-a67c-472a-b0da-308aa9da1653"
live = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
entry=[r for r in pre if r.get("id")==ID][0]["practice_data"]
for tier in ["bronze","silver","gold"]:
    pl,ll=entry["problem_bank"][tier],live["problem_bank"][tier]
    print(f"=== {tier}: pre_n={len(pl)} live_n={len(ll)}")
    for i in range(max(len(pl),len(ll))):
        pd_=pl[i] if i<len(pl) else {}
        ld_=ll[i] if i<len(ll) else {}
        pdisp,ldisp=pd_.get("display"),ld_.get("display")
        psol,lsol=pd_.get("solutions"),ld_.get("solutions")
        flag = "" if (pdisp==ldisp and psol==lsol) else "  <<CHANGED>>"
        if flag:
            print(f"  [{i}] disp {pdisp!r} -> {ldisp!r} | sol {psol} -> {lsol}{flag}")
print("\nmethod_card example full:")
print(live["method_card"].get("example"))
