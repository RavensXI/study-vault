import json
pd = json.load(open("_L08_live.json", encoding="utf-8"))
pb = pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    print(f"\n########## {tier} ({pb.get(tier+'_description')}) ##########")
    for i,p in enumerate(pb[tier]):
        print(f"\n--- [{i}] ---")
        for k,v in p.items():
            print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
