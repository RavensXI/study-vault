import json
pd=json.load(open("_live_graphsL01.json"))
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    arr=pb[tier]
    print(f"\n########## {tier} ##########")
    for i,p in enumerate(arr):
        print(f"\n----- {tier}[{i}] -----")
        print("DISPLAY:", p.get("display"))
        print("SOL:", p.get("solutions"))
        print("HINT:", p.get("hint"))
        if "chart" in p:
            print("CHART:", json.dumps(p["chart"]))
