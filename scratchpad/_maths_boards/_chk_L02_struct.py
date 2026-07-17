import json
pd = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]
pb = pd["problem_bank"]
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb:
        print(f"\n=== {t} : {len(pb[t])} problems ===")
        print("desc:", pb.get(t+"_description"))
