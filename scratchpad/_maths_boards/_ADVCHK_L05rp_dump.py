import json

pd = json.load(open("_ADVCHK_L05rp_live.json", encoding="utf-8"))["practice_data"]
pb = pd["problem_bank"]

for t in ["bronze","silver","gold"]:
    print("="*70)
    print(t.upper(), "  desc:", pb.get(t+"_description"))
    print("="*70)
    for i, p in enumerate(pb[t]):
        print(f"\n--- {t}[{i}]  input_type={p.get('input_type')} calc={p.get('calculator')}")
        print("DISPLAY:", p.get("display"))
        print("SOLUTIONS:", p.get("solutions"))
        print("HINT:", p.get("hint"))
        if p.get("chart"):
            print("CHART:", json.dumps(p["chart"])[:400])
        for m in p.get("misconceptions", []):
            print("  MISC pattern=",m.get("pattern")," expect=",m.get("expect")," msg=",m.get("message"))
        gs = p.get("guided_steps", [])
        for j, s in enumerate(gs):
            if "say" in s and "answer" not in s:
                print(f"    gs[{j}] SAY: {s['say']}")
            else:
                print(f"    gs[{j}] BOX pre={s.get('pre')!r} post={s.get('post')!r} answer={s.get('answer')!r} phase={s.get('phase')} hint={s.get('hint')!r}")
