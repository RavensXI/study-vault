import json
ID="65e7a745-9820-431a-8b99-d96cd7514bf3"
live=json.load(open("_CHKR_ps03_live.json",encoding="utf-8"))["practice_data"]
pre=[e for e in json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8")) if e.get("id")==ID][0]["practice_data"]
out=[]
mc_pre=pre.get("method_card"); mc_live=live.get("method_card")
out.append("method_card content pre:\n"+str(mc_pre.get("content")))
out.append("\nmethod_card content live:\n"+str(mc_live.get("content")))
# compare solutions & displays per tier
for t in ["bronze","silver","gold"]:
    lp=live["problem_bank"][t]; pp=pre["problem_bank"].get(t,[])
    out.append(f"\n== {t}: pre {len(pp)} vs live {len(lp)}")
    for i in range(max(len(lp),len(pp))):
        ls=lp[i].get("solutions") if i<len(lp) else None
        ps=pp[i].get("solutions") if i<len(pp) else None
        ld=(lp[i].get("display","")[:55]) if i<len(lp) else None
        pdd=(pp[i].get("display","")[:55]) if i<len(pp) else None
        flag="SOLCHG" if ls!=ps else ""
        dchg="DISPCHG" if ld!=pdd else ""
        out.append(f"  [{i}] pre_sol={ps} live_sol={ls} {flag} {dchg}")
        if dchg:
            out.append(f"       pre_disp: {pdd}")
            out.append(f"       live_disp: {ld}")
open("_CHKR_ps03_pb.txt","w",encoding="utf-8").write("\n".join(out))
print("done")
