import json
d=json.load(open("_chk_live_ps5.json",encoding="utf-8"))
pd=d["practice_data"]
print("TOP KEYS:", list(pd.keys()))
pb=pd.get("problem_bank",{})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs=pb.get(t) if isinstance(pb.get(t),list) else pb.get(t,{}).get("problems") if isinstance(pb.get(t),dict) else None
    print(t, type(pb.get(t)))
