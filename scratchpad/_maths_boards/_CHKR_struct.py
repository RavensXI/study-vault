import json
pd=json.load(open("_CHKR_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
print("problem_bank keys:",list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs=pb.get(t,[])
    print(f"\n=== {t}: {len(probs) if isinstance(probs,list) else 'desc'} ===")
    if isinstance(probs,list):
        for i,p in enumerate(probs):
            print(f"[{i}] input_type={p.get('input_type')} chart={'Y' if p.get('chart') else '-'} svg={'Y' if '<svg' in p.get('display','') else '-'}")
            print("    display:",p.get('display','')[:200].replace('\n',' '))
            print("    solutions:",p.get('solutions'))
