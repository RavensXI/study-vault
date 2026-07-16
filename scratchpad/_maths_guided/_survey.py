import json
pd=json.load(open("_live_graphsL01.json"))
pb=pd["problem_bank"]
print("problem_bank keys:", list(pb.keys()))
for tier in ["bronze","silver","gold"]:
    if tier in pb:
        arr=pb[tier]
        print(f"\n=== {tier}: {len(arr)} problems ===")
        for i,p in enumerate(arr):
            has_chart="chart" in p
            disp=p.get("display","")
            has_svg="<svg" in disp
            print(f"[{i}] chart={has_chart} svg={has_svg} input={p.get('input_type')} sol={p.get('solutions')}")
