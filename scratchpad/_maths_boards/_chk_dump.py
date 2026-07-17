import json
d=json.load(open("_chk_live_ps5.json",encoding="utf-8"))
pd=d["practice_data"]
pb=pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    print("="*70)
    print(t.upper(), " desc:", pb.get(t+"_description"))
    for i,p in enumerate(pb[t]):
        print("-"*50)
        print(f"[{t}][{i}] input_type={p.get('input_type')} calc={p.get('calculator')}")
        print("DISPLAY:", p.get("display"))
        print("SOLUTIONS:", p.get("solutions"))
        print("HINT:", p.get("hint"))
        if p.get("chart"): print("HAS CHART")
        for j,m in enumerate(p.get("misconceptions",[])):
            print(f"  MISC[{j}] pattern={m.get('pattern')} expect={m.get('expect')} msg={m.get('message')}")
