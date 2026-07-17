import json,sys
sys.stdout.reconfigure(encoding="utf-8")
s=json.load(open("_CHKR_ps03_shard.json",encoding="utf-8"))
pb=s["problem_bank"]
for t in ("bronze","silver","gold"):
    print("#### DESC",t,":",repr(pb.get(t+"_description")))
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        print("="*60)
        hasfig = "<svg" in (p.get("display") or "")
        print(f"[{t}][{i}] it={p.get('input_type')} sols={p.get('solutions')} svg={hasfig} chart={'chart' in p}")
        print("  display:", (p.get('display') or '')[:120].replace(chr(10),' '))
        print("  hint:",repr(p.get("hint")))
        for m in (p.get("misconceptions") or []):
            print("   MIS pat=",repr(m.get("pattern"))," expect=",m.get("expect")," msg=",repr(m.get("message"))[:90])
        gs=p.get("guided_steps")
        if gs:
            print("  GUIDED_STEPS:")
            for st in gs:
                if "say" in st and st.get("answer") is None:
                    print("    say:",st["say"][:80])
                else:
                    print(f"    box pre={st.get('pre')!r} post={st.get('post')!r} ans={st.get('answer')} phase={st.get('phase')} done={bool(st.get('done'))}")
