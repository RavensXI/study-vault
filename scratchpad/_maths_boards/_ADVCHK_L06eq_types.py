# -*- coding: utf-8 -*-
import json
ID="a36e47ae-bd22-4127-af9d-5b37e34c0b64"
live=json.load(open("_ADVCHK_L06eq_live.json",encoding="utf-8"))
dump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
pre=[r for r in dump if r.get("id")==ID][0]["practice_data"]
for t in ["bronze","silver","gold"]:
    pp=pre["problem_bank"][t]; pl=live["problem_bank"][t]
    for i in range(len(pl)):
        it_p=pp[i].get("input_type"); it_l=pl[i].get("input_type")
        cal_p=pp[i].get("calculator"); cal_l=pl[i].get("calculator")
        flag = "  <-- INPUT_TYPE CHANGED" if it_p!=it_l else ""
        print(f"{t}[{i}] input_type {it_p} -> {it_l}{flag} | calc {cal_p}->{cal_l} | pre_sol={pp[i].get('solutions')}")
