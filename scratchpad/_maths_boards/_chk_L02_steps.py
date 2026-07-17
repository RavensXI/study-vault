import json,io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]
pb = pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        print("="*64)
        print(f"{tier}[{i}]  display={p.get('display')}  sol={p.get('solutions')}")
        if gs is None:
            print("  NO guided_steps  skip_reason=", p.get("guided_skip_reason"))
            continue
        boxidx=0
        for s in gs:
            if "say" in s and "answer" not in s:
                print(f"   say: {s['say']}")
            else:
                ph = "  <<PHASE:substitute>>" if s.get("phase")=="substitute" else ""
                print(f"   box#{boxidx}: pre={s.get('pre')!r} post={s.get('post')!r} answer={s.get('answer')}{ph}")
                if s.get("done"): print(f"        done={s['done']}")
                boxidx+=1
