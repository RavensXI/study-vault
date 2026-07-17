import json
pd=json.load(open("_CHKR_ps03_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
print("problem_bank keys:",list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb:
        probs=pb[t]
        print(f"\n=== {t}: {len(probs)} problems ===")
        for i,p in enumerate(probs):
            print(f"  [{i}] input_type={p.get('input_type')} sol={p.get('solutions')} has_chart={'chart' in p} has_gs={'guided_steps' in p} has_svg={'<svg' in p.get('display','')}")
