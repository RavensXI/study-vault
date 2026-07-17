import json

data = json.load(open("_CHK_gL03_live.json", encoding="utf-8"))
pd = data[0]["practice_data"]

def show_problem(t, i, p):
    print(f"\n===== {t}[{i}] =====")
    print("display:", repr(p.get("display")))
    print("input_type:", p.get("input_type"), "| calculator:", p.get("calculator"))
    print("solutions:", p.get("solutions"), "| answer:", p.get("answer"))
    print("hint:", repr(p.get("hint")))
    if p.get("chart"):
        print("CHART:", json.dumps(p["chart"])[:600])
    for mi, m in enumerate(p.get("misconceptions", []) or []):
        print(f"  misc[{mi}]: pattern={m.get('pattern')!r} expect={m.get('expect')!r}")
        print(f"           message={m.get('message')!r}")
    gs = p.get("guided_steps", [])
    for gi, s in enumerate(gs):
        if "say" in s and "answer" not in s:
            print(f"  gs[{gi}] SAY: {s['say']!r}")
        else:
            ph = f" PHASE={s.get('phase')}" if s.get('phase') else ""
            print(f"  gs[{gi}] BOX pre={s.get('pre')!r} post={s.get('post')!r} answer={s.get('answer')!r} hint={s.get('hint')!r}{ph}")
            if s.get("done"): print(f"           done={s['done']!r}")
            if s.get("say"): print(f"           say={s['say']!r}")

pb = pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    print(f"\n######## {t.upper()} — {pb.get(t+'_description')!r}")
    for i, p in enumerate(pb[t]):
        show_problem(t, i, p)
