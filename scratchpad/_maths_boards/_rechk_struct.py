import json
pd=json.load(open("_rechk_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
print("problem_bank keys:",list(pb.keys()))
for tier in ["bronze","silver","gold"]:
    probs=pb.get(tier,[])
    print(f"\n=== {tier}: {len(probs)} problems ===")
    for i,p in enumerate(probs):
        print(f" [{i}] input_type={p.get('input_type')} sol={p.get('solutions')} has_chart={'chart' in p} disp_has_svg={'<svg' in p.get('display','')}")
