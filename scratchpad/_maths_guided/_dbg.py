import json
live=json.load(open("_live_L04.json",encoding="utf-8"))
for tier in ["gold","bronze","silver"]:
    for j,prob in enumerate(live["problem_bank"][tier]):
        gs=prob.get("guided_steps",[])
        rows=[]
        for i,s in enumerate(gs):
            tag="P" if s.get("phase")=="substitute" else " "
            has="ans" if "answer" in s else "say"
            rows.append(f"{i}{tag}:{has}")
        print(tier,j,"|"," ".join(rows))
