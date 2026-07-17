import json
pd=json.load(open("_CHK_L04_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
print("problem_bank keys:",list(pb.keys()))
for tier in ["bronze","silver","gold"]:
    probs=pb.get(tier,[])
    print(f"\n=== {tier}: {len(probs)} problems ===")
    print("desc:",pb.get(tier+"_description"))
    for i,p in enumerate(probs):
        print(f"[{i}] input_type={p.get('input_type')} sol={p.get('solutions')} has_chart={'chart' in p} has_gs={'guided_steps' in p}")
