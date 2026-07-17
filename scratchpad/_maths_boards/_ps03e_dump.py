import json,sys
sys.stdout.reconfigure(encoding="utf-8")
pd=json.load(open("_ps03e_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
for t in ("bronze","silver","gold"):
    print("="*70)
    print("TIER",t.upper(),"  count:",len(pb[t]))
    for i,p in enumerate(pb[t]):
        print("-"*60)
        print(f"[{t}][{i}] keys:",list(p.keys()))
        print("  display:",repr(p.get("display")))
        print("  input_type:",p.get("input_type"))
        print("  solutions:",p.get("solutions"))
        print("  answer:",p.get("answer"))
        print("  hint:",repr(p.get("hint")))
        if "chart" in p: print("  chart: PRESENT")
        mis=p.get("misconceptions")
        if mis:
            for m in mis:
                print("   mis pattern:",repr(m.get("pattern"))," expect:",m.get("expect")," msg:",repr(m.get("message")))
    # descriptions
for k in pb:
    if k not in ("bronze","silver","gold"):
        print("PB other key:",k,"=",pb[k])
