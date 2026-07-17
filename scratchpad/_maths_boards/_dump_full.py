import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open("_L09_live_fresh.json", encoding="utf-8"))["practice_data"]
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        print("="*70)
        print(f"{tier}[{i}] display: {p['display']}")
        print(f"  solutions: {p['solutions']}  calc={p.get('calculator')}  it={p.get('input_type')}")
        print(f"  hint: {p.get('hint')}")
        for j,m in enumerate(p.get("misconceptions",[])):
            print(f"  MISC[{j}] pattern={m.get('pattern')} expect={m.get('expect')}")
            print(f"     msg: {m.get('message')}")
        print("  GUIDED_STEPS:")
        for k,st in enumerate(p.get("guided_steps",[])):
            ph = " [PHASE:sub]" if st.get("phase")=="substitute" else ""
            if st.get("answer") is not None:
                print(f"    {k}{ph} BOX pre={st.get('pre')!r} post={st.get('post')!r} ans={st.get('answer')}")
            else:
                print(f"    {k}{ph} say={st.get('say')!r}")
