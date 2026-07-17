import json
live=json.load(open("_ADV_ps01_live.json",encoding="utf-8"))["practice_data"]
pb=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        disp=p["display"].split("</svg>")[-1].replace("<br>","").strip()
        for k,m in enumerate(p.get("misconceptions",[])):
            print(f"{tier}[{i}].misc[{k}] pattern={m.get('pattern')} note={m.get('note')!r} expect={m.get('expect')} sol={p['solutions']}")
            print("   Q:",disp[:90])
            print("   msg:",m.get('message'))
        if p.get("misconceptions"): print()
