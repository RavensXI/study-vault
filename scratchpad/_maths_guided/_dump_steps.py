import json
pd = json.load(open("_revise_L05_live.json",encoding="utf-8"))
out = []
for tier, idx in [("gold",0),("gold",4),("silver",5),("silver",2),("teach","gold")]:
    if tier == "teach":
        prob = pd["guided"]["teach"]["gold"]
        out.append(f"\n=== TEACH GOLD ===")
        out.append("problem: " + json.dumps(prob.get("problem",""), ensure_ascii=False))
        steps = prob.get("steps", [])
    else:
        prob = pd["problem_bank"][tier][idx]
        out.append(f"\n=== {tier}[{idx}] ===")
        out.append("display: " + str(prob.get("display")))
        out.append("solutions: " + str(prob.get("solutions")))
        steps = prob.get("guided_steps", [])
    for i, s in enumerate(steps):
        out.append(f"  [{i}] {json.dumps(s, ensure_ascii=False)}")
open("_steps_dump.txt","w",encoding="utf-8").write("\n".join(out))
print("done")
