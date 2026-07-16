import json
d = json.load(open("_CHK_geomL01_live.json",encoding="utf-8"))
pd = d["practice_data"]
pb = pd["problem_bank"]
def show(tier):
    for i,p in enumerate(pb.get(tier,[])):
        print("\n"+"="*70)
        print(f"### {tier}[{i}]  solutions={p.get('solutions')}")
        print("DISPLAY:")
        print(p.get("display",""))
        print("HINT:", p.get("hint",""))
for t in ["bronze","silver","gold"]:
    print("\n\n########## TIER",t.upper())
    show(t)
