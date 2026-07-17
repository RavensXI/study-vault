import json
ID="d84411dc-60b7-4f96-8f42-35486f5d7129"
pre=[r for r in json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8")) if r.get("id")==ID][0]
pdpre=pre["practice_data"]
live=json.load(open("_ADVCHK_L13_live.json",encoding="utf-8"))
for tier in ["bronze","silver","gold"]:
    pb_pre=pdpre["problem_bank"].get(tier,[])
    pb_live=live["problem_bank"].get(tier,[])
    print(f"=== {tier}: pre {len(pb_pre)} live {len(pb_live)}")
    for i in range(max(len(pb_pre),len(pb_live))):
        pp=pb_pre[i] if i<len(pb_pre) else {}
        lp=pb_live[i] if i<len(pb_live) else {}
        dsame = pp.get("display")==lp.get("display")
        ssame = pp.get("solutions")==lp.get("solutions")
        osame = pp.get("options")==lp.get("options")
        if not (dsame and ssame and osame):
            print(f" [{i}] display_same={dsame} sol_same={ssame} opt_same={osame}")
            if not dsame:
                print("   PRE disp:", pp.get("display"))
                print("   LIVE disp:", lp.get("display"))
            if not ssame:
                print("   PRE sol:", pp.get("solutions"), "LIVE sol:", lp.get("solutions"))
            if not osame:
                print("   PRE opt:", pp.get("options"), "LIVE opt:", lp.get("options"))
