import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
pd=json.load(open("_CHKR_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        print(f"\n===== {t}[{i}] :: {p['display']}  sol={p.get('solutions')}")
        print("  hint:",p.get("hint"))
        gs=p.get("guided_steps",[])
        for j,s in enumerate(gs):
            if "say" in s and "answer" not in s:
                print(f"   ({j}) SAY: {s['say']}")
            else:
                print(f"   ({j}) pre={s.get('pre','')!r} post={s.get('post','')!r} ans={s.get('answer')} phase={s.get('phase','')} done={s.get('done','')!r}")
        for m in p.get("misconceptions",[]):
            print(f"   MISC expect={m.get('expect')!r} pattern={m.get('pattern')!r} msg={m.get('message')!r}")
