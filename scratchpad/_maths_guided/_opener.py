import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_live_graphsL01.json"))
op=pd["guided"]["opener"]
print("OPENER DISPLAY:\n", op.get("display"))
print("\nOPENER STEPS:")
for i,s in enumerate(op.get("steps",[])):
    print(f"[{i}]", json.dumps(s,ensure_ascii=False))
