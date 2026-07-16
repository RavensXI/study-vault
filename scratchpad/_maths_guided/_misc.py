import json, io, sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_live_L07_CHECKER.json",encoding="utf-8"))
pb=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]
        for j,m in enumerate(p.get("misconceptions",[])):
            exp=m.get("expect")
            flag=" <-- COLLIDES WITH SOLUTION" if exp==sol else ""
            print(f"{tier}[{i}].misc[{j}] expect={exp} sol={sol}{flag}")
# teach box counts
for t,w in live["guided"]["teach"].items():
    boxes=[s for s in w["steps"] if "answer" in s]
    print(f"teach.{t}: {len(boxes)} boxes, answers={[s['answer'] for s in boxes]}")
op=[s for s in live["guided"]["opener"]["steps"] if "answer" in s]
print("opener boxes:",[s['answer'] for s in op])
