import json
live = json.load(open("_chk_live_L08.json", encoding="utf-8"))
pb=live["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps");sol=p.get("solutions")
        if not gs or p.get("input_type")=="multiple_choice":continue
        # solution box = the phase step's answer
        ph=next((s for s in gs if s.get("phase")=="substitute"),None)
        val=ph.get("answer") if ph else None
        ok = sol and abs(float(val)-float(sol[0]))<1e-9
        last=[s for s in gs if "answer" in s][-1]
        is_check = "check" in (last.get("pre","")+last.get("done","")).lower()
        print(f"{tier}[{i}] phase-box={val} sol={sol[0]} {'OK' if ok else 'MISMATCH'} last_is_check={is_check}")
