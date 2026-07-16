import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_live_graphsL01.json"))
pb=pd["problem_bank"]
for tier in ["silver","gold"]:
    for i,p in enumerate(pb[tier]):
        print(f"{tier}[{i}]: {p.get('display')}  SOL={p.get('solutions')}")
# teach walks
print("\n--- TEACH ---")
for t,w in pd["guided"].get("teach",{}).items():
    print(f"\n[{t}] q:", w.get("question") if isinstance(w,dict) else w)
    if isinstance(w,dict):
        for j,s in enumerate(w.get("steps",[])):
            if "<svg" in json.dumps(s): print(f"  step{j} HAS SVG")
