import json
pd = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]
pb = pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    print("="*70)
    print(t.upper())
    print("="*70)
    for i,p in enumerate(pb[t]):
        print(f"\n--- {t}[{i}] ---")
        print("display:", p.get("display"))
        print("input_type:", p.get("input_type"))
        print("solutions:", p.get("solutions"))
        print("answer:", p.get("answer"))
        print("hint:", p.get("hint"))
        print("calculator:", p.get("calculator"))
        misc = p.get("misconceptions",[])
        for j,m in enumerate(misc):
            print(f"  misc[{j}] pattern={m.get('pattern')} expect={m.get('expect')!r} msg={m.get('message')}")
