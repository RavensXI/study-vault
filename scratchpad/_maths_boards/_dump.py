import json, io
pd=json.load(io.open("_live_graphs-L01.json",encoding="utf-8"))["practice_data"]
out=io.open("_dump_full.txt","w",encoding="utf-8")
def p(*a): print(*a,file=out)
pb=pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    p("="*70); p("TIER",t.upper(), "  desc:",pb.get(t+"_description"))
    for i,prob in enumerate(pb[t]):
        p("-"*60)
        p(f"[{t}][{i}] input_type={prob.get('input_type')} calc={prob.get('calculator')}")
        p(" display:",prob.get("display"))
        p(" solutions:",json.dumps(prob.get("solutions"),ensure_ascii=False))
        p(" answer:",json.dumps(prob.get("answer"),ensure_ascii=False))
        p(" hint:",prob.get("hint"))
        if prob.get("chart"): p(" CHART:",json.dumps(prob.get("chart"),ensure_ascii=False))
        mc=prob.get("misconceptions")
        if mc:
            for j,m in enumerate(mc):
                p(f"   MC[{j}] expect={json.dumps(m.get('expect'),ensure_ascii=False)} pattern={m.get('pattern')}")
                p(f"        msg={m.get('message')}")
        gs=prob.get("guided_steps")
        if gs:
            for k,s in enumerate(gs):
                if "say" in s and "answer" not in s:
                    p(f"   step[{k}] SAY: {s['say']}")
                else:
                    ph=(" PHASE="+s['phase']) if s.get('phase') else ""
                    p(f"   step[{k}] pre={s.get('pre')!r} post={s.get('post')!r} ANS={json.dumps(s.get('answer'),ensure_ascii=False)}{ph}")
                    if s.get('hint'): p(f"        hint={s.get('hint')}")
                    if s.get('done'): p(f"        done={s.get('done')}")
out.close()
print("done")
