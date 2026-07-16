import json
pd=json.load(open("_live_algebra_L10.json",encoding="utf-8"))
pb=pd["problem_bank"]
for t in ("bronze","silver","gold"):
    print("="*70)
    print("TIER",t)
    for i,p in enumerate(pb[t]):
        print("-"*50)
        print(f"[{i}] input_type={p.get('input_type')} calculator={p.get('calculator')}")
        print("DISPLAY:",repr(p.get('display')))
        print("SOLUTIONS:",p.get('solutions'))
